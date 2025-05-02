import pandas as pd
from datetime import timedelta, datetime
import os
import requests
import matplotlib.pyplot as plt
import argparse
import sys



os.chdir(os.path.dirname(os.path.abspath(__file__)))

start_date = (datetime.now() - timedelta(days=16)).date()
end_date = datetime.now().date()

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def fetch():
    #History rates
    df = pd.DataFrame()
    try:
        for single_date in daterange(start_date, end_date):
            try:
                dfs = pd.read_html(f'https://www.xe.com/currencytables/?from=HUF&date={single_date.strftime("%Y-%m-%d")}')[0]
                dfs['Date'] = single_date.strftime("%Y-%m-%d")
                df = pd.concat([df, dfs], ignore_index=True)
            except Exception as e:
                print(f"Error fetching data for {single_date}: {e}")
        df_eur = df.loc[df['Currency'] == 'EUR']
        df_eur_filtered = df_eur[['HUF per unit', 'Date']]

    #Today's rate
        try:
            url = f'https://api.frankfurter.app/latest?from=EUR&to=HUF'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            rate = data['rates']['HUF']
            date = data['date']
        except Exception as e:
            print(f"Error fetching today's rate: {e}")
            rate = None
            date = None
    
        #Today's rate might be already in the file, so we check if it is already there
        if date not in df_eur_filtered['Date'].values:
            today_data = pd.DataFrame({'HUF per unit': [rate], 'Date': [date]})
            df_eur_filtered = pd.concat([df_eur_filtered, today_data], ignore_index=True)
        else:
            print("The latest data is already in the file.")
        df_eur_filtered.to_csv('rates.csv', index=False)

        last_row = df_eur_filtered.iloc[-1]
        print(f"[✔] Stored rate: {last_row['HUF per unit']:.2f} HUF/EUR on {last_row['Date']}")
    
    except Exception as e:
        print(f"[✘] Failed to fetch data: {e}")

def recommend():
    try:
        df = pd.read_csv('rates.csv')
        df = df.sort_values('Date')
        df['SMA7'] = df['HUF per unit'].rolling(window=7).mean()

        if len(df) < 7:
            print("Not enough data to make a recommendation. Minimum 7 days required.")
            return
        
        last_value = df['HUF per unit'].iloc[-1]
        sma7_today = df['SMA7'].iloc[-1] 

        if last_value > sma7_today:
            signal = "SELL"
        elif last_value < sma7_today:
            signal = "BUY"
        else:
            signal = "HOLD"

        print(f"📈 Last value: {last_value:.2f}")
        print(f"📊 SMA7:       {sma7_today:.2f}")
        print(f"💡 Recommendation: {signal}")
    except FileNotFoundError:
        print("rates.csv cannot be found. Fetch data first.")
        return

   
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['HUF per unit'], label='HUF per EUR', marker='o')
    plt.plot(df['Date'], df['SMA7'], label='SMA 7', linestyle='--', color='orange')

    plt.title("HUF per EUR with SMA7")
    plt.xlabel("Date")
    plt.ylabel("HUF per EUR")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and analyze HUF/EUR exchange rate.")
    parser.add_argument("action", choices=["fetch", "recommend"], help="Choose an action to perform.")
    args = parser.parse_args()

    if args.action == "fetch":
        fetch()
    elif args.action == "recommend":
        recommend()
