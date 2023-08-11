# Standard Library
import asyncio
from datetime import datetime
from pathlib import Path
import os
from random import randint

# External Packages
import pandas as pd
from collections import deque
# Local Imports
from fetch import fetch_from_url
from util_logger import setup_logger

# Set up a file logger
logger, log_filename = setup_logger(__file__)

def init_csv_fruit(file_path):
    df_empty = pd.DataFrame(
        columns=["name","calories","fat","sugar","carbohydrates","protein"]
    )
    df_empty.to_csv(file_path, index=False)

async def get_fruit_nutrition(fruit:str):
    logger.info(f"Calling  get fruit nutrition for {fruit}")
    fruit_api_url = f"https://www.fruityvice.com/api/fruit/{fruit}"
    logger.info(f"fetching from url for {fruit_api_url}")
    result = await fetch_from_url(fruit_api_url,"json")
    logger.info(f"Data for {fruit}:{result.data}")
    nutri_value = result.data["nutritions"]
    logger.info(f"Data on nutri_value:{nutri_value}")
    return nutri_value

async def update_csv_fruit():
    logger.info(f"update update_csv_fruit")
    try:
        fruits = ["mango","banana","apple"]
        num_updates = 10  # Keep the most recent 10 readings
        update_interval = 60  # Update every 1 minute (60 seconds)
          # Use a deque to store just the last, most recent 10 readings in order
        records_deque = deque(maxlen=num_updates)

        fp = Path(__file__).parent.joinpath("data").joinpath("fruits_nutri.csv")

        # Check if the file exists, if not, create it with only the column headings
        if not os.path.exists(fp):
            init_csv_fruit(fp)

        logger.info(f"Initialized csv file at {fp}")
        for _ in range(num_updates):  # To get num_updates readings
            for fruit in fruits:
                name = fruit
                nutri_value = await get_fruit_nutrition(fruit)
                new_record ={
                    "name" : name,
                    "calories":nutri_value['calories'],
                    "fat": nutri_value['fat'],
                    "sugar": nutri_value['sugar'],
                    "carbohydrates": nutri_value['carbohydrates'],
                    "protein": nutri_value['protein']
               }
                records_deque.append(new_record)

            # Use the deque to make a DataFrame
            df = pd.DataFrame(records_deque)

            # Save the DataFrame to the CSV file, deleting its contents before writing
            df.to_csv(fp, index=False, mode="w")
            logger.info(f"Saving Fruits nutrition to {fp}")

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_fruit: {e}")
