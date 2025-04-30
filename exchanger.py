import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import pandas as pd
import os

API_URL = "https://api.frankfurter.dev/v1"
BASE_CURRENCY = "EUR"
TARGET_CURRENCY = "HUF"
CSV_FILE = "rates.csv"

def get_start_date():
    """Get the start date from the CSV file or return a default date."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, parse_dates=['date'])
        return df['date'].max().strftime('%Y-%m-%d')
    else:
        return 

START_DATE = get_start_date() or "2025-03-04"
END_DATE = datetime.now().strftime("%Y-%m-%d")

def fetch_today_rate():
    """Fetch today's EUR to HUF rate using Frankfurter API."""
    try:
        response = requests.get(f"{API_URL}/latest", params={"from": BASE_CURRENCY, "to": TARGET_CURRENCY})
        response.raise_for_status()
        data = response.json()
        rate = data["rates"][TARGET_CURRENCY]
        date = data["date"]
        print(f"[✔] Stored rate: {rate:.2f} HUF/EUR on {date}")
    except requests.RequestException as e:
        print(f"[✖] Network error: {e}")
        sys.exit(1)
    except KeyError:
        print("[✖] Unexpected API response format.")
        sys.exit(1)

def fetch_historical_rate():
    """Fetch historical EUR to HUF rate based on a date range using Frankfurter API.
    If the rates.csv file contains data from the past, it will not be fetched from the API."""
    try:
        response = requests.get(f"{API_URL}/{START_DATE}..{END_DATE}", params={"from": BASE_CURRENCY, "to": TARGET_CURRENCY })
        data = response.json()
        return data["rates"]
    except requests.RequestException as e:
        print(f"[✖] Network error: {e}")
        sys.exit(1)
    except KeyError:
        print("[✖] Unexpected API response format.")
        sys.exit(1)

def save_to_csv(data):
    """Append the fetched data to a CSV file using pandas."""
    
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
    
def calculate_signal():
    """Calculate 7-day moving average and generate recommendation."""

    df = pd.read_csv(CSV_FILE)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values("date", inplace=True)
    df['7ma'] = df['rate'].rolling(window=7).mean()

    today = df.iloc[-1]
    if len(df) < 7:
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

def main():
    historical = fetch_historical_rate()
    save_to_csv(historical)

    if len(sys.argv) != 2:
        print("Usage: python exchanger.py [fetch|recommend]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "fetch":
        fetch_today_rate()
    elif command == "recommend":
        calculate_signal()
    else:
        print("[✖] Unknown command. Use 'fetch' or 'recommend'.")

if __name__ == "__main__":
    main()
    