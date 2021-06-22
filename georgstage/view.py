from datetime import datetime, date, timedelta
import logging
import pdb
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import traceback

from dateutil.parser import parse

from georgstage.model import Opgave

logger = logging.getLogger()


NO_DATE = '-'

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
        self._make_vars()
        self._make_main_frame()
        self._make_menu()
        self._make_labels()
        self._make_dropdown()
        self._make_entries()
        #pdb.set_trace()

    def main(self):
        logger.info('In main of view ')
        self.mainloop()

    def update(self):
        logger.info('Updating')
        self._reset_vars()
        # refresh date list
        logger.info('Updating date list')
        datoer = self.controller.get_datoer()
        format_date = lambda d: d.isoformat() if type(d) == datetime.date else str(d)
        date_list = sorted([format_date(d) for d in datoer])
        self._dropdown['menu'].delete(0, 'end')
        for dato in date_list:
            self._dropdown['menu'].add_command(label=dato, command=tk._setit(self.current_date, dato))

        logger.info('Resetting and updating variables')
        if self.current_date.get() == NO_DATE:
            self.current_date.set(date_list[-1])
        vagter = self.controller.get_vagter(self.current_date.get())
        for vagt in vagter:
            key = (vagt.opgave, vagt.vagt_tid)
            #pdb.set_trace()
            self._vars[key].set(str(vagt.gast))

    def get_vars(self):
        return [(k,v.get()) for k,v in self._vars.items()]

    def get_previous_date(self):
        return self.previous_date.get()

    def get_current_date(self):
        return self.current_date.get()

    def _make_vars(self):
        self._vars = {}
        self.current_date = tk.StringVar(self)
        self.current_date.trace('w', self._on_date_selected)
        self.previous_date = tk.StringVar(self)

    def _reset_vars(self):
        logger.info('Resetting variables')
        for var in self._vars.values():
            var.set('')

    def _make_main_frame(self):
        self.main_frm = tk.Frame(self, bg='White')
        self.main_frm.pack(padx=self.PAD, pady=self.PAD, side=tk.TOP)

    def _make_var(self, key):
        return self._vars.setdefault(key, tk.StringVar(self))

    def _make_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Filer", menu=file_menu)
        file_menu.add_command(label="Åben vagtplan", command=self._on_open)
        file_menu.add_command(label="Gem vagtplan", command=self._on_save_as)

        rediger_menu = tk.Menu(menu)
        menu.add_cascade(label="Rediger", menu=rediger_menu)
        rediger_menu.add_command(label="Opret ny dato", command=self._on_create_date)
        rediger_menu.add_command(label="Nulstil valgte dato", command=self.controller.reset_date)
        rediger_menu.add_command(label="Slet valgte dato", command=self.controller.delete_date)

        function_menu = tk.Menu(menu)
        menu.add_cascade(label="Funktioner", menu=function_menu)
        function_menu.add_command(label="Udfyld resten automatisk", command=self.controller.autofill)
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
            try:
                valid_date = parse(self.current_date.get())
                return str == '' or (str.isdigit() and 0 < int(str) <= 60)
            except:
                messagebox.showwarning(title='Ingen dato valgt', message='Før du kan indtaste gaster, skal du vælge en dato fra dropdown eller oprette en ny dato under "Rediger" -> "Opret dato"')
                return False
        vcmd = (self.register(is_gast_or_empty), '%P')
        for i, (opgave, label_text) in enumerate(self.LABELS):
            if opgave == (Opgave.PEJLEGAST_A, Opgave.PEJLEGAST_B):
                # Pejlegase entries
                pejlegast_frame = tk.Frame(self.main_frm)
                tk.Entry(
                    pejlegast_frame,
                    validate='key',
                    validatecommand=vcmd,
                    textvariable=self._make_var((Opgave.PEJLEGAST_A, 16)),
                    justify='right',
                    width=4
                ).pack(side=tk.LEFT)
                tk.Entry(
                    pejlegast_frame,
                    validate='key',
                    validatecommand=vcmd,
                    textvariable=self._make_var((Opgave.PEJLEGAST_B, 16)),
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
                        textvariable=self._make_var((opgave, start_tid)),
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
                        textvariable=self._make_var((opgave, start_tid)),
                        width = self.WIDTH
                    ).grid(row=i+2, column=j+1, sticky=tk.E)
            for i in range(self.COLS):
                start_tid = self.START_TIDER[i]
                tk.Entry(
                    self.main_frm,
                    justify='right',
                    validate='key',
                    validatecommand=vcmd,
                    textvariable=self._make_var((Opgave.UDE, start_tid)),
                    width=self.WIDTH
                ).grid(row=len(self.LABELS)+4, column=i+1, sticky=tk.E)



        #tk.Entry(pejlegast_frame, textvariable=tk.StringVar(), justify='right', width=4).pack(side=tk.LEFT)
        #tk.Entry(pejlegast_frame, textvariable=tk.StringVar(), justify='right', width=4).pack(side=tk.LEFT)

    def _make_dropdown(self):
        date_list = [NO_DATE]
        self.current_date.set(date_list[0])
        self._dropdown = tk.OptionMenu(
            self.main_frm,
            self.current_date,
            *date_list
        )
        self._dropdown.grid(row=0, column=0, sticky=tk.E)

    def show_can_not_fill(self):
        messagebox.showwarning("Udfyld resten",f"Vagtplanen kan ikke udfyldes.")

    def show_ask_skifte(self, vagt_tid=0):
        skifte = simpledialog.askinteger(
            "Angiv skifte", f"Hvilket skifte har vagt fra klokken {vagt_tid}",
            parent=self.main_frm
        )
        return skifte

    def _on_help(self):
        messagebox.showinfo(title='Hjælp', message='Dette programmet er udviklet af Pimin Konstantin Kefaloukos. Læs mere på hjemmesiden https://github.com/skipperkongen/georgstage')

    def _on_date_selected(self, a, b, c):
        if self.current_date.get() == NO_DATE: return
        logger.info (f'Dato changed {self.previous_date.get()} -> {self.current_date.get()}')
        try:
            self.controller.change_date()
            self.update()
            self.previous_date.set(self.current_date.get())
        except Exception as e:
            # previous date was not a date
            logger.exception(e)

    def show_confirm_delete_date(self, dt):
        return messagebox.askokcancel("Slet dato",f"Er du sikker på at du vil slette den datoen {dt.isoformat()}?")

    def show_confirm_reset_date(self, dt):
        return messagebox.askokcancel("Slet dato",f"Er du sikker på at du vil nulstille datoen {dt.isoformat()}?")

    def show_could_not_delete_date(self):
        messagebox.showwarning("Slet dato",f"Kunne ikke slette dato")

    def show_could_not_reset_date(self):
        messagebox.showwarning("Slet dato",f"Kunne ikke nulstille dato")

    def _on_create_date(self):
        try:
            datoer = self.controller.get_datoer()
            if len(datoer) > 0:
                max_dt = max(datoer)
                initial_value = max_dt + timedelta(days=1)
            else:
                initial_value = date.today()
            input_dato = simpledialog.askstring(
                "Opret dato", "Indtast dato som skal oprettes (YYYY-MM-DD)",
                parent=self.main_frm,
                initialvalue=initial_value.isoformat()
            )
            dt = parse(input_dato).date()
            created = self.controller.create_date(dt)
            if created:
                self.current_date.set(input_dato)
                self.update()
            else:
                messagebox.showwarning(title='Ugyldig dato', message='Dato findes i forvejen')

        except Exception as e:
            logger.exception(e)
            messagebox.showwarning(title='Ugyldig dato', message='Ugyldigt datoformat. Benyt venligst formatet YYYY-MM-DD, f.eks. 1935-4-24.')

    def _on_open(self):
        logger.info('Opening file')
        try:
            filename = filedialog.askopenfilename(filetypes=[('Georg Stage Vagtplan', '*.gsv')])
            self.controller.open_file(filename)
            self.update()
        except Exception as e:
            logger.exception(e)
            messagebox.showerror(title='Fejl', message='Der opstod en fejl under forsøget på at åbne din vagtplan. Check filformatet og prøv igen.')

    def _on_save_as(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension='gsv', filetypes=[('Georg Stage Vagtplan', '*.gsv')])
            if filename is not None:
                self.controller.save_file(filename)
                messagebox.showinfo(title='Fil gemt', message='Din vagtplan er blevet gemt')
        except Exception as e:
            logger.exception(e)
            messagebox.showerror(title='Fejl', message='Der opstod en fejl under forsøget på at gemme din vagtplan')
