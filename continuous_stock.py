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
  ticker_dictionary ={
     "Tesla Inc":{"tick":"TSLA"},
     "General Motors Company" : {"tick":"GM"},
     "Ford":{"tick":"F"},
  }
  answer_dict = ticker_dictionary[company]
  ticker = answer_dict["tick"]
  return ticker

def init_csv_file(file_path):
    df_empty = pd.DataFrame(
        columns=["Company", "Ticker", "Longitude", "Time", "Price"]
    )
    df_empty.to_csv(file_path, index=False)

async def get_stock_price(ticker:str):
  logger.info("Calling get_stock_price for {ticker}}")
  stock_api_url =f"https://query1.finance.yahoo.com/v7/finance/options/{ticker}"
  logger.info(f" Calling fetch_from_url for {stock_api_url}")
  result = await fetch_from_url(stock_api_url,"json")
  logger.info(f"Data for {ticker}:{result.data}")
  price = result.data["optionChain"]["result"][0]["quote"]["regularMarketPrice"]
 # stock = yf.Ticker(ticker) # Get the stock data
 # price = stock.history(period="1d").tail(1)["Close"][0] # Get the closing price
  #price = randint(132, 148) 
  return price

async def update_csv_stock():
    """Update the CSV file with the latest stocks information."""
    logger.info("Calling update_csv_stock")
    try:
        companys = ["Tesla Inc", "General Motors Company", "Ford"]
        update_interval = 60  # Update every 1 minute (60 seconds)
        total_runtime = 15 * 60  # Total runtime maximum of 15 minutes
        num_updates = 10  # Keep the most recent 10 readings
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")

        # Use a deque to store just the last, most recent 10 readings in order
        records_deque = deque(maxlen=num_updates)

        fp = Path(__file__).parent.joinpath("data").joinpath("mtcars_stock.csv")

        # Check if the file exists, if not, create it with only the column headings
        if not os.path.exists(fp):
            init_csv_file(fp)

        logger.info(f"Initialized csv file at {fp}")

        for _ in range(num_updates):  # To get num_updates readings
            for company in companys:
                ticker  = lookup_ticker(company)
                price = await get_stock_price(ticker)
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
                new_record = {
                    "Company": company,
                    "Ticker": ticker,
                    "Time": time_now,
                    "Price": price,
                }
                records_deque.append(new_record)

            # Use the deque to make a DataFrame
            df = pd.DataFrame(records_deque)

            # Save the DataFrame to the CSV file, deleting its contents before writing
            df.to_csv(fp, index=False, mode="w")
            logger.info(f"Saving Stocks price to {fp}")

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_stock: {e}")





