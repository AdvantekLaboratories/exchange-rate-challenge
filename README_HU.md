# Valuta Árfolyam Követő

## Telepítés

```bash
pip install -r requirements.txt
```

## Használat

Lásd: `python exchanger.py --help`

## Fejlesztés

### Szolgáltató hozzáadása

Új árfolyam szolgáltatóhoz fel kell venni egy egy új fájlt a `providers` mappába, és ebbe kell beletenni a szolgáltatót reprezentáló osztályt. Érdemes azonos néven elnevezni a fájt és a benne lévő osztályt. Az osztály konstruktorának fogadnia kell egy `str` típusú valuta kódot, későbbiekben ennek az értékeit adja vissza. Az osztálynak tartalmaznia kell továbbá egy `current(self) -> CurrencyData` metódust, ami a jelenlegi árfolyammal tér vissza és egy `history(self, from_: datetime.datetime, to: datetime.datetime) -> List[CurrencyData]` metódust, ami a kiválasztott intervallumon megadja az árfolyamokat. Ezen kívül a `providers/__init__.py` fájl `__all__` változóba fel kell venni a nevét, valamint egy `from .<file> import <class>` sort is. Ezután már a program látja a szolgáltatót, és képes használni is.

### Stratégia hozzáadása

Új stratégiához fel kell venni egy egy új fájlt a `strategies` mappába, és ebbe kell beletenni a stratégiát reprezentáló osztályt. Érdemes azonos néven elnevezni a fájt és a benne lévő osztályt. Az osztály konstruktorának fogadnia kell egy `List[CurrencyData]` típusú valuta érték tömböt. Az osztálynak tartalmaznia kell továbbá egy `show(self) -> None` metódust, ami a konstruktorban kapott adatok alapján következtet egy javaslatot, majd megjeleníti a konzolon. Ezen kívül a `strategies/__init__.py` fájl `__all__` változóba fel kell venni a nevét, valamint egy `from .<file> import <class>` sort is. Ezután már a program látja a stratégiát, és képes használni is.

### Plotter hozzáadása

Új plotterhez fel kell venni egy egy új fájlt a `plotters` mappába, és ebbe kell beletenni a plottert reprezentáló osztályt. Érdemes azonos néven elnevezni a fájt és a benne lévő osztályt. Az osztály konstruktorának fogadnia kell egy `List[CurrencyData]` típusú valuta érték tömböt. Az osztálynak tartalmaznia kell továbbá egy `show(self) -> None` metódust, ami a konstruktorban kapott adatokat megjeleníti. Ezen kívül a `plotters/__init__.py` fájl `__all__` változóba fel kell venni a nevét, valamint egy `from .<file> import <class>` sort is. Ezután már a program látja a plotters, és képes használni is.
