# Standard Library
from pathlib import Path

# External Libraries
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
import plotly.express as px
from shiny import render, reactive
from shinywidgets import render_widget

#local imports
from fruits_get_basics import get_fruits_df
from util_logger import setup_logger

# Set up a global logger for this file
logger, logname = setup_logger(__name__)

# Declare our file path variables globally so they can be used in all the functions (like logger)
csv_fruits = Path(__file__).parent.joinpath("data").joinpath("fruits_nutri.csv")

def get_fruits_server_function(input, output, session):
   
    reactive_fruit = reactive.Value("mango")
    reactive_df = reactive.Value()
    original_df = get_fruits_df()
    total_count = len(original_df)

    @output
    @render_widget
    def fruits_nutri_chart():
        df = get_fruits_nutri_df()
        df_fruit = df[df["name"] == reactive_fruit.get()]
        logger.info(f"Rendering Nutri chart with {len(df_fruit)} dollars")
        plotly_express_plot = px.line(
            df_fruit, x="sugar", y="carbohydrates", color="calories", markers=True
        )
        plotly_express_plot.update_layout(title="Continuous Fruits Nutrition Values")
        return plotly_express_plot

    @reactive.Effect
    @reactive.event(input.FRUIT_SELECT_INPUT)
    def _():
        """Set two reactive values (the stocks and price df) when user changes company"""
        reactive_fruit.set(input.FRUIT_SELECT_INPUT())
        df = get_fruits_nutri_df()
        logger.info(f"init fruit nutri: {len(df)}")

    @reactive.file_reader(str(csv_fruits))
    def get_fruits_nutri_df():
        logger.info(f"Reading df from {csv_fruits} ")
        df=pd.read_csv(csv_fruits)
        logger.info(f"Reading df len {len(df)}")
        return df
    
    
    @output
    @render.text
    def fruits_nutri_string():
        """Return a string based on selected fruit."""
        logger.info("starting fruits_nutrition_string")
        selected = reactive_fruit.get()
        message = f"Nutrition value of {selected}."
        logger.info(f"{message}")
        return message
    
    @output
    @render.table
    def fruits_nutri_table():
        df = get_fruits_nutri_df()
        df_fruit = df[df["name"] == reactive_fruit.get()]
        logger.info(f"Rendering Nutrition table with {len(df_fruit)} rows")
        return df_fruit
    


    return[
        fruits_nutri_string,
        fruits_nutri_table,
        fruits_nutri_chart,
    ]