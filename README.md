# Exchange Rate Tracker

## Installation

```bash
pip install -r requirements.txt
```

## Usage

See: `python exchanger.py --help`

## Development

### Adding a Provider

To add a new exchange rate provider, create a new file in the `providers` folder and define a class inside it that represents the provider. It’s recommended to name the file and the class inside it identically. The class constructor should accept a `str` type currency code, which it will later return values for. The class must also include a `current(self) -> CurrencyData` method that returns the current exchange rate, and a `history(self, from_: datetime.datetime, to: datetime.datetime) -> List[CurrencyData]` method that returns exchange rates for the specified time interval. Additionally, the class name should be added to the `__all__` variable in the `providers/__init__.py` file, and a `from .<file> import <class>` line must be included. After this, the program will recognize and be able to use the new provider.

### Adding a Strategy

To add a new strategy, create a new file in the `strategies` folder and define a class inside it that represents the strategy. It’s recommended to name the file and the class identically. The class constructor should accept a `List[CurrencyData]` type list of currency values. The class must also include a `show(self) -> None` method that analyzes the data received in the constructor, makes a recommendation based on it, and prints it to the console. Additionally, the class name should be added to the `__all__` variable in the `strategies/__init__.py` file, and a `from .<file> import <class>` line must be included. After this, the program will recognize and be able to use the new strategy.

### Adding a Plotter

To add a new plotter, create a new file in the `plotters` folder and define a class inside it that represents the plotter. It’s recommended to name the file and the class identically. The class constructor should accept a `List[CurrencyData]` type list of currency values. The class must also include a `show(self) -> None` method that visualizes the data received in the constructor. Additionally, the class name should be added to the `__all__` variable in the `plotters/__init__.py` file, and a `from .<file> import <class>` line must be included. After this, the program will recognize and be able to use the new plotter.
