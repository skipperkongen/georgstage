# Georg Stage Vagtplanlægger 0.0.1

> Hjælpeprogram til vagtplanlægning på Georg Stage

## Til brugere

Programmet kan installeres via pip:

```
pip install georgstage
```

### Eksempler

Start UI:

```
# TODO
```

Kode eksempler:

```python
import georgstage
```


## Fremtidigt arbejde

> Se https://trello.com/b/nId6IuH1/georg-stage  


## Til udviklere

### Sådan kører du tests

Ved hjælp af make:

```
make test
```

### Sådan publicerer du en ny version

Trin (kan måske forbedre):

1. Opdater version and download_url felter i setup.py
1. Kør git add + commit + push
1. Opret ny release på GitHub (check source-code link, skal matche download_url i setup.py)
1. Kør `python setup.py sdist`
1. Kør `twine upload dist/* --verbose` (hvis ej installet, kør `pip install twine` først)


## Gamle noter

Kør program:

```
python3 georgstage/interface.py
```


Noter:

```
3 skifter

20 gaster på hver

1-20: skifte 1
21-40: skifte 2
41-60: skifte 3

61-63: kokke elever

5'eren er ude

- indikere hvilke numre er "ude"/deaktiveret
- hvilket skifte har 8-12? 20-24?
- hvilket skifte har 12-16? 0-4?
- hvilket skifte har 16-20? 4-8?
- det skal være fair, så alle få alle poster lige mange gange
- 1 kvartermester til hver skifte
- [rotation] vagthavende elev, samme gast både morgen og aften, går på tur, dag for dag, også når skifterne får nye vagter.
- [rotation] pejlegast A/B, to gaster. Hvis 1,2 var sidst, så 2,3 næste gang, o.s.v.
- [rotation] pejlegast kun 16-20 vagten
- [rotation] Dækselev i kabys, kun 8-12 (morgenmad), 12-16 (frokost), 16-20 (aftensmad)
- i havn:

kontroller:
- i havn (hvornår ankomst og afgang?) eller til søs
```
