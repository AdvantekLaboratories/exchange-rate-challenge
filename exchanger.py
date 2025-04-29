import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import argparse

# Relative Strength Index indicator
def rsi(data: pd.Series, window: int = 14):
    # Calculate daily price changes
    delta = data.diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    
    # Calculate relative strength
    rs = avg_gain / avg_loss
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# Download historical data from Yahoo Finance API
def download_historical():
    import yfinance as yf

    # Download the data
    data = yf.download("EURHUF=X")

    # Get the relevant columns
    rates = list(data["Close"]["EURHUF=X"])
    dates = list(data.index)

    # Create a new dataframe with the required format
    for d in dates:
        d = d.date().strftime("%Y-%m-%d")
    df = pd.DataFrame({'Date': dates, 'Rate': rates})
    df = df.set_index("Date")

    # Save the dataframe
    df.to_csv("rates.csv")

# Function for loading the local data
def load_data() -> pd.DataFrame:
    # Open rates.csv if found
    try:
        df = pd.read_csv("rates.csv", parse_dates=["Date"], index_col="Date")

    # Create an empty dataframe if not found
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Rate"])
        df = df.set_index("Date")

    return df

def fetch():
    URL = "https://www.investing.com/currencies/eur-huf"

    req = requests.get(URL)
    # If the request was succesful
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")

        # Get the current price text from the website
        res = soup.find("div", {"class" : "text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]"})
        rate = float(res.text)

        # Today's date in the required format
        date_str = datetime.now().strftime("%Y-%m-%d")

        df = load_data()
        # Add the fetched data to the dataframe
        df.loc[date_str] = rate
        # Save the dataframe
        df.to_csv("rates.csv")

        print(f"[✔] Stored rate: {rate} HUF/EUR on {date_str}")
    else:
        print("[x] Rate fetching failed")

def recommend():
    df = load_data()

    # Get today's RSI value
    rsi_today = round(rsi(df["Rate"]).iloc[-1], 2)
    print(f"📊 14-day RSI: {rsi_today}")

    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"📈 Today's Rate: {df.loc[date_str]['Rate']}")

    # Basic trading strategy
    # Buy when the default 14-day RSI is above 50
    # Sell otherwise
    if rsi_today > 50:
        print(f"💡 Recommendation: BUY EUR")
    else:
        print(f"💡 Recommendation: SELL EUR")

def plot():
    import matplotlib.pyplot as plt

    df = load_data()
    df.plot(xlabel="Date", ylabel="Rate")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="Action that the program should perform (download/fetch/recommend/plot)")
    
    args = parser.parse_args()

    if args.action == "download":
        download_historical()
    elif args.action == "fetch":
        fetch()
    elif args.action == "recommend":
        recommend()
    elif args.action == "plot":
        plot()