import datetime
from dateutil.parser import parse
import logging

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

    def delete_date(self):
        current_date = self.view.get_current_date()
        try:
            dt = parse(current_date).date()
            header = "Slet dato"
            text = f"Er du sikker på at du vil slette {dt.isoformat()}?"
            if self.view.ask_consent(header, text):
                del self.model[dt]
                self.view.update()
        except:
            self.view.show_warning("Fejl", "Kunne ikke slette dato")


    def reset_date(self):
        current_date = self.view.get_current_date()
        try:
            dt = parse(current_date).date()
            header = "Nulstil dato"
            text = f"Er du sikker på at du vil nulstille {dt.isoformat()}?"
            if self.view.ask_consent(header, text):
                self.model[dt] = []
                self.view.update()
        except:
            self.view.show_warning("Fejl", "Kunne ikke nulstille datoen")

    def guess_pejlegast_a(self, dt):
        yesterday = dt - datetime.timedelta(days=1)
        logger.info(f'{dt}, {yesterday}')
        logger.info(f'Inspecting vagter {yesterday}: {self.model[yesterday]}')
        for vagt in self.model[yesterday]:
            if vagt.opgave == Opgave.PEJLEGAST_B:
                logger.info(vagt)
                return Vagt(dato=dt, vagt_tid=16, gast=vagt.gast, opgave=Opgave.PEJLEGAST_A)


    def create_date(self, dt):
        logger.info(f'Creating date: {dt}')
        datoer = self.model.get_datoer()
        # Check that date is new date
        if dt in datoer:
            return False
        else:
            vagter = []
            # try to fill in pejlegast A as B from yesterday
            pejlegast_a = self.guess_pejlegast_a(dt)
            if pejlegast_a is not None:
                vagter.append(pejlegast_a)
            self.model[dt] = vagter
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

    def _guess_skifter(self, vagter):
        logger.info('Guessing skifter')
        guesses = [None,None,None,None,None,None]
        for vagt in vagter:
            skifte = 1 + vagt.gast // 20
            idx = vagt.vagt_tid // 4
            guesses[idx] = skifte
        return guesses


    def open_file(self):
        logger.info('Opening file')
        try:
            filepath = self.view.ask_open_file(filetypes=[('Georg Stage Vagtplan', '*.gsv')])
            logger.info(f'loading file: {filepath}')
            gs = GeorgStage.load(filepath)
            self.model = gs
            self.view.update()
        except Exception as e:
            logger.exception(e)
            self.view.show_warning('Fejl', 'Der opstod en fejl under forsøget på at åbne din vagtplan. Check filformatet og prøv igen.')


    def save_file_as(self):
        try:
            filepath = self.view.ask_save_file_as(defaultextension='gsv', filetypes=[('Georg Stage Vagtplan', '*.gsv')])
            if filepath is not None:
                logger.info(f'Saving file: {filepath}')
                self.persist_view()
                self.model.save(filepath)
                self.view.show_info('Fil gemt', 'Din vagtplan er blevet gemt')
        except Exception as e:
            logger.exception(e)
            self.view.show_warning('Fejl', 'Der opstod en fejl under forsøget på at gemme din vagtplan')


    def get_help(self):
        header = 'Hjælp'
        text = 'Dette programmet er udviklet af Pimin Konstantin Kefaloukos. Læs mere på hjemmesiden https://github.com/skipperkongen/georgstage'
        self.view.show_info(header, text)

    def get_vagter(self, dt):
        logger.info('Getting vagter for date')
        vagter = self.model[dt]
        return vagter

    def get_datoer(self):
        logger.info('Getting datoer')
        return self.model.get_datoer()

    def autofill(self):
        logger.info('Fill day clicked')
        try:
            dt = parse(self.view.get_current_date())
            self.persist_view()
            vagter = self.get_vagter(dt)
            skifter = self._guess_skifter(vagter)
            logger.info(f'Guesses: {skifter}')
            for i, skifte in enumerate(skifter):
                if skifte is None:
                    header = "Angiv skifte"
                    text = f"Hvilket skifte har vagt fra klokken {i*4}"
                    skifte = self.view.ask_number(header, text)
                    if skifte not in (1,2,3):
                        raise ValueError(f'Skifte {skifte} not one of 1, 2, 3')
                    skifter[i] = skifte
            logger.info(f'Skifter: {skifter}')
            fill_result = self.model.autofill(dt, skifter)
            logger.info(fill_result)
            if fill_result.status != 1:
                raise ValueError(f'Vagtplan not optimal')
            self.model[dt] = fill_result.vagter
            self.view.update()

        except Exception as e:
            logger.exception(e)
            self.view.show_warning("Fejl", "Vagtplanen kan ikke udfyldes automatisk")


    def show_stats(self):
        logger.info('Show stats clicked')
        self.view.show_info('Stats', 'Statistikvisning er ikke implementeret endnu')

    def pick_date(self):
        logger.info('Pick day')
