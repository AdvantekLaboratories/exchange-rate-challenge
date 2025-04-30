import argparse

def get_parser_args():
    parser = argparse.ArgumentParser(description="Currency Exchange Rate Fetcher and Recommendation Tool")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand: 'fetch'
    fetch_parser = subparsers.add_parser("fetch", help="Fetch and display today's EUR/HUF exchange rate")

    # Subcommand: 'recommend'
    recommend_parser = subparsers.add_parser("recommend", help="Calculate the trading recommendation based on the 7-day moving average")
    recommend_parser.add_argument(
        "--plot", action="store_true", help="Enable plot of historical rates vs moving average"
    )

    return parser.parse_args()