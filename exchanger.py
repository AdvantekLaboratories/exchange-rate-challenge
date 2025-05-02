#!/usr/bin/env python3
"""
Advantek Labs Exchange Rate Tracker
A simple command-line tool for tracking EUR/HUF exchange rates and providing trading recommendations.
"""

import argparse
import csv
import datetime
import os
import statistics
import sys
from typing import List, Dict, Tuple, Optional

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


class ExchangeRateTracker:
    """Handles fetching, storing, and analyzing EUR/HUF exchange rates."""
    
    def __init__(self, csv_file: str = 'rates.csv'):
        """Initialize the tracker with the path to the CSV file."""
        self.csv_file = csv_file
        self.ensure_csv_exists()
    
    def ensure_csv_exists(self) -> None:
        """Create the CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['date', 'rate'])
    
    def fetch_current_rate(self) -> Tuple[datetime.date, float]:
        """Fetch the current EUR/HUF exchange rate from a public source."""
        try:
            # Using the European Central Bank's exchange rate data
            url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            # Find the HUF rate in the XML
            huf_rate_elem = soup.find('Cube', currency='HUF')
            
            if not huf_rate_elem:
                raise ValueError("Could not find HUF rate in the XML data")
            
            rate = float(huf_rate_elem['rate'])
            today = datetime.date.today()
            
            return today, rate
        
        except (requests.RequestException, ValueError) as e:
            # Fallback to another source if the first one fails
            try:
                # Fallback to the Hungarian National Bank's website
                url = "https://www.mnb.hu/en/arfolyamok"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                # Find the EUR/HUF rate (this selector might need adjustment)
                rate_elem = soup.select_one("table.exchange-rates tr:contains('EUR') td:nth-child(3)")
                
                if not rate_elem:
                    raise ValueError("Could not find EUR/HUF rate on the MNB website")
                
                # Clean and convert the rate to float
                rate_text = rate_elem.text.strip().replace(',', '.')
                rate = float(rate_text)
                today = datetime.date.today()
                
                return today, rate
            
            except (requests.RequestException, ValueError) as e:
                print(f"[❌] Error fetching exchange rate: {e}")
                sys.exit(1)
    
    def store_rate(self, date: datetime.date, rate: float) -> None:
        """Store the exchange rate for the given date in the CSV file."""
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date.isoformat(), rate])
    
    def load_historical_rates(self) -> List[Dict[str, str]]:
        """Load historical exchange rates from the CSV file."""
        rates = []
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                rates = list(reader)
            
            # Convert rates to float for calculations
            for entry in rates:
                entry['rate'] = float(entry['rate'])
            
            return rates
        except FileNotFoundError:
            print(f"[❌] Error: Could not find {self.csv_file}")
            sys.exit(1)
    
    def calculate_moving_average(self, days: int = 7) -> Optional[float]:
        """Calculate the moving average for the specified number of days."""
        rates = self.load_historical_rates()
        
        if len(rates) < days:
            print(f"[⚠️] Warning: Not enough data for {days}-day moving average. Need at least {days} days of data.")
            return None
        
        # Get the last 'days' rates
        recent_rates = [entry['rate'] for entry in rates[-days:]]
        return statistics.mean(recent_rates)
    
    def generate_recommendation(self) -> Tuple[float, float, str]:
        """Generate a trading recommendation based on moving average crossover strategy."""
        rates = self.load_historical_rates()
        
        if not rates:
            print("[❌] Error: No historical data available. Run 'fetch' command first.")
            sys.exit(1)
        
        ma_7day = self.calculate_moving_average(7)
        
        if ma_7day is None:
            print("[⚠️] Warning: Using available data for recommendation.")
            ma_7day = statistics.mean([entry['rate'] for entry in rates])
        
        current_rate = rates[-1]['rate']
        
        # Simple trading signal: Buy EUR if today's rate is higher than MA, sell otherwise
        # (This is a simplified strategy for demonstration purposes)
        if current_rate > ma_7day:
            recommendation = "BUY EUR"
        else:
            recommendation = "SELL EUR"
        
        return ma_7day, current_rate, recommendation
    
    def plot_historical_rates(self, output_file: str = 'exchange_rates.png') -> None:
        """Create a plot of historical rates with moving average."""
        rates = self.load_historical_rates()
        
        if len(rates) < 2:
            print("[❌] Error: Not enough data to create a plot.")
            return
        
        # Create DataFrame for plotting
        df = pd.DataFrame(rates)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Calculate 7-day moving average if we have enough data
        if len(df) >= 7:
            df['ma_7day'] = df['rate'].rolling(window=7).mean()
            
            # Plot
            plt.figure(figsize=(10, 6))
            plt.plot(df.index, df['rate'], label='EUR/HUF Rate', marker='o')
            plt.plot(df.index, df['ma_7day'], label='7-day Moving Average', linestyle='--')
            plt.title('EUR/HUF Exchange Rate History')
            plt.xlabel('Date')
            plt.ylabel('Exchange Rate (HUF/EUR)')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save the plot
            plt.savefig(output_file)
            print(f"[✔] Plot saved as {output_file}")
        else:
            # Simple plot without moving average
            plt.figure(figsize=(10, 6))
            plt.plot(df.index, df['rate'], label='EUR/HUF Rate', marker='o')
            plt.title('EUR/HUF Exchange Rate History')
            plt.xlabel('Date')
            plt.ylabel('Exchange Rate (HUF/EUR)')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save the plot
            plt.savefig(output_file)
            print(f"[✔] Plot saved as {output_file}")


def setup_argparse() -> argparse.ArgumentParser:
    """Set up command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description='EUR/HUF Exchange Rate Tracker and Recommendation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch and store today\'s exchange rate')
    
    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Analyze rates and provide a trading recommendation')
    
    # Plot command (bonus)
    plot_parser = subparsers.add_parser('plot', help='Create a plot of historical exchange rates')
    plot_parser.add_argument('--output', '-o', help='Output filename for the plot', default='exchange_rates.png')
    
    return parser


def main():
    """Main entry point for the application."""
    parser = setup_argparse()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tracker = ExchangeRateTracker()
    
    if args.command == 'fetch':
        date, rate = tracker.fetch_current_rate()
        tracker.store_rate(date, rate)
        print(f"[✔] Stored rate: {rate:.2f} HUF/EUR on {date.isoformat()}")
    
    elif args.command == 'recommend':
        ma_7day, current_rate, recommendation = tracker.generate_recommendation()
        print(f"📊 7-day Moving Average: {ma_7day:.2f}")
        print(f"📈 Today's Rate: {current_rate:.2f}")
        print(f"💡 Recommendation: {recommendation}")
    
    elif args.command == 'plot':
        tracker.plot_historical_rates(args.output)


if __name__ == "__main__":
    main()