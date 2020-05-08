from pathlib import Path
import pandas
import altair
from theme import Font, Colors, Palettes, AltairTheme


def add_css_import_to_style(html_text, css_import):
    """Include a CSS import into an existing HTML string"""
    return html_text.replace("<style>", "<style>\n{}\n".format(css_import))


def add_import_to_html_file(html_file, css_import):
    """Include a CSS import into an existing HTML file"""
    html_text = Path(html_file).read_text()
    Path(html_file).write_text(
        add_css_import_to_style(html_text, css_import=css_import,)
    )


# Theme based on the IBM Plex typeface and a color palette from Tableau
base = 16
ibm_plex_sans_condensed_import = "@import url('https://fonts.googleapis.com/css?family=IBM+Plex+Sans+Condensed:400');"
font = Font("IBM Plex Sans Condensed", 0.889 * base, base, 1.424 * base)
colors = Colors("#ffffff", "#000000", "#000000", "#DCDCDC")
palettes = Palettes(
    [
        "#4e79a7",
        "#f28e2b",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc948",
        "#b07aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ac",
    ],
    ["#cfe8f3", "#a2d4ec", "#73bfe2", "#46abdb", "#1696d2", "#12719e",],
)

ibm_theme = AltairTheme("ibm", font, colors, palettes)
ibm_theme.register()

life_expectancies = pandas.read_csv("./life_expectancies.csv")
average_life_expectancies = (
    life_expectancies.assign(temp=lambda df: df["age"] * df["death_rate"])
    .groupby(by="percentile")
    .agg(value=("temp", "sum"))
)

selected_percentiles = ["0-5%", "25-30%", "50-55%", "95-100%"]
years_added = (
    average_life_expectancies.loc["95-100%"]["value"]
    - average_life_expectancies.loc["0-5%"]["value"]
)

html_file = "life_expectancy.html"

with altair.themes.enable(ibm_theme.name):
    chart = (
        altair.Chart(
            life_expectancies.query("percentile in @selected_percentiles").assign(
                percentage_of_survival=lambda df: df["survival_rate"] * 100
            ),
            width=600,
            height=400,
        )
        .mark_line()
        .encode(
            x=altair.X("age", title="Age (years)"),
            y=altair.Y(
                "percentage_of_survival", title="Percentage of the group surviving"
            ),
            color=altair.Color("percentile", title=["Percentile of", "income"]),
        )
        .properties(
            title={
                "text": "Life expectancy increases with income",
                "subtitle": f"The wealthiest live, on average, {int(years_added)} years longer than the least wealthy group.",
            }
        )
    )

    chart.save(
        html_file, vegalite_version="4.8.1", vega_version="5", vegaembed_version="6",
    )
    add_import_to_html_file(html_file, ibm_plex_sans_condensed_import)
