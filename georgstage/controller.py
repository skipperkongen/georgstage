from georgstage.model import Model
from georgstage.view import View

class Controller(object):
    """docstring for Controller."""

    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def main(self):
        print('In main of controller')
        self.view.main()

    def on_incr(self):
        print(f'Incr clicked')
        result = self.model.incr()
        self.view.value_var.set(result)

    def open_file(self, filepath):
        print(f'loading file: {filepath}')

    def save_file(self, filepath):
        print(f'Saving file: {filepath}')

    def fill_day(self):
        print('Fill day clicked')

if __name__ == '__main__':
    app = Controller()
    app.main()
