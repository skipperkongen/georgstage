import logging

from georgstage.model import GeorgStage, Vagt, Opgave, AutoFiller
from georgstage.view import View

logger = logging.getLogger()

class Controller(object):
    """docstring for Controller."""

    def __init__(self):
        self.model = GeorgStage([])
        self.view = View(self)

    def main(self):
        logger.info('In main of controller')
        self.view.main()

    def new_plan(self):
        logger.info('New plan')

    def create_date(self, dt):
        logger.info(f'Creating date: {dt} ({type(dt)})')
        datoer = self.model.get_datoer()
        # Check that date is new date
        if dt in datoer:
            return False
        else:
            self.model[dt] = []
            return True

    def change_date(self):
        logger.info('Changing day')

    def persist_view(self, dt):
        logger.info('Persisting view')
        # translate dt and export_vars to vagter
        export_vars = self.view.export_vars()
        vagter = [
            Vagt(dato=dt, vagt_tid=vagt_tid, gast=int(gast), opgave=opgave)
            for (opgave, vagt_tid), gast in export_vars
            if gast.isdigit()
        ]
        self.model[dt] = vagter

    def get_vagter(self, dt):
        logger.info('Getting vagter for date')
        vagter = self.model[dt]
        return vagter

    def get_datoer(self):
        logger.info('Getting datoer')
        return self.model.get_datoer()

    def open_file(self, filepath):
        logger.info(f'loading file: {filepath}')
        gs = GeorgStage.load(filepath)
        self.model = gs

    def save_file(self, filepath):
        logger.info(f'Saving file: {filepath}')
        try:
            self.model.save(filepath)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def fill_day(self):
        logger.info('Fill day clicked')

    def show_stats(self):
        logger.info('Show stats clicked')

    def pick_date(self):
        logger.info('Pick day')
