import pathlib
import os
import pandas as pd
from georgstage.solver import *

localdir = pathlib.Path(__file__).parent.absolute()

DEFAULT_PATH = os.path.join(localdir, '..', 'data', 'togt.csv')

class App:

    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.df = None
        self.current_day = None

    def foo(self):
        return 42

    def load(self):
        self.df = pd.read_csv(self.path)
        self.current_day = self.df.date.max()

    def save(self):
        self.df.to_csv(self.path, index=False)
