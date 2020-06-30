from datetime import datetime

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class Gui():

    def __init__(self, root):
        self.root = root
        # Static widgets
        tk.Label(root, text='Valgte dag').grid(row=0, column=0, sticky=tk.E)
        tk.Label(root, text='Skifter').grid(row=1, column=0, sticky=tk.E)
        tk.Label(root, text='Søvagt').grid(row=2, column=0, sticky=tk.E)
        # tider
        tk.Label(root, text='08-12', width=10).grid(row=2, column=1)
        tk.Label(root, text='12-16', width=10).grid(row=2, column=2)
        tk.Label(root, text='16-20', width=10).grid(row=2, column=3)
        tk.Label(root, text='20-24', width=10).grid(row=2, column=4)
        tk.Label(root, text='00-04', width=10).grid(row=2, column=5)
        tk.Label(root, text='04-08', width=10).grid(row=2, column=6)
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
        self._date = tk.StringVar()
        self._skifte1 = tk.StringVar()
        self._skifte2 = tk.StringVar()
        self._skifte3 = tk.StringVar()
        self._skifte4 = tk.StringVar()
        self._skifte5 = tk.StringVar()
        self._skifte6 = tk.StringVar()

        self._ve1 = tk.StringVar()
        self._ve2 = tk.StringVar()
        self._ve3 = tk.StringVar()
        self._ve4 = tk.StringVar()
        self._ve5 = tk.StringVar()
        self._ve6 = tk.StringVar()

        self._o1 = tk.StringVar()
        self._o2 = tk.StringVar()
        self._o3 = tk.StringVar()
        self._o4 = tk.StringVar()
        self._o5 = tk.StringVar()
        self._o6 = tk.StringVar()

        self._u1 = tk.StringVar()
        self._u2 = tk.StringVar()
        self._u3 = tk.StringVar()
        self._u4 = tk.StringVar()
        self._u5 = tk.StringVar()
        self._u6 = tk.StringVar()

        self._bm1 = tk.StringVar()
        self._bm2 = tk.StringVar()
        self._bm3 = tk.StringVar()
        self._bm4 = tk.StringVar()
        self._bm5 = tk.StringVar()
        self._bm6 = tk.StringVar()

        self._rg1 = tk.StringVar()
        self._rg2 = tk.StringVar()
        self._rg3 = tk.StringVar()
        self._rg4 = tk.StringVar()
        self._rg5 = tk.StringVar()
        self._rg6 = tk.StringVar()

        self._uga1 = tk.StringVar()
        self._uga2 = tk.StringVar()
        self._uga3 = tk.StringVar()
        self._uga4 = tk.StringVar()
        self._uga5 = tk.StringVar()
        self._uga6 = tk.StringVar()

        self._ugb1 = tk.StringVar()
        self._ugb2 = tk.StringVar()
        self._ugb3 = tk.StringVar()
        self._ugb4 = tk.StringVar()
        self._ugb5 = tk.StringVar()
        self._ugb6 = tk.StringVar()

        self._ugc1 = tk.StringVar()
        self._ugc2 = tk.StringVar()
        self._ugc3 = tk.StringVar()
        self._ugc4 = tk.StringVar()
        self._ugc5 = tk.StringVar()
        self._ugc6 = tk.StringVar()

        self._ugd1 = tk.StringVar()
        self._ugd2 = tk.StringVar()
        self._ugd3 = tk.StringVar()
        self._ugd4 = tk.StringVar()
        self._ugd5 = tk.StringVar()
        self._ugd6 = tk.StringVar()

        self._uge1 = tk.StringVar()
        self._uge2 = tk.StringVar()
        self._uge3 = tk.StringVar()
        self._uge4 = tk.StringVar()
        self._uge5 = tk.StringVar()
        self._uge6 = tk.StringVar()

        self._pga = tk.StringVar()
        self._pgb = tk.StringVar()

        self._hu1 = tk.StringVar()
        self._hu2 = tk.StringVar()
        self._hu3 = tk.StringVar()
        self._hu4 = tk.StringVar()
        self._hu5 = tk.StringVar()
        self._hu6 = tk.StringVar()

        self._dk1 = tk.StringVar()
        self._dk2 = tk.StringVar()
        self._dk3 = tk.StringVar()
        self._dk4 = tk.StringVar()
        self._dk5 = tk.StringVar()
        self._dk6 = tk.StringVar()

        self._syge = tk.StringVar()


        # Widgets controlled by variables
        tk.Label(root, textvariable=self._date, background='gray').grid(row=0, column=1)

        tk.Entry(root, textvariable=self._skifte1, justify='right', width=10).grid(row=1, column=1)
        tk.Entry(root, textvariable=self._skifte2, justify='right', width=10).grid(row=1, column=2)
        tk.Entry(root, textvariable=self._skifte3, justify='right', width=10).grid(row=1, column=3)
        tk.Entry(root, textvariable=self._skifte4, justify='right', width=10).grid(row=1, column=4)
        tk.Entry(root, textvariable=self._skifte5, justify='right', width=10).grid(row=1, column=5)
        tk.Entry(root, textvariable=self._skifte6, justify='right', width=10).grid(row=1, column=6)

        tk.Entry(root, textvariable=self._ve1, justify='right', width=10).grid(row=3, column=1)
        tk.Entry(root, textvariable=self._ve2, justify='right', width=10).grid(row=3, column=2)
        tk.Entry(root, textvariable=self._ve3, justify='right', width=10).grid(row=3, column=3)
        tk.Entry(root, textvariable=self._ve4, justify='right', width=10).grid(row=3, column=4)
        tk.Entry(root, textvariable=self._ve5, justify='right', width=10).grid(row=3, column=5)
        tk.Entry(root, textvariable=self._ve6, justify='right', width=10).grid(row=3, column=6)

        tk.Entry(root, textvariable=self._o1, justify='right', width=10).grid(row=4, column=1)
        tk.Entry(root, textvariable=self._o2, justify='right', width=10).grid(row=4, column=2)
        tk.Entry(root, textvariable=self._o3, justify='right', width=10).grid(row=4, column=3)
        tk.Entry(root, textvariable=self._o4, justify='right', width=10).grid(row=4, column=4)
        tk.Entry(root, textvariable=self._o5, justify='right', width=10).grid(row=4, column=5)
        tk.Entry(root, textvariable=self._o6, justify='right', width=10).grid(row=4, column=6)

        tk.Entry(root, textvariable=self._u1, justify='right', width=10).grid(row=5, column=1)
        tk.Entry(root, textvariable=self._u2, justify='right', width=10).grid(row=5, column=2)
        tk.Entry(root, textvariable=self._u3, justify='right', width=10).grid(row=5, column=3)
        tk.Entry(root, textvariable=self._u4, justify='right', width=10).grid(row=5, column=4)
        tk.Entry(root, textvariable=self._u5, justify='right', width=10).grid(row=5, column=5)
        tk.Entry(root, textvariable=self._u6, justify='right', width=10).grid(row=5, column=6)

        tk.Entry(root, textvariable=self._bm1, justify='right', width=10).grid(row=6, column=1)
        tk.Entry(root, textvariable=self._bm2, justify='right', width=10).grid(row=6, column=2)
        tk.Entry(root, textvariable=self._bm3, justify='right', width=10).grid(row=6, column=3)
        tk.Entry(root, textvariable=self._bm4, justify='right', width=10).grid(row=6, column=4)
        tk.Entry(root, textvariable=self._bm5, justify='right', width=10).grid(row=6, column=5)
        tk.Entry(root, textvariable=self._bm6, justify='right', width=10).grid(row=6, column=6)

        tk.Entry(root, textvariable=self._rg1, justify='right', width=10).grid(row=7, column=1)
        tk.Entry(root, textvariable=self._rg2, justify='right', width=10).grid(row=7, column=2)
        tk.Entry(root, textvariable=self._rg3, justify='right', width=10).grid(row=7, column=3)
        tk.Entry(root, textvariable=self._rg4, justify='right', width=10).grid(row=7, column=4)
        tk.Entry(root, textvariable=self._rg5, justify='right', width=10).grid(row=7, column=5)
        tk.Entry(root, textvariable=self._rg6, justify='right', width=10).grid(row=7, column=6)

        tk.Entry(root, textvariable=self._uga1, justify='right', width=10).grid(row=8, column=1)
        tk.Entry(root, textvariable=self._uga2, justify='right', width=10).grid(row=8, column=2)
        tk.Entry(root, textvariable=self._uga3, justify='right', width=10).grid(row=8, column=3)
        tk.Entry(root, textvariable=self._uga4, justify='right', width=10).grid(row=8, column=4)
        tk.Entry(root, textvariable=self._uga5, justify='right', width=10).grid(row=8, column=5)
        tk.Entry(root, textvariable=self._uga6, justify='right', width=10).grid(row=8, column=6)

        tk.Entry(root, textvariable=self._ugb1, justify='right', width=10).grid(row=9, column=1)
        tk.Entry(root, textvariable=self._ugb2, justify='right', width=10).grid(row=9, column=2)
        tk.Entry(root, textvariable=self._ugb3, justify='right', width=10).grid(row=9, column=3)
        tk.Entry(root, textvariable=self._ugb4, justify='right', width=10).grid(row=9, column=4)
        tk.Entry(root, textvariable=self._ugb5, justify='right', width=10).grid(row=9, column=5)
        tk.Entry(root, textvariable=self._ugb6, justify='right', width=10).grid(row=9, column=6)

        tk.Entry(root, textvariable=self._ugc1, justify='right', width=10).grid(row=10, column=1)
        tk.Entry(root, textvariable=self._ugc2, justify='right', width=10).grid(row=10, column=2)
        tk.Entry(root, textvariable=self._ugc3, justify='right', width=10).grid(row=10, column=3)
        tk.Entry(root, textvariable=self._ugc4, justify='right', width=10).grid(row=10, column=4)
        tk.Entry(root, textvariable=self._ugc5, justify='right', width=10).grid(row=10, column=5)
        tk.Entry(root, textvariable=self._ugc6, justify='right', width=10).grid(row=10, column=6)

        tk.Entry(root, textvariable=self._ugd1, justify='right', width=10).grid(row=11, column=1)
        tk.Entry(root, textvariable=self._ugd2, justify='right', width=10).grid(row=11, column=2)
        tk.Entry(root, textvariable=self._ugd3, justify='right', width=10).grid(row=11, column=3)
        tk.Entry(root, textvariable=self._ugd4, justify='right', width=10).grid(row=11, column=4)
        tk.Entry(root, textvariable=self._ugd5, justify='right', width=10).grid(row=11, column=5)
        tk.Entry(root, textvariable=self._ugd6, justify='right', width=10).grid(row=11, column=6)

        tk.Entry(root, textvariable=self._uge1, justify='right', width=10).grid(row=12, column=1)
        tk.Entry(root, textvariable=self._uge2, justify='right', width=10).grid(row=12, column=2)
        tk.Entry(root, textvariable=self._uge3, justify='right', width=10).grid(row=12, column=3)
        tk.Entry(root, textvariable=self._uge4, justify='right', width=10).grid(row=12, column=4)
        tk.Entry(root, textvariable=self._uge5, justify='right', width=10).grid(row=12, column=5)
        tk.Entry(root, textvariable=self._uge6, justify='right', width=10).grid(row=12, column=6)

        frame = tk.Frame()
        tk.Entry(frame, textvariable=self._pga, justify='right', width=4).pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self._pgb, justify='right', width=4).pack(side=tk.LEFT)
        frame.grid(row=13, column=3)

        tk.Entry(root, textvariable=self._hu1, justify='right', width=10).grid(row=14, column=1)
        tk.Entry(root, textvariable=self._hu2, justify='right', width=10).grid(row=14, column=2)
        tk.Entry(root, textvariable=self._hu3, justify='right', width=10).grid(row=14, column=3)
        tk.Entry(root, textvariable=self._hu4, justify='right', width=10).grid(row=14, column=4)
        tk.Entry(root, textvariable=self._hu5, justify='right', width=10).grid(row=14, column=5)
        tk.Entry(root, textvariable=self._hu6, justify='right', width=10).grid(row=14, column=6)

        tk.Entry(root, textvariable=self._dk1, justify='right', width=10).grid(row=15, column=1)
        tk.Entry(root, textvariable=self._dk2, justify='right', width=10).grid(row=15, column=2)
        tk.Entry(root, textvariable=self._dk3, justify='right', width=10).grid(row=15, column=3)
        tk.Entry(root, textvariable=self._dk4, justify='right', width=10).grid(row=15, column=4)
        tk.Entry(root, textvariable=self._dk5, justify='right', width=10).grid(row=15, column=5)
        tk.Entry(root, textvariable=self._dk6, justify='right', width=10).grid(row=15, column=6)

        tk.Entry(root, textvariable=self._syge, justify='right', width=10).grid(row=16, column=1)

        # Buttons
        tk.Button(root, text='Forrige dag', command=self.prev_day).grid(row=0, column=2)
        tk.Button(root, text='Næste dag', command=self.next_day).grid(row=0, column=3)
        tk.Button(root, text='Nulstil togt', command=self.reset).grid(row=0, column=6)
        tk.Button(root, text='Udfyld resten', command=self.reset).grid(row=17, column=5)
        tk.Button(root, text='Eksporter dag', command=self.reset).grid(row=17, column=6)

    def prev_day(self):
        pass

    def next_day(self):
        pass

    def reset(self):
        pass

    def update(self, model):
        # set date
        d = model.selected_date
        date_text = f'{d.year}/{str(d.month).zfill(2)}/{str(d.day).zfill(2)}'
        self._date.set(date_text)
        self._skifte1.set(model.skifte1)
        self._skifte2.set(model.skifte2)
        self._skifte3.set(model.skifte3)
        self._skifte4.set(model.skifte4)
        self._skifte5.set(model.skifte5)
        self._skifte6.set(model.skifte6)

class Model():

    def __init__(self):
        self.selected_date = datetime.now()
        self.skifte1 = 1
        self.skifte2 = 2
        self.skifte3 = 3
        self.skifte4 = 1
        self.skifte5 = 2
        self.skifte6 = 3


if __name__=='__main__':
    root = tk.Tk()
    root.title('Georg Stage Søvagt - version 0.1')
    gui = Gui(root)
    model = Model()
    gui.update(model)
    tk.mainloop()
