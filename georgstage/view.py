from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from tkcalendar import Calendar

from georgstage import Opgave


class View(tk.Tk):
    """docstring for View."""

    PAD = 20
    WIDTH = 10
    LABELS = [
        (Opgave.VAGTHAVENDE_ELEV, 'Vagthavende elev'),
        (Opgave.ORDONNANS, 'Ordonnans'),
        (Opgave.UDKIG, 'Udkig'),
        (Opgave.BJAERGEMAERS, 'Bjærgemærs'),
        (Opgave.RORGAENGER, 'Rorgænger'),
        (Opgave.UDSAETNINGSGAST_A, 'Udsætningsgast A'),
        (Opgave.UDSAETNINGSGAST_B, 'Udsætningsgast B'),
        (Opgave.UDSAETNINGSGAST_C,'Udsætningsgast C'),
        (Opgave.UDSAETNINGSGAST_D,'Udsætningsgast D'),
        (Opgave.UDSAETNINGSGAST_E,'Udsætningsgast E'),
        ((Opgave.PEJLEGAST_A, Opgave.PEJLEGAST_B), 'Pejlegast A/B'),
        (Opgave.DAEKSELEV_I_KABYS, 'Dækselev i kabys'),
        (Opgave.HU, 'HU'),
        (Opgave.INAKTIV, 'Fraværende')
    ]
    START_TIDER = [0, 4, 8, 12, 16, 20]
    TIDSPUNKTER = ['00 - 04', '04 - 08', '08 - 12', '12 - 16', '16 - 20', '20 - 24']
    ROWS = len(LABELS)
    COLS = 6

    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller
        self.title('Georg Stage vagtplanlægger')
        self._vars = {}
        self._make_main_frame()
        self._make_menu()
        self._make_labels()
        self._make_entries()
        self._make_buttons()
        print([k for k in self._vars.keys()])

    def main(self):
        print('In main of view ')
        self.mainloop()


    def _make_main_frame(self):
        self.main_frm = ttk.Frame(self)
        self.main_frm.pack(padx=self.PAD, pady=self.PAD, side=tk.TOP)

    def _make_var(self, key):
        return self._vars.setdefault(key, tk.StringVar())

    def _make_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Filer", menu=file_menu)
        file_menu.add_command(label="Ny plan", command=self.controller.new_plan)
        file_menu.add_command(label="Åben", command=self._on_open)
        file_menu.add_command(label="Gem som", command=self._on_save_as)

        function_menu = tk.Menu(menu)
        menu.add_cascade(label="Funktioner", menu=function_menu)
        function_menu.add_command(label="Udfyld resten automatisk", command=self.controller.fill_day)

    def _make_labels(self):
        tk.Label(self.main_frm, text='Dato (YYYY/MM/DD)').grid(row=0, column=0, sticky=tk.E)
        tk.Label(self.main_frm, text='Skifte').grid(row=1, column=0, sticky=tk.E)
        tk.Label(self.main_frm, text='Vagt').grid(row=2, column=0, sticky=tk.E)
        tk.Label(self.main_frm, text='').grid(row=3, column=0, sticky=tk.E)
        for i, (_, label_text) in enumerate(self.LABELS):
            tk.Label(self.main_frm, text=label_text).grid(row=i+4, column=0, sticky=tk.E)
        for i, tidspunkt in enumerate(self.TIDSPUNKTER):
            tk.Label(self.main_frm, text=tidspunkt, width=self.WIDTH).grid(row=2, column=i+1, sticky=tk.E)

    def _make_entries(self):

        # Dato
        def is_date(str):
            try:
                datetime.strptime(str, '%Y/%m/%d')
                print('Date ok: ', str)
                return True
            except:
                print('Date NOT ok', str)
                return False
        ttk.Entry(
            self.main_frm,
            justify='center',
            textvariable=self._make_var('DATO'),
            width=self.WIDTH
        ).grid(row=0, column=1, sticky=tk.E)

        # skifter
        def is_skifte_or_empty(str):
            return str == '' or str.isdigit() and int(str) in [1,2,3]
        vcmd = (self.register(is_skifte_or_empty), '%P')
        for i in range(self.COLS):
            tidspunkt = self.START_TIDER[i]
            ttk.Entry(
                self.main_frm,
                justify='right',
                validate='key',
                validatecommand=vcmd,
                textvariable=self._make_var(f'SKIFTE_{tidspunkt}'),
                width=self.WIDTH
            ).grid(row=1, column=i+1, sticky=tk.E)

        # vagter, except pejlegast
        def is_gast_or_empty(str):
            print('is_gast received:', str)
            return str == '' or str.isdigit() and 0 < int(str) <= 60
        vcmd = (self.register(is_gast_or_empty), '%P')
        for i, (opgave, label_text) in enumerate(self.LABELS):
            if opgave == (Opgave.PEJLEGAST_A, Opgave.PEJLEGAST_B):
                # Pejlegase entries
                pejlegast_frame = ttk.Frame(self.main_frm)
                ttk.Entry(
                    pejlegast_frame,
                    validate='key',
                    validatecommand=vcmd,
                    textvariable=self._make_var(Opgave.PEJLEGAST_A.name),
                    justify='right',
                    width=4
                ).pack(side=tk.LEFT)
                ttk.Entry(
                    pejlegast_frame,
                    validate='key',
                    validatecommand=vcmd,
                    textvariable=self._make_var(Opgave.PEJLEGAST_B.name),
                    justify='right',
                    width=4
                ).pack(side=tk.LEFT)
                pejlegast_frame.grid(row=14, column=4)
            elif opgave == Opgave.DAEKSELEV_I_KABYS:
                for j in range (3):
                    start_tid = self.START_TIDER[j+2]
                    ent = ttk.Entry(
                        self.main_frm,
                        validate='key',
                        validatecommand=vcmd,
                        justify='right',
                        textvariable=self._make_var(f'{opgave.name}_{start_tid}'),
                        width = self.WIDTH
                    ).grid(row=i+4, column=j+3, sticky=tk.E)
            else:
                for j in range(self.COLS):
                    start_tid = self.START_TIDER[j]
                    ent = ttk.Entry(
                        self.main_frm,
                        validate='key',
                        validatecommand=vcmd,
                        justify='right',
                        textvariable=self._make_var(f'{opgave.name}_{start_tid}'),
                        width = self.WIDTH
                    ).grid(row=i+4, column=j+1, sticky=tk.E)



        #tk.Entry(pejlegast_frame, textvariable=tk.StringVar(), justify='right', width=4).pack(side=tk.LEFT)
        #tk.Entry(pejlegast_frame, textvariable=tk.StringVar(), justify='right', width=4).pack(side=tk.LEFT)

    def _make_buttons(self):
        self.btn_dato = ttk.Button(
            self.main_frm,
            text='Skift dato',
            command=self._on_button_push
        )
        self.btn_dato.grid(row=0, column=2, sticky=tk.E)

    def _is_date(self, str):
        try:
            datetime.strptime(str, '%Y/%m/%d')
            return True
        except:
            return False


    def _on_button_push(self):
        #print('Button pushed')
        value = self._vars['DATO'].get()
        if self._is_date(value):
            # save state of currently active date (if )
            pass
        else:
            messagebox.showwarning(title='Ugyldig dato', message='Den dato du har tastet er ugyldig. Benyt venligst formatet YYYY/MM/DD.')

    def _on_open(self):
        filename = filedialog.askopenfilename()
        self.controller.open_file(filename)

    def _on_save_as(self):
        filename = filedialog.asksaveasfilename()
        self.controller.save_file(filename)
