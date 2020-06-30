from tkinter import *

class Model():

    def __init__(self):
        self.day=1

    def __str__(self):
        return f'day = {self.day}'

class View():
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.plan=Plan(master)
        self.sidepanel=SidePanel(master)

    def update(self, model):
        pass


class Plan():
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.label = tk.Label(self.frame, text='yomomma')


class SidePanel():
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.spinbox = tk.Spinbox(self.frame, from_=1, to=365)
        self.spinbox.pack(side="top",fill=tk.BOTH)

class Controller():
    def __init__(self):
        self.root = tk.Tk()
        self.model=Model()
        self.view=View(self.root)
        self.view.sidepanel.spinbox.bind("<ButtonRelease-1>",self.set_day)

    def run(self):
        self.root.title("Tkinter MVC example")
        self.root.mainloop()

    def set_day(self, event):
        #pdb.set_trace()
        self.model.day = int(event.widget.get())
        print(self.model, event.widget.get())
        self.view.update(self.model)



if __name__ == '__main__':
    c = Controller()
    c.run()
