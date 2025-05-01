import requests
import sys
from datetime import datetime
import pandas as pd
import os

from plots import plot_data
from parser import get_parser_args

API_URL = "https://api.frankfurter.dev/v1"
BASE_CURRENCY = "EUR"
TARGET_CURRENCY = "HUF"
CSV_FILE = "rates.csv"

def get_start_date():
    """Gets the start date from the CSV file or returns a default date."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, parse_dates=['date'])
        return df['date'].max().strftime('%Y-%m-%d')
    return "2025-03-04"

START_DATE = get_start_date()
END_DATE = datetime.today().strftime("%Y-%m-%d")

def fetch():
    """Fetches and stores EUR/HUF exchange rate from START_DATE to END_DATE.
    START_DATE is the last date in the CSV file or a default date.
    If START_DATE == END_DATE, it fetches today's rate.
    """
    try:
        response =  requests.get(f"{API_URL}/{START_DATE}..{END_DATE}", params={"from": BASE_CURRENCY, "to": TARGET_CURRENCY })
        data = response.json()
        data = data["rates"]

        save_to_csv(data)

        today_date, today_rate = data.popitem()

        print(f"[✔] Stored rate: {today_rate} HUF/EUR on {today_date}")
    except requests.RequestException as e:
        print(f"[✖] Network error: {e}")
        sys.exit(1)
    except KeyError:
        print("[✖] Unexpected API response format.")
        sys.exit(1)

def save_to_csv(data):
    """Appends the fetched data to a CSV file using pandas."""
    new_rows = []
    for date, rates in data.items():
        rate = rates[TARGET_CURRENCY]

        current_date = pd.to_datetime(date)
        if current_date > pd.Timestamp(START_DATE):
            new_rows.append({"date": current_date, "rate": rate})

    if new_rows:
        new_data_df = pd.DataFrame(new_rows)
        new_data_df.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)
        print(f"📁 Appended {len(new_rows)} new rows to {CSV_FILE}")
    else:
        print("📁 No new data to append.")
        
def calculate_signal(plot=False):
    """Calculates 7-day moving average and generates recommendation."""

    try:
        insufficient_data = False

        df = pd.read_csv(CSV_FILE)
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values("date", inplace=True)
        df['7ma'] = df['rate'].rolling(window=7).mean()

        today = df.iloc[-1]
        if len(df) < 7:
            insufficient_data = True
            print("[!] Not enough data to calculate 7-day moving average.")
            print(f"📈 Today's Rate: {today['rate']}")
            print("💡 Recommendation: HOLD (Insufficient data)")
            return

        ma = today['7ma']
        rate = today['rate']
        signal = "BUY EUR" if rate > ma else "SELL EUR" if rate < ma else "HOLD"

        print(f"📊 7-day Moving Average: {ma:.2f}")
        print(f"📈 Today's Rate: {rate:.2f}")
        print(f"💡 Recommendation: {signal}")

        if plot and not insufficient_data:
            plot_data(df)

    except FileNotFoundError:
        print(f"[✖] CSV file '{CSV_FILE}' not found. Run 'fetch' command first.")
        sys.exit(1)
    except Exception as e:
        print(f"[✖] An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    # Parse arguments
    args = get_parser_args()

    # Perform actions based on arguments
    if args.command == "fetch":
        fetch()
    elif args.command == "recommend":
        calculate_signal(plot=args.plot)
    

if __name__ == "__main__":
    main()
    