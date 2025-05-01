import argparse
import inspect
import providers
import plotters
import strategies
from models import CurrencyData
from datetime import datetime, timedelta
import csv

def fetch(args) -> None:
    provider = providers_[args.provider](args.currency)
    data: CurrencyData = provider.current()
    
    writer = csv.writer(args.output)
    writer.writerow([args.currency, data.time, data.value])

    print(f"[✔] Stored rate: {data.value} HUF/{args.currency} on {data.time.strftime('%Y-%m-%d')}")

def recommend(args) -> None:
    provider = providers_[args.provider](args.currency)
    history = provider.history(datetime.today()-timedelta(args.days), datetime.today())
    strategy = strategies_[args.strategy](history)
    
    strategy.show()

def plot(args) -> None:
    provider = providers_[args.provider](args.currency)
    history = provider.history(datetime.today()-timedelta(args.days), datetime.today())
    plotter = plotters_[args.plotter](history)
    
    plotter.show()


def list_(args) -> None:
    def _list(tolist: dict):
        for name, module in tolist.items():
            print(f"\t{name}:")
            print(f"\t\t{module.__doc__}")
        
    print("Exchange Rate Providers:")
    _list(providers_)
        
    print("strategies:")
    _list(strategies_)
            
    print("Plotters:")
    _list(plotters_)

actions = {
    "fetch": fetch,
    "recommend": recommend,
    "plot": plot,
    "list": list_
}

providers_ = dict(inspect.getmembers(providers, inspect.isclass))

strategies_   = dict(inspect.getmembers(strategies,   inspect.isclass))

plotters_  = dict(inspect.getmembers(plotters,  inspect.isclass))


def main() -> None:
    parser = argparse.ArgumentParser(
                        prog='Exchange Rate Tracker')

    parser.add_argument('--output', 
                        type=argparse.FileType(mode='a'), 
                        default="rates.csv",
                        help="Select a file where to save fetched data")

    parser.add_argument('--provider', 
                        type=str, 
                        choices=providers_.keys(), 
                        default="CIB",
                        help="Select an exchange rate source")

    parser.add_argument('--currency', 
                        type=str, 
                        default="EUR",
                        metavar="CODE",
                        help="Select a currency.")

    parser.add_argument('--strategy', 
                        type=str, 
                        choices=strategies_.keys(),
                        default="MovingAverage",
                        help="Select what to recommend based on")

    parser.add_argument('--days', 
                        type=int, 
                        default=7,
                        help="Days to look back for strategies")

    parser.add_argument('--plotter', 
                        type=str, 
                        choices=plotters_.keys(), 
                        default="MovingAverage",
                        help="Select what to show when plotting")

    parser.add_argument("action",
                        type=str,
                        choices=actions.keys(),
                        help="""Select what to do:
                        fetch: get the current value of selected currency
                        recommend: get a trading strategy recommendation based on the last --days values
                        plot: show a graph about the currency
                        list: list available modules""")

    args = parser.parse_args()
    
    actions[args.action](args)

if __name__ == "__main__":
    main()