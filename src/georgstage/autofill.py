from dataclasses import dataclass
from typing import List

import pandas as pd
import pulp as P

from georgstage.model import Opgave, Vagt


N_GASTS = 60
VAGT_TIDER = [0, 4, 8, 12, 16, 20]


@dataclass
class FillResult:
    status: int
    vagter: List[Vagt]
    stats: List[int]


class AutoFiller:

    def __init__(self):
        pass

    def get_counts(self, vagter: List[Vagt]):
        """
        Returns function with signature lookup(gast:int, opgave:str) -> count: int
        Treat fysiske vagter special: sum of all fysiske, not just concrete
        """
        stats = {}
        fysiske = (Opgave.ORDONNANS, Opgave.UDKIG,
                   Opgave.BJAERGEMAERS, Opgave.RORGAENGER)
        for vagt in vagter:
            if vagt.opgave in fysiske:
                keys = [(vagt.gast, opgave) for opgave in fysiske]
            else:
                keys = [(vagt.gast, vagt.opgave)]
            for key in keys:
                stats[key] = stats.setdefault(key, 0) + 1
        return lambda gast, opgave: stats.get((gast, opgave)) or 0

    def get_counts_frame(self, vagter):
        """
        Returns dataframe with rows = gaster, columns = opgaver, values = count
        """
        counts = self.get_counts(vagter, N_GASTS)
        df = pd.DataFrame(range(1, N_GASTS + 1), columns=['gast'])
        for opgave in Opgave:
            df[opgave.name] = df.gast.apply(lambda g: counts(g, opgave))
        return df

    def get_skifte_for_gast(self, gast):
        if 0 < gast <= 20:
            return 1
        elif 20 < gast <= 40:
            return 2
        else:
            return 3

    def autofill(self, model, skifter=[1, 2, 3, 1, 2, 3]):
        """
        Limitation: vagthavende elev must be filled manually to ensure same gast
        morning and evening.
        """
        datestr = str(model.get_current_dato())
        day_vagter = model[datestr]
        other_vagter = list(model.get_vagter(before=datestr))
        lookup = self.get_counts(day_vagter + other_vagter)

        # Problem
        prob = P.LpProblem('udfyld_vagter', P.LpMinimize)

        # All gaster
        gaster = [gast for gast in range(1, N_GASTS+1)]

        # All opgaver
        opgaver = [o.value for o in Opgave]

        # Special opgaver
        opgaver_spec = [
            Opgave.UDE.value,
            Opgave.DAEKSELEV_I_KABYS.value,
            Opgave.PEJLEGAST_A.value,
            Opgave.PEJLEGAST_B.value,
        ]
        # Normal opgaver
        opgaver_norm = [o.value for o in Opgave if o.value not in opgaver_spec]

        # Decision variables (normal tasks)
        #   X_ijt: gast i, opgave j, hour t
        X = P.LpVariable.dicts(
            'X', (gaster, opgaver, VAGT_TIDER), 0, 1, P.LpBinary)

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

        # preassigned day vagter must be assigned
        for vagt in day_vagter:
            prob += X[vagt.gast][vagt.opgave.value][vagt.vagt_tid] == 1

        # all tasks except:
        # - UDE, PEJLEGAST_A, PEJLEGAST_B, DAEKSELEV_I_KABYS
        # must be assigned exactly once per vagt_tid
        for j in opgaver_norm:
            for t in VAGT_TIDER:
                prob += P.lpSum(
                    [X[i][j][t]
                     for i in gaster
                     ]) == 1

        # Pejlegaster only 16-20 vagt
        for t in VAGT_TIDER:
            # Set RHS to 1 if vagt_tid is 16, else 0
            rhs = 1 if t == 16 else 0
            prob += P.lpSum([X[i][Opgave.PEJLEGAST_A.value][t]
                            for i in gaster]) == rhs
            prob += P.lpSum([X[i][Opgave.PEJLEGAST_B.value][t]
                            for i in gaster]) == rhs

        # Dæks elev i kabys. Only 4, 8, 12, 16
        for t in VAGT_TIDER:
            # Set RHS to 1 if vagt_tid is 16, else 0
            rhs = 1 if t in [4, 8, 12, 16] else 0
            prob += P.lpSum([
                X[i][Opgave.DAEKSELEV_I_KABYS.value][t]
                for i in gaster
            ]) == rhs

        # gasts can have at most one task per shift
        for i in gaster:
            for t in VAGT_TIDER:
                prob += P.lpSum([X[i][j][t] for j in opgaver]) <= 1

        # gasts can take zero tasks outside their own shift
        for idx, skifte in enumerate(skifter):
            gaster_inactive = [
                i for i in gaster if self.get_skifte_for_gast(i) != skifte]
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
                        vagter.append(
                            Vagt(datestr, vagt_tid, gast, Opgave(opgave)))

        stats = [lookup(vagt.gast, vagt.opgave) for vagt in vagter]

        return FillResult(status=status, vagter=vagter, stats=stats)
