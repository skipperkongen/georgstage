from dataclasses import dataclass, asdict
from datetime import date
from enum import Enum

class Task(Enum):
    

@dataclass
class Assigment:
    """Class for keeping track of gast -> task assignments"""
    date: date
    at_sea: bool
    gast_no: int
    team_no: int
    shift_no: int
    task: int

    def asdict(self):
        return asdict(self)
