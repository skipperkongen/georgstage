import logging

from dateutil.parser import parse

from georgstage.model import GeorgStage, Vagt, Opgave, AutoFiller
from georgstage.view import View, NO_DATE


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
        logger.info(f'Creating date: {dt}')
        datoer = self.model.get_datoer()
        # Check that date is new date
        if dt in datoer:
            return False
        else:
            self.model[dt] = []
            return True

    def change_date(self):
        logger.info(f'Changing date')
        old_date = self.view.get_previous_date()
        try:
            dt = parse(old_date)
            self.persist_view(dt)
        except:
            logger.info('Not persisting, because no previous date')


    def persist_view(self, dt=None):
        logger.info('Persisting view')
        # translate dt and export_vars to vagter
        if self.view.get_current_date() == NO_DATE:
            logger.info('Nothing to persist')
            return
        export_vars = self.view.get_vars()
        if dt is None:
            dt = parse(self.view.get_current_date())
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
        self.persist_view()
        self.model.save(filepath)

    def fill_day(self):
        logger.info('Fill day clicked')
        self.persist_view()

    def show_stats(self):
        logger.info('Show stats clicked')
        self.persist_view()

    def pick_date(self):
        logger.info('Pick day')
