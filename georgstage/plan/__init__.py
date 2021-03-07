from dataclasses import dataclass, asdict
from datetime import date
from enum import Enum
from typing import List
import pandas as pd

class Task(Enum):
  VAGTHAVENDE_ELEV = 1
  ORDONNANS = 2
  UDKIG = 3
  BJÆRGEMÆRS = 4
  RORGÆNGER = 5
  UDSÆTNINGSGAST = 6
  HÅNDVÆRKSMÆSSIG_UDDANNELSE = 7
  PEJLEGAST_A = 8
  PEJLEGAST_B = 9
  DÆKSELEV_I_KABYS = 10
  SYG = 11

@dataclass
class Assignment:
    """Class for keeping track of gast -> task assignments"""
    date: date
    at_sea: bool
    gast_no: int
    team_no: int
    shift_no: int
    task: Task

    def asdict(self):
        d = asdict(self)
        d['task'] = self.task.name
        return d

@dataclass
class Plan:
    assignments: List[Assignment]

    def asdf(self):
        dicts = self.asdicts()
        df = pd.DataFrame(dicts)
        df.date = pd.to_datetime(df.date)
        return

    def asdicts(self):
        return [x.asdict() for x in self.assignments]
