from dataclasses import dataclass
from enum import Enum
import os.path

import numpy as np
import pandas as pd

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
    tidspunkt: int
    skifte: int
    gast: int
    opgave: Opgave

    def to_dict(self):
        return {
            'dato': self.dato,
            'tidspunkt': self.tidspunkt,
            'skifte': self.skifte,
            'gast': self.gast,
            'opgave_value': self.opgave.value,
            'opgave_name': self.opgave.name
        }

    @staticmethod
    def from_dict(d):
        opgave = Opgave(d['opgave_value']) if 'opgave_value' in d else Opgave[d['opgave_name']]
        return Vagt(
            dato = d['dato'],
            tidspunkt = d['tidspunkt'],
            skifte = d['skifte'],
            gast = d['gast'],
            opgave = opgave
        )


def load(filein):
    df = pd.read_csv(filein)
    vagter = {}
    for dato, grp in df.groupby('dato'):
        vagter[dato] = [Vagt.from_dict(row) for idx, row in grp.iterrows()]
    return GeorgStage(vagter)

class GeorgStage:

    def __init__(self, vagter):
        if type(vagter) == list:
            self._vagter = {}
            for vagt in vagter:
                self._vagter.setdefault(vagt.dato, []).append(vagt)
        elif type(vagter) == dict:
            self._vagter = vagter
        else:
            raise TypeError('Argument vagter must have type List[Vagt] or Dict[str,Vagt]')

    def __len__(self):
        pass

    def __getitem__(self, datestr):
        return self._vagter.get(datestr) or []

    def __setitem__(self, datestr, vagter):
        self._vagter[datestr] = vagter

    def __delitem__(self, datestr):
        del self._vagter[datestr]

    def get_datoer(self):
        return list(self._vagter.keys())

    def validate(self):
        pass

    def get_vagter(self, before=None, exclude=[]):
        if type(exclude) == str:
            exclude = [exclude]
        for dato, values in self._vagter.items():
            if (before and dato >= before) or dato in exclude: continue
            for vagt in values:
                yield vagt

    def autofill(self, datestr):
        vagter = self[datestr]
        andre = []
        filled_day = None
        return filled_day

    def get_stats(self):
        pass

    def save(self, fout):
        pass


class Analyzer:

    def get_counts(self, vagter, n_gaster=60):
        df = pd.DataFrame([a.to_dict() for a in vagter])
        hist = df.groupby(['gast', 'opgave_value']).size()
        counts = df.groupby(['gast', 'opgave_value']).size()
        return lambda gast,opgave: counts.get((gast,opgave.value)) or 0

    def get_counts_frame(self, vagter, n_gaster=60):
        counts = self.get_counts(vagter, n_gaster)
        df = pd.DataFrame(range(1, n_gaster + 1), columns=['gast'])
        for opgave in Opgave:
            df[opgave.name] = df.gast.apply(lambda g: counts(g, opgave))
        return df
