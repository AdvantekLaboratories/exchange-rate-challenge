import matplotlib.pyplot as plt

def plot_data(df):
    """Plot historical rates and 7-day moving average using matplotlib."""
    plt.figure(figsize=(10, 6))
    
    # Plot historical rates
    plt.plot(df['date'], df['rate'], label='Historical Rates', color='b', marker='o', linestyle='-', markersize=4)
    
    # Plot 7-day moving average
    plt.plot(df['date'], df['7ma'], label='7-day Moving Average', color='r', linestyle='--')
    
    # Set plot labels and title
    plt.title(f"EUR/HUF Exchange Rates vs 7-day Moving Average")
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate (HUF/EUR)')
    plt.legend()
    
    # Rotate date labels for better readability
    plt.xticks(rotation=45)
    
    # Display the plot
    plt.tight_layout()
    plt.show()
