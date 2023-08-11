from shiny import ui
from shinywidgets import output_widget

def get_fruits_outputs():
    return ui.panel_main(
        ui.h2("Main Panel with Continuous and Reactive Output"),
        ui.tags.hr(),
        ui.tags.section(
        ui.h3("Continuous Updates (Fruit API)"),
            ui.tags.br(),
            ui.tags.hr(),
            ui.output_text("fruits_nutri_string"),
            ui.tags.br(),
            ui.output_ui("fruits_nutri_table"),
            ui.tags.br(),
            ui.h3("Filtered Fruits: Nutri Chart"),
            output_widget("fruits_nutri_chart"),
            ui.tags.hr(),
        ),
    )