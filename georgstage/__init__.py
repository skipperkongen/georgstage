from dataclasses import dataclass
from enum import Enum
import os.path
from typing import Tuple, List

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
    BJAERGEMAERS = 3
    RORGAENGER = 4
    UDSAETNINGSGAST_A = 5
    UDSAETNINGSGAST_B = 6
    UDSAETNINGSGAST_C = 7
    UDSAETNINGSGAST_D = 8
    UDSAETNINGSGAST_E = 9
    PEJLEGAST_A = 10
    PEJLEGAST_B = 11
    DAEKSELEV_I_KABYS = 12
    HU = 13
    INAKTIV = 14


@dataclass
class Vagt:
    dato: str
    vagt_tid: int
    gast: int
    opgave: Opgave

    def to_dict(self):
        return {
            'dato': self.dato,
            'vagt_tid': self.vagt_tid,
            'gast': self.gast,
            'opgave': self.opgave.name
        }

    @staticmethod
    def from_dict(d):
        return Vagt(
            dato = d['dato'],
            vagt_tid = d['vagt_tid'],
            gast = d['gast'],
            opgave = Opgave[d['opgave']]
        )


@dataclass
class FillResult:
    status: int
    vagter: List[Vagt]
    stats: List[int]


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
        """
        Limitation: vagthavende elev must be filled manually to ensure same gast
        morning and evening.
        """

        day_vagter = georgstage[datestr]
        other_vagter = list(georgstage.get_vagter(before=datestr))
        lookup = self.get_counts(day_vagter + other_vagter)

        # Problem
        prob = P.LpProblem('udfyld_vagter', P.LpMinimize)

        # Remove gasts from problem, who should not be assigned
        opgaver = [o.value for o in Opgave]
        opgaver_spec = [
            Opgave.HU.value,
            Opgave.INAKTIV.value,
            Opgave.DAEKSELEV_I_KABYS.value,
            Opgave.PEJLEGAST_A.value,
            Opgave.PEJLEGAST_B.value
        ]
        opgaver_norm = [o.value for o in Opgave if o.value not in opgaver_spec]

        gaster = [gast for gast in range(1, N_GASTS+1)]

        # Decision variables (normal tasks)
        #   X_ijt: gast i, opgave j, hour t
        X = P.LpVariable.dicts('X', (gaster, opgaver, VAGT_TIDER), 0, 1, P.LpBinary)

        lookup = self.get_counts(day_vagter + other_vagter)

        # Coefficients (number of times gast performed task)
        coef = {}
        for i in gaster:
            for j in opgaver:
                coef.setdefault(i, {})[j] = lookup(i, Opgave(j))

        # Objective function
        prob += P.lpSum([
            coef[i][j] * X[i][j][t]
            for i in gaster
            for j in opgaver
            for t in VAGT_TIDER
        ])

        ## preassigned day vagter must be assigned
        for vagt in day_vagter:
            prob += X[vagt.gast][vagt.opgave.value][vagt.vagt_tid] == 1

        ## all tasks except:
        ## - HU, INACTIVE, PEJLEGAST_A, PEJLEGAST_B, DAEKSELEV_I_KABYS
        ## must be assigned exactly once per vagt_tid
        for j in opgaver_norm:
            for t in VAGT_TIDER:
                prob += P.lpSum(
                    [X[i][j][t]
                    for i in gaster
                ]) == 1

        ## Pejlegaster only 16-20 vagt
        for t in VAGT_TIDER:
            # Set RHS to 1 if vagt_tid is 16, else 0
            rhs = 1 if t == 16 else 0
            prob += P.lpSum([X[i][Opgave.PEJLEGAST_A.value][t]for i in gaster]) == rhs
            prob += P.lpSum([X[i][Opgave.PEJLEGAST_B.value][t]for i in gaster]) == rhs

        ## Kabys only 8-12, 12-16 and 16-20 vagt
        for t in VAGT_TIDER:
            # Set RHS to 1 if vagt_tid is 16, else 0
            rhs = 1 if t in [8, 12, 16] else 0
            prob += P.lpSum([
                X[i][Opgave.DAEKSELEV_I_KABYS.value][t]
                for i in gaster
            ]) == rhs

        ## gasts can have at most one task per shift
        for i in gaster:
            for t in VAGT_TIDER:
                prob += P.lpSum([X[i][j][t] for j in opgaver]) <= 1

        ## gasts can take zero tasks outside their own shift
        for idx, skifte in enumerate(skifter):
            gaster_inactive = [i for i in gaster if self.get_skifte_for_gast(i) != skifte]
            t = VAGT_TIDER[idx]
            prob += P.lpSum([
                X[i][j][t]
                for i in gaster_inactive
                for j in opgaver
            ]) == 0

        # Solve
        status = prob.solve()
        vagter = []
        for gast in gaster:
            for opgave in opgaver:
                for vagt_tid in VAGT_TIDER:
                    x = X[gast][opgave][vagt_tid]
                    if x.varValue == 1:
                        vagter.append(Vagt(datestr, vagt_tid, gast, Opgave(opgave)))

        stats = [lookup(vagt.gast, vagt.opgave) for vagt in vagter]

        return FillResult(status=status, vagter=vagter, stats=stats)


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
        Returns a FillResult
        """
        return self._auto_filler.autofill(self, datestr)

    def to_dataframe(self):
        return pd.DataFrame([v.to_dict() for v in self.get_vagter()])

    def save(self, abspath):
        pass
