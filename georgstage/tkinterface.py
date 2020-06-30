from datetime import datetime

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class Gui():

    def __init__(self, root):
        self.root = root
        # Date selection
        tk.Label(root, text='Valgte dag').grid(row=0, column=0)
        tk.Label(root, text='xx/xx/xx', name='date_label', background='gray').grid(row=0, column=1)
        tk.Button(root, text='Forrige dag', name='prev_btn').grid(row=0, column=2)
        tk.Button(root, text='Næste dag', name='next_btn').grid(row=0, column=3)

        # Reset
        tk.Button(root, text='Nulstil togt', name='reset_btn').grid(row=0, column=6)

        # Skifte
        tk.Label(root, text='Skifte').grid(row=2, column=0)
        for i in range(6):
            field_name = f'skifte{i}_field'
            tk.Entry(root, text='', name=field_name).grid(row=2, column=i+1)



    def update(self, model):
        # set date
        d = model.selected_date
        date_text = f'{d.year}/{str(d.month).zfill(2)}/{str(d.day).zfill(2)}'
        self.root.nametowidget('date_label')['text'] = date_text

        # set skifter
        for i in range(6):
            w = self.root.nametowidget(f'skifte{i}_field')
            w['text'] = 'fpo'


class Model():

    def __init__(self):
        self.selected_date = datetime.now()
        self.shift = 0


if __name__=='__main__':
    root = tk.Tk()
    gui = Gui(root)
    model = Model()
    gui.update(model)
    tk.mainloop()
