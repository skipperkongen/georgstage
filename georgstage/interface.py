import datetime
import random
import tkinter as tk
from tkinter import messagebox

WIDTH = 11

class View():

    def __init__(self, root, controller):
        self.controller = controller
        self.controller.view = self
        self.build(root)
        self.controller.initialize()

    def build(self, root):
        # Static widgets
        tk.Label(root, text='Valgte dag').grid(row=0, column=0, sticky=tk.E)
        tk.Label(root, text='Skifter').grid(row=1, column=0, sticky=tk.E)
        tk.Label(root, text='Søvagt').grid(row=2, column=0, sticky=tk.E)
        # tider
        tk.Label(root, text='08-12', width=WIDTH).grid(row=2, column=1)
        tk.Label(root, text='12-16', width=WIDTH).grid(row=2, column=2)
        tk.Label(root, text='16-20', width=WIDTH).grid(row=2, column=3)
        tk.Label(root, text='20-24', width=WIDTH).grid(row=2, column=4)
        tk.Label(root, text='00-04', width=WIDTH).grid(row=2, column=5)
        tk.Label(root, text='04-08', width=WIDTH).grid(row=2, column=6)
        # resten
        tk.Label(root, text='Vagthavende ELEV').grid(row=3, column=0, sticky=tk.E)
        tk.Label(root, text='Ordonnans').grid(row=4, column=0, sticky=tk.E)
        tk.Label(root, text='Udkig').grid(row=5, column=0, sticky=tk.E)
        tk.Label(root, text='Bjærgemærs').grid(row=6, column=0, sticky=tk.E)
        tk.Label(root, text='Rorgænger').grid(row=7, column=0, sticky=tk.E)
        tk.Label(root, text='Udsætningsgast A').grid(row=8, column=0, sticky=tk.E)
        tk.Label(root, text='Udsætningsgast B').grid(row=9, column=0, sticky=tk.E)
        tk.Label(root, text='Udsætningsgast C').grid(row=10, column=0, sticky=tk.E)
        tk.Label(root, text='Udsætningsgast D').grid(row=11, column=0, sticky=tk.E)
        tk.Label(root, text='Udsætningsgast E').grid(row=12, column=0, sticky=tk.E)
        tk.Label(root, text='Pejlegast A/B').grid(row=13, column=0, sticky=tk.E)
        tk.Label(root, text='HU').grid(row=14, column=0, sticky=tk.E)
        tk.Label(root, text='Dækselev i kabys').grid(row=15, column=0, sticky=tk.E)
        tk.Label(root, text='Syge (f.eks 1,2,3)').grid(row=16, column=0, sticky=tk.E)

        # Variables
        vars = {
            'date': tk.StringVar(),
            'skifte1': tk.StringVar(),
            'skifte2': tk.StringVar(),
            'skifte3': tk.StringVar(),
            'skifte4': tk.StringVar(),
            'skifte5': tk.StringVar(),
            'skifte6': tk.StringVar(),
            've1': tk.StringVar(),
            've2': tk.StringVar(),
            've3': tk.StringVar(),
            've4': tk.StringVar(),
            've5': tk.StringVar(),
            've6': tk.StringVar(),
            'o1': tk.StringVar(),
            'o2': tk.StringVar(),
            'o3': tk.StringVar(),
            'o4': tk.StringVar(),
            'o5': tk.StringVar(),
            'o6': tk.StringVar(),
            'u1': tk.StringVar(),
            'u2': tk.StringVar(),
            'u3': tk.StringVar(),
            'u4': tk.StringVar(),
            'u5': tk.StringVar(),
            'u6': tk.StringVar(),
            'bm1': tk.StringVar(),
            'bm2': tk.StringVar(),
            'bm3': tk.StringVar(),
            'bm4': tk.StringVar(),
            'bm5': tk.StringVar(),
            'bm6': tk.StringVar(),
            'rg1': tk.StringVar(),
            'rg2': tk.StringVar(),
            'rg3': tk.StringVar(),
            'rg4': tk.StringVar(),
            'rg5': tk.StringVar(),
            'rg6': tk.StringVar(),
            'uga1': tk.StringVar(),
            'uga2': tk.StringVar(),
            'uga3': tk.StringVar(),
            'uga4': tk.StringVar(),
            'uga5': tk.StringVar(),
            'uga6': tk.StringVar(),
            'ugb1': tk.StringVar(),
            'ugb2': tk.StringVar(),
            'ugb3': tk.StringVar(),
            'ugb4': tk.StringVar(),
            'ugb5': tk.StringVar(),
            'ugb6': tk.StringVar(),
            'ugc1': tk.StringVar(),
            'ugc2': tk.StringVar(),
            'ugc3': tk.StringVar(),
            'ugc4': tk.StringVar(),
            'ugc5': tk.StringVar(),
            'ugc6': tk.StringVar(),
            'ugd1': tk.StringVar(),
            'ugd2': tk.StringVar(),
            'ugd3': tk.StringVar(),
            'ugd4': tk.StringVar(),
            'ugd5': tk.StringVar(),
            'ugd6': tk.StringVar(),
            'uge1': tk.StringVar(),
            'uge2': tk.StringVar(),
            'uge3': tk.StringVar(),
            'uge4': tk.StringVar(),
            'uge5': tk.StringVar(),
            'uge6': tk.StringVar(),
            'pga': tk.StringVar(),
            'pgb': tk.StringVar(),
            'hu1': tk.StringVar(),
            'hu2': tk.StringVar(),
            'hu3': tk.StringVar(),
            'hu4': tk.StringVar(),
            'hu5': tk.StringVar(),
            'hu6': tk.StringVar(),
            'dk1': tk.StringVar(),
            'dk2': tk.StringVar(),
            'dk3': tk.StringVar(),
            'dk4': tk.StringVar(),
            'dk5': tk.StringVar(),
            'dk6': tk.StringVar(),
            'syge': tk.StringVar()
        }

        self._vars = vars

        # Widgets controlled by variables
        tk.Label(root, textvariable=vars['date'], background='gray').grid(row=0, column=1)

        tk.Entry(root, textvariable=vars['skifte1'], justify='right', width=WIDTH).grid(row=1, column=1)
        tk.Entry(root, textvariable=vars['skifte2'], justify='right', width=WIDTH).grid(row=1, column=2)
        tk.Entry(root, textvariable=vars['skifte3'], justify='right', width=WIDTH).grid(row=1, column=3)
        tk.Entry(root, textvariable=vars['skifte4'], justify='right', width=WIDTH).grid(row=1, column=4)
        tk.Entry(root, textvariable=vars['skifte5'], justify='right', width=WIDTH).grid(row=1, column=5)
        tk.Entry(root, textvariable=vars['skifte6'], justify='right', width=WIDTH).grid(row=1, column=6)

        tk.Entry(root, textvariable=vars['ve1'], justify='right', width=WIDTH).grid(row=3, column=1)
        tk.Entry(root, textvariable=vars['ve2'], justify='right', width=WIDTH).grid(row=3, column=2)
        tk.Entry(root, textvariable=vars['ve3'], justify='right', width=WIDTH).grid(row=3, column=3)
        tk.Entry(root, textvariable=vars['ve4'], justify='right', width=WIDTH).grid(row=3, column=4)
        tk.Entry(root, textvariable=vars['ve5'], justify='right', width=WIDTH).grid(row=3, column=5)
        tk.Entry(root, textvariable=vars['ve6'], justify='right', width=WIDTH).grid(row=3, column=6)

        tk.Entry(root, textvariable=vars['o1'], justify='right', width=WIDTH).grid(row=4, column=1)
        tk.Entry(root, textvariable=vars['o2'], justify='right', width=WIDTH).grid(row=4, column=2)
        tk.Entry(root, textvariable=vars['o3'], justify='right', width=WIDTH).grid(row=4, column=3)
        tk.Entry(root, textvariable=vars['o4'], justify='right', width=WIDTH).grid(row=4, column=4)
        tk.Entry(root, textvariable=vars['o5'], justify='right', width=WIDTH).grid(row=4, column=5)
        tk.Entry(root, textvariable=vars['o6'], justify='right', width=WIDTH).grid(row=4, column=6)

        tk.Entry(root, textvariable=vars['u1'], justify='right', width=WIDTH).grid(row=5, column=1)
        tk.Entry(root, textvariable=vars['u2'], justify='right', width=WIDTH).grid(row=5, column=2)
        tk.Entry(root, textvariable=vars['u3'], justify='right', width=WIDTH).grid(row=5, column=3)
        tk.Entry(root, textvariable=vars['u4'], justify='right', width=WIDTH).grid(row=5, column=4)
        tk.Entry(root, textvariable=vars['u5'], justify='right', width=WIDTH).grid(row=5, column=5)
        tk.Entry(root, textvariable=vars['u6'], justify='right', width=WIDTH).grid(row=5, column=6)

        tk.Entry(root, textvariable=vars['bm1'], justify='right', width=WIDTH).grid(row=6, column=1)
        tk.Entry(root, textvariable=vars['bm2'], justify='right', width=WIDTH).grid(row=6, column=2)
        tk.Entry(root, textvariable=vars['bm3'], justify='right', width=WIDTH).grid(row=6, column=3)
        tk.Entry(root, textvariable=vars['bm4'], justify='right', width=WIDTH).grid(row=6, column=4)
        tk.Entry(root, textvariable=vars['bm5'], justify='right', width=WIDTH).grid(row=6, column=5)
        tk.Entry(root, textvariable=vars['bm6'], justify='right', width=WIDTH).grid(row=6, column=6)

        tk.Entry(root, textvariable=vars['rg1'], justify='right', width=WIDTH).grid(row=7, column=1)
        tk.Entry(root, textvariable=vars['rg2'], justify='right', width=WIDTH).grid(row=7, column=2)
        tk.Entry(root, textvariable=vars['rg3'], justify='right', width=WIDTH).grid(row=7, column=3)
        tk.Entry(root, textvariable=vars['rg4'], justify='right', width=WIDTH).grid(row=7, column=4)
        tk.Entry(root, textvariable=vars['rg5'], justify='right', width=WIDTH).grid(row=7, column=5)
        tk.Entry(root, textvariable=vars['rg6'], justify='right', width=WIDTH).grid(row=7, column=6)

        tk.Entry(root, textvariable=vars['uga1'], justify='right', width=WIDTH).grid(row=8, column=1)
        tk.Entry(root, textvariable=vars['uga2'], justify='right', width=WIDTH).grid(row=8, column=2)
        tk.Entry(root, textvariable=vars['uga3'], justify='right', width=WIDTH).grid(row=8, column=3)
        tk.Entry(root, textvariable=vars['uga4'], justify='right', width=WIDTH).grid(row=8, column=4)
        tk.Entry(root, textvariable=vars['uga5'], justify='right', width=WIDTH).grid(row=8, column=5)
        tk.Entry(root, textvariable=vars['uga6'], justify='right', width=WIDTH).grid(row=8, column=6)

        tk.Entry(root, textvariable=vars['ugb1'], justify='right', width=WIDTH).grid(row=9, column=1)
        tk.Entry(root, textvariable=vars['ugb2'], justify='right', width=WIDTH).grid(row=9, column=2)
        tk.Entry(root, textvariable=vars['ugb3'], justify='right', width=WIDTH).grid(row=9, column=3)
        tk.Entry(root, textvariable=vars['ugb4'], justify='right', width=WIDTH).grid(row=9, column=4)
        tk.Entry(root, textvariable=vars['ugb5'], justify='right', width=WIDTH).grid(row=9, column=5)
        tk.Entry(root, textvariable=vars['ugb6'], justify='right', width=WIDTH).grid(row=9, column=6)

        tk.Entry(root, textvariable=vars['ugc1'], justify='right', width=WIDTH).grid(row=10, column=1)
        tk.Entry(root, textvariable=vars['ugc2'], justify='right', width=WIDTH).grid(row=10, column=2)
        tk.Entry(root, textvariable=vars['ugc3'], justify='right', width=WIDTH).grid(row=10, column=3)
        tk.Entry(root, textvariable=vars['ugc4'], justify='right', width=WIDTH).grid(row=10, column=4)
        tk.Entry(root, textvariable=vars['ugc5'], justify='right', width=WIDTH).grid(row=10, column=5)
        tk.Entry(root, textvariable=vars['ugc6'], justify='right', width=WIDTH).grid(row=10, column=6)

        tk.Entry(root, textvariable=vars['ugd1'], justify='right', width=WIDTH).grid(row=11, column=1)
        tk.Entry(root, textvariable=vars['ugd2'], justify='right', width=WIDTH).grid(row=11, column=2)
        tk.Entry(root, textvariable=vars['ugd3'], justify='right', width=WIDTH).grid(row=11, column=3)
        tk.Entry(root, textvariable=vars['ugd4'], justify='right', width=WIDTH).grid(row=11, column=4)
        tk.Entry(root, textvariable=vars['ugd5'], justify='right', width=WIDTH).grid(row=11, column=5)
        tk.Entry(root, textvariable=vars['ugd6'], justify='right', width=WIDTH).grid(row=11, column=6)

        tk.Entry(root, textvariable=vars['uge1'], justify='right', width=WIDTH).grid(row=12, column=1)
        tk.Entry(root, textvariable=vars['uge2'], justify='right', width=WIDTH).grid(row=12, column=2)
        tk.Entry(root, textvariable=vars['uge3'], justify='right', width=WIDTH).grid(row=12, column=3)
        tk.Entry(root, textvariable=vars['uge4'], justify='right', width=WIDTH).grid(row=12, column=4)
        tk.Entry(root, textvariable=vars['uge5'], justify='right', width=WIDTH).grid(row=12, column=5)
        tk.Entry(root, textvariable=vars['uge6'], justify='right', width=WIDTH).grid(row=12, column=6)

        frame = tk.Frame()
        tk.Entry(frame, textvariable=vars['pga'], justify='right', width=4).pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=vars['pgb'], justify='right', width=4).pack(side=tk.LEFT)
        frame.grid(row=13, column=3)

        tk.Entry(root, textvariable=vars['hu1'], justify='right', width=WIDTH).grid(row=14, column=1)
        tk.Entry(root, textvariable=vars['hu2'], justify='right', width=WIDTH).grid(row=14, column=2)
        tk.Entry(root, textvariable=vars['hu3'], justify='right', width=WIDTH).grid(row=14, column=3)
        tk.Entry(root, textvariable=vars['hu4'], justify='right', width=WIDTH).grid(row=14, column=4)
        tk.Entry(root, textvariable=vars['hu5'], justify='right', width=WIDTH).grid(row=14, column=5)
        tk.Entry(root, textvariable=vars['hu6'], justify='right', width=WIDTH).grid(row=14, column=6)

        tk.Entry(root, textvariable=vars['dk1'], justify='right', width=WIDTH).grid(row=15, column=1)
        tk.Entry(root, textvariable=vars['dk2'], justify='right', width=WIDTH).grid(row=15, column=2)
        tk.Entry(root, textvariable=vars['dk3'], justify='right', width=WIDTH).grid(row=15, column=3)
        tk.Entry(root, textvariable=vars['dk4'], justify='right', width=WIDTH).grid(row=15, column=4)
        tk.Entry(root, textvariable=vars['dk5'], justify='right', width=WIDTH).grid(row=15, column=5)
        tk.Entry(root, textvariable=vars['dk6'], justify='right', width=WIDTH).grid(row=15, column=6)
        tk.Entry(root, textvariable=vars['syge'], justify='right', width=WIDTH).grid(row=16, column=1)

        # Buttons
        tk.Button(root, text='Forrige dag', command=self.controller.prev_day).grid(row=0, column=2)
        tk.Button(root, text='Næste dag', command=self.controller.next_day).grid(row=0, column=3)
        tk.Button(root, text='Load', command=self.controller.load).grid(row=0, column=5)
        tk.Button(root, text='Save', command=self.controller.save).grid(row=0, column=6)
        tk.Button(root, text='Udfyld resten', command=self.controller.fill_day).grid(row=17, column=5)
        tk.Button(root, text='Eksporter', command=self.controller.export_day).grid(row=17, column=6)

    def set_vars(self, vars):
        # set date
        for key, value in vars.items():
            assert(key in self._vars)
            self._vars[key].set(value)

    def get_vars(self):
        return {k:v.get() for k,v in self._vars.items()}


class Controller():

    def __init__(self, model):
        self.view = None
        self.model = model

    def _todatestr(self, date):
        return f'{date.year}/{str(date.month).zfill(2)}/{str(date.day).zfill(2)}'

    def _fromdatestr(self, datestr):
        return datetime.datetime.strptime(datestr, '%Y/%m/%d').date()

    def load(self):
        pass

    def save(self):
        pass

    def initialize(self):
        print('initialize called')
        date = self._todatestr(datetime.date.today())
        day = self.model.get_day(date)
        self.view.set_vars(day)

    def change_day(self, num_days):
        cur_day = self.view.get_vars()
        cur_date = cur_day['date']
        self.model.set_day(cur_date, cur_day)
        new_date =  self._fromdatestr(cur_date) + datetime.timedelta(days=num_days)
        new_date = self._todatestr(new_date)
        new_day = self.model.get_day(new_date)
        self.view.set_vars(new_day)

    def next_day(self):
        print('next_day called')
        self.change_day(1)

    def prev_day(self):
        print('prev_day called')
        self.change_day(-1)

    def reset(self):
        print('reset called')

    def fill_day(self):
        print('fill_day called')
        vars = self.view.get_vars()
        new_vars = {k:random.randint(1,60) for k in vars if k != 'date'}
        self.view.set_vars(new_vars)

    def export_day(self):
        print('export_day called')

    def close(self):
        print('close called')

class Model():

    def __init__(self, days=None):
        self.days = days or {}

    def get_day(self, date):
        if date in self.days:
            return self.days[date]
        else:
            self.days[date] = {'date': date}
            return self.days[date]

    def set_day(self, date, vars):
        self.days[date] = vars

if __name__=='__main__':
    root = tk.Tk()
    root.title('Georg Stage Søvagt - version 0.1')
    model = Model()
    controller = Controller(model)
    view = View(root, controller)
    tk.mainloop()
