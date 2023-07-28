# Standard Library
import asyncio
from datetime import datetime
from pathlib import Path
import os
from random import randint

# External Packages
import pandas as pd
from collections import deque
from dotenv import load_dotenv

# import Yahoo Finance Api
import yfinance as yf

# Local Imports
from fetch import fetch_from_url
from util_logger import setup_logger

# Set up a file logger
logger, log_filename = setup_logger(__file__)

def lookup_ticker(company):
  return "F"

async def get_stock_price(ticker):
  logger.info("Calling get_stock_price for {ticker}}")
 # stock = yf.Ticker(ticker) # Get the stock data
 # price = stock.history(period="1d").tail(1)["Close"][0] # Get the closing price
  price = randint(132, 148) 
  return price

async def update_csv_stock():
    """Update the CSV file with the latest stock prices."""
    logger.info("Calling update_csv_stock")

    try:
        # Add column headers when creating the empty CSV file for stock prices
        file_path = Path(__file__).parent.joinpath("data").joinpath("mtcars_stock.csv")
        if not os.path.exists(file_path):
            df_empty = pd.DataFrame(
                columns=["Company", "Ticker", "Time", "Price"]
            ).copy()
            df_empty.to_csv(file_path, index=False)
    
        # Stub: Create a simple DataFrame with static data
        df_data = pd.DataFrame({
            "Company": ["Tesla Inc", "General Motors Company", "Ford"],
            "Ticker": ["TSLA", "GM", "F"],
            "Time": ["2023-07-25 09:00:00", "2023-07-25 09:01:00","2023-07-25 09:01:00"],
            "Price": [700.0, 60.0,120.0]
        })

        # Save stock prices to the CSV file
        logger.info(f"Saving stock prices to {file_path}")
        df_data.to_csv(file_path, index=False)

    except Exception as e:
        logger.error(f"An error occurred in update_csv_stock: {e}")



