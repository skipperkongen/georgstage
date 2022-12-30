from georgstage.model import Opgave, Vagt
from georgstage.autofill import N_GASTS, VAGT_TIDER, FillResult, get_counts, get_skifte_for_gast


def autofill(model, skifter=[1, 2, 3, 1, 2, 3]):

    datestr = str(model.get_current_dato())
    day_vagter = model[datestr]
    other_vagter = list(model.get_vagter(before=datestr))
    lookup = get_counts(day_vagter + other_vagter)

    return FillResult(status=1, vagter=day_vagter)