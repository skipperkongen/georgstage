from datetime import datetime
from dateutil.parser import parse
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk

from tkcalendar import Calendar

from georgstage import Opgave


class View(tk.Tk):
    """docstring for View."""

    PAD = 30
    WIDTH = 12
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
        (Opgave.DAEKSELEV_I_KABYS, 'Dækselev i kabys')
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
        self._make_dropdown()
        self._make_entries()
        print([k for k in self._vars.keys()])

    def main(self):
        print('In main of view ')
        self.mainloop()


    def _make_main_frame(self):
        self.main_frm = tk.Frame(self, bg='White')
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

        rediger_menu = tk.Menu(menu)
        menu.add_cascade(label="Rediger", menu=rediger_menu)
        rediger_menu.add_command(label="Opret ny dato", command=self._on_create_date)
        rediger_menu.add_command(label="Slet valgte dato", command=self._on_delete_date)

        function_menu = tk.Menu(menu)
        menu.add_cascade(label="Funktioner", menu=function_menu)
        function_menu.add_command(label="Udfyld resten automatisk", command=self.controller.fill_day)
        function_menu.add_command(label="Vis statistik", command=self.controller.show_stats)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Hjælp", menu=help_menu)
        help_menu.add_command(label="Om Georg Stage vagtplanlægger", command=self._on_help)

    def _make_labels(self):

        #tk.Label(self.main_frm, bg='White', text='Tidspunkt').grid(row=1, column=0, sticky=tk.E)
        tk.Label(self.main_frm, bg='White', text='').grid(row=2, column=0, sticky=tk.E)
        for i, (_, label_text) in enumerate(self.LABELS):
            tk.Label(self.main_frm, bg='White', text=label_text).grid(row=i+2, column=0, sticky=tk.E)
        for i, tidspunkt in enumerate(self.TIDSPUNKTER):
            tk.Label(self.main_frm, bg='White', text=tidspunkt, width=self.WIDTH).grid(row=1, column=i+1, sticky=tk.E)
        tk.Label(self.main_frm, bg='White', text='').grid(row=len(self.LABELS)+3, column=0, sticky=tk.E)
        tk.Label(self.main_frm, bg='White', text='Ude (f.eks. 1, 2, 3)').grid(row=len(self.LABELS)+4, column=0, sticky=tk.E)

    def _make_entries(self):

        # vagter, except pejlegast
        def is_gast_or_empty(str):
            valid_date = self._vars['DATO'].get() != '-'
            if not valid_date:
                messagebox.showwarning(title='Ingen dato valgt', message='Før du kan indtaste gaster, skal du vælge en dato fra dropdown eller oprette en ny dato under "Rediger" -> "Opret dato"')

            return valid_date and (str == '' or str.isdigit()) and 0 < int(str) <= 60
        vcmd = (self.register(is_gast_or_empty), '%P')
        for i, (opgave, label_text) in enumerate(self.LABELS):
            if opgave == (Opgave.PEJLEGAST_A, Opgave.PEJLEGAST_B):
                # Pejlegase entries
                pejlegast_frame = tk.Frame(self.main_frm)
                tk.Entry(
                    pejlegast_frame,
                    validate='key',
                    validatecommand=vcmd,
                    textvariable=self._make_var(Opgave.PEJLEGAST_A.name),
                    justify='right',
                    width=4
                ).pack(side=tk.LEFT)
                tk.Entry(
                    pejlegast_frame,
                    validate='key',
                    validatecommand=vcmd,
                    textvariable=self._make_var(Opgave.PEJLEGAST_B.name),
                    justify='right',
                    width=4
                ).pack(side=tk.LEFT)
                pejlegast_frame.grid(row=12, column=4)
            elif opgave == Opgave.DAEKSELEV_I_KABYS:
                for j in range (3):
                    start_tid = self.START_TIDER[j+2]
                    ent = tk.Entry(
                        self.main_frm,
                        validate='key',
                        validatecommand=vcmd,
                        justify='right',
                        textvariable=self._make_var(f'{opgave.name}_{start_tid}'),
                        width = self.WIDTH
                    ).grid(row=i+2, column=j+3, sticky=tk.E)
            else:
                for j in range(self.COLS):
                    start_tid = self.START_TIDER[j]
                    ent = tk.Entry(
                        self.main_frm,
                        validate='key',
                        validatecommand=vcmd,
                        justify='right',
                        textvariable=self._make_var(f'{opgave.name}_{start_tid}'),
                        width = self.WIDTH
                    ).grid(row=i+2, column=j+1, sticky=tk.E)
            for i in range(self.COLS):
                tidspunkt = self.START_TIDER[i]
                tk.Entry(
                    self.main_frm,
                    justify='right',
                    validate='key',
                    validatecommand=vcmd,
                    textvariable=self._make_var(f'UDE_{tidspunkt}'),
                    width=self.WIDTH
                ).grid(row=len(self.LABELS)+4, column=i+1, sticky=tk.E)



        #tk.Entry(pejlegast_frame, textvariable=tk.StringVar(), justify='right', width=4).pack(side=tk.LEFT)
        #tk.Entry(pejlegast_frame, textvariable=tk.StringVar(), justify='right', width=4).pack(side=tk.LEFT)

    def _make_dropdown(self):
        self.date_list = ['-']
        var = self._make_var('DATO')
        var.set(self.date_list[0])
        var.trace('w', self._on_date_selected)
        listbox = tk.OptionMenu(
            self.main_frm,
            var,
            *self.date_list
        ).grid(row=0, column=0, sticky=tk.E)

    def _on_help(self):
        messagebox.showinfo(title='Hjælp', message='Dette programmet er udviklet af Pimin Konstantin Kefaloukos. Læs mere på hjemmesiden https://github.com/skipperkongen/georgstage')

    def _on_date_selected(self, a, b, c):
        print ('Valgt dato:', self._vars['DATO'].get())

    def _on_delete_date(self):
        dato = self._vars['DATO'].get()
        if dato != '-':
            do_delete = messagebox.askokcancel("Slet dato",f"Er du sikker på at du vil slette datoen {dato}?")
            print(do_delete)
        else:
            messagebox.showwarning("Slet dato",f"Der er ikke valgt nogen dato")

    def _on_create_date(self):
        input_dato = simpledialog.askstring(
            "Opret dato", "Indtast dato som skal oprettes (YYYY-MM-DD)",
            parent=self.main_frm)
        try:
            dt = parse(input_dato).date()
            created = self.controller.create_date(dt)
            if not created:
                messagebox.showwarning(title='Ugyldig dato', message='Dato findes i forvejen')
        except Exception as e:
            messagebox.showwarning(title='Ugyldig dato', message='Ugyldigt datoformat. Benyt venligst formatet YYYY-MM-DD, f.eks. 1935-4-24.')

    def _on_open(self):
        filename = filedialog.askopenfilename()
        self.controller.open_file(filename)

    def _on_save_as(self):
        filename = filedialog.asksaveasfilename()
        self.controller.save_file(filename)
