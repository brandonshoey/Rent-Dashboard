import pandas as pd
import numpy as np
import datetime

# Localize a timeframe for analysis
start = np.datetime64("2009-12-31")
end = np.datetime64(datetime.datetime.today().date())

# Importing the data
df = pd.read_csv("appData/appData.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
df = df.loc[(df["Date"] > start)]
df = df.loc[(df["Date"] < end)]

# Set up the markets
def getMarkets():
    markets = df["MarketName"].unique().tolist()
    markets.append("All")
    return markets

# Extract data from markets
def getMarketData(market):
    if market == "All":
        data = df.copy()
        data = data.groupby("Date").agg({"RentGrowth": "mean",
                                         "AvailableSF": "sum"})
        data = data.reset_index()
        return data[["Date", "AvailableSF", "RentGrowth"]]
    else:
        data = df.copy()
        data = data.loc[(df["MarketName"] == market)]
        return data[["Date", "AvailableSF", "RentGrowth"]]