from dataclasses import dataclass

import numpy as np

@dataclass
class SeaDay:
    shifts: list
    sick: list
    tasks: np.ndarray
    pejle_a: int
    pejle_b: int

    def is_valid(self):
        """
        Perform checks that SeaDay is valid
        """
        if len(self.shifts) != 6:
            return False
        elif tasks.shape != (12,6):
            return False
        elif self.inconsistent():
            return False
        else:
            return True

    def inconsistent(self):
        """
        Check that each sailor is accounted for exactly once
        """


class Planner:

    def fill_seaday(self, full_hist, sea_day):
        return day


    def fill_portday(self, hist, partial_day, sick=[], shift=0):
        raise NotImplementedError()
