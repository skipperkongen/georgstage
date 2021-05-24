from dataclasses import dataclass
from enum import Enum
import os.path
from typing import Tuple

import numpy as np
import pandas as pd
import pulp as P
import pdb

N_GASTS = 60
VAGT_TIDER = [0, 4, 8, 12, 16, 20]


class Opgave(Enum):
    VAGTHAVENDE_ELEV = 0
    ORDONNANS = 1
    UDKIG = 2
    BJÆRGEMÆRS = 3
    RORGÆNGER = 4
    UDSÆTNINGSGAST_A = 5
    UDSÆTNINGSGAST_B = 6
    UDSÆTNINGSGAST_C = 7
    UDSÆTNINGSGAST_D = 8
    UDSÆTNINGSGAST_E = 9
    PEJLEGAST_A = 10
    PEJLEGAST_B = 11
    DÆKSELEV_I_KABYS = 12
    HU = 13
    INAKTIV = 14

@dataclass
class Vagt:
    dato: str
    vagt_tid: int
    skifte: int
    gast: int
    opgave: Opgave

    def to_dict(self):
        return {
            'dato': self.dato,
            'vagt_tid': self.vagt_tid,
            'skifte': self.skifte,
            'gast': self.gast,
            'opgave': self.opgave.name
        }

    @staticmethod
    def from_dict(d):
        return Vagt(
            dato = d['dato'],
            vagt_tid = d['vagt_tid'],
            skifte = d['skifte'],
            gast = d['gast'],
            opgave = Opgave[d['opgave']]
        )


def load(filein):
    df = pd.read_csv(filein)
    vagter = {}
    for dato, grp in df.groupby('dato'):
        vagter[dato] = [Vagt.from_dict(row) for idx, row in grp.iterrows()]
    return GeorgStage(vagter)


class AutoFiller:

    def __init__(self):
        pass

    def get_counts(self, vagter):
        """
        Returns function with signature lookup(gast:int, opgave:str) -> count: int
        """
        if len(vagter):
            df = pd.DataFrame([a.to_dict() for a in vagter])
        else:
            df = pd.DataFrame([], columns=[
                'dato', 'vagt_tid', 'skifte', 'gast', 'opgave'
            ])
        hist = df.groupby(['gast', 'opgave']).size()
        counts = df.groupby(['gast', 'opgave']).size()
        return lambda gast, opgave: counts.get((gast,opgave.name)) or 0

    def get_counts_frame(self, vagter):
        """
        Returns dataframe with rows = gaster, columns = opgaver, values = count
        """
        counts = self.get_counts(vagter, N_GASTER)
        df = pd.DataFrame(range(1, N_GASTER + 1), columns=['gast'])
        for opgave in Opgave:
            df[opgave.name] = df.gast.apply(lambda g: counts(g, opgave))
        return df

    def get_skifte_for_gast(self, gast):
        if 0 < gast <= 20:
            return 1
        elif  20 < gast <= 40:
            return 2
        else:
            return 3


    def autofill(self, georgstage, datestr, skifter=[1,2,3,1,2,3]):

        day_vagter = georgstage[datestr]
        other_vagter = list(georgstage.get_vagter(before=datestr))
        lookup = self.get_counts(day_vagter + other_vagter)

        # Problem
        prob = P.LpProblem('udfyld_vagter', P.LpMinimize)

        # Remove gasts from problem, who should not be assigned
        opgaver_out = [Opgave.HU, Opgave.INAKTIV]
        opgaver_in = [o.value for o in Opgave if o not in opgaver_out]
        gaster_out = {vagt.gast for vagt in day_vagter if vagt.opgave in opgaver_out}
        gaster_in = [gast for gast in range(1, N_GASTS+1) if gast not in gaster_out]

        # Decision variables (normal tasks)
        #   X_ijt: gast i, opgave j, hour t
        X = P.LpVariable.dicts('X', (gaster_in, opgaver_in, VAGT_TIDER), 0, 1, P.LpBinary)

        lookup = self.get_counts(day_vagter + other_vagter)

        # Coefficients (task counts)
        coef = {}
        for i in gaster_in:
            for j in opgaver_in:
                coef.setdefault(i, {})[j] = lookup(i, Opgave(j))

        # Objective function
        prob += P.lpSum([
            coef[i][j] * X[i][j][t]
            for i in gaster_in
            for j in opgaver_in
            for t in VAGT_TIDER
        ])

        # Constraints to force variables up

        ## preassigned day vagter must be assigned
        for vagt in day_vagter:
            if vagt.opgave not in opgaver_out:
                prob += X[vagt.gast][vagt.opgave.value][vagt.vagt_tid] == 1

        ## all tasks must be assigned exactly once in every vagttid
        for j in opgaver_in:
            for t in VAGT_TIDER:
                prob += P.lpSum([X[i][j][t] for i in gaster_in]) == 1

        ## gasts can have at most one task per shift
        for i in gaster_in:
            for t in VAGT_TIDER:
                prob += P.lpSum([X[i][j][t] for j in opgaver_in]) <= 1

        ## gasts can only take tasks during their own shift
        for idx, skifte in enumerate(skifter):
            gaster_active = [i for i in gaster_in if self.get_skifte_for_gast(i) == skifte]
            t = VAGT_TIDER[idx]
            prob += P.lpSum([
                X[i][j][t]
                for i in gaster_in if i not in gaster_active
                for j in opgaver_in
            ]) == 0
        status = prob.solve()
        filled_day = []
        for gast in gaster_in:
            for opgave in opgaver_in:
                for idx, vagt_tid in enumerate(VAGT_TIDER):
                    skifte = skifter[idx]
                    x = X[gast][opgave][vagt_tid]
                    if x.varValue == 1:
                        filled_day.append(Vagt(datestr, vagt_tid, skifte, gast, Opgave(opgave)))

        stats = [lookup(vagt.gast, vagt.opgave) for vagt in filled_day]

        return status, zip(filled_day, stats)


class GeorgStage:

    def __init__(self, vagter, auto_filler=AutoFiller()):
        if type(vagter) == list:
            self._vagter = {}
            for vagt in vagter:
                self._vagter.setdefault(vagt.dato, []).append(vagt)
        elif type(vagter) == dict:
            self._vagter = vagter
        else:
            raise TypeError('Argument vagter must have type List[Vagt] or Dict[str,Vagt]')
        self._auto_filler = auto_filler

    def __len__(self):
        """
        returns the number of days set, i.e. distinct **keys** in self._vagter
        """
        return len(self._vagter)

    def __getitem__(self, datestr):
        return self._vagter.get(datestr) or []

    def __setitem__(self, datestr, vagter):
        """
        Set list of Vagter object on a given day
        """
        self._vagter[datestr] = vagter

    def __delitem__(self, datestr):
        del self._vagter[datestr]

    def get_datoer(self):
        """
        Returns all days that have been set, even empty ones.
        """
        return list(self._vagter.keys())

    def validate(self):
        """
        Validate that the GeorgStage instance is valid.
        """
        return True

    def get_vagter(self, before=None, exclude=[]):
        """
        Returns all vagter objects, with optional filtering.
        """
        if type(exclude) == str:
            exclude = [exclude]
        for dato, values in self._vagter.items():
            if (before and dato >= before) or dato in exclude: continue
            for vagt in values:
                yield vagt

    def autofill(self, datestr):
        """
        Returns a filled day, which can then be set using gs['SOME_DATE'] = filled_day.
        """
        status, solution = self._auto_filler.autofill(self, datestr)
        return status, solution

    def save(self, fout):
        pass
