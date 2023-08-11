from shiny import ui

def get_fruits_inputs():
    return ui.panel_sidebar(
        ui.h2("Want to know Fruits Nutrition"),
        ui.tags.hr(),
        ui.input_select(
        id="FRUIT_SELECT_INPUT",
        label="Choose a favorite fruit",
        choices=["mango","banana","apple"],
        selected="mango",
        ),
        ui.tags.hr(),
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )