from georgstage.model import GeorgStage, Vagt, Opgave, AutoFiller
from georgstage.view import View

class Controller(object):
    """docstring for Controller."""

    def __init__(self):
        self.model = GeorgStage([])
        self.view = View(self)

    def main(self):
        print('In main of controller')
        self.view.main()

    def new_plan(self):
        print('New plan')

    def create_date(self, dt):
        print(f'Creating date: {dt} ({type(dt)})')
        datoer = self.model.get_datoer()
        # Check that date is new date
        if dt in datoer:
            return False
        else:
            self.model[dt] = []
            self.view.update(self.model.get_datoer(), dt, [])
            return True

    def change_date(self):
        print('Changing day')

    def open_file(self, filepath):
        print(f'loading file: {filepath}')
        try:
            gs = GeorgStage.load(filepath)
            self.model = gs
            return True
        except Exception as e:
            print(e)
            return False

    def save_file(self, filepath):
        print(f'Saving file: {filepath}')
        try:
            self.model.save(filepath)
            return True
        except Exception as e:
            print(e)
            return False

    def fill_day(self):
        print('Fill day clicked')

    def show_stats(self):
        print('Show stats clicked')

    def pick_date(self):
        print('Pick day')

if __name__ == '__main__':
    app = Controller()
    app.main()
