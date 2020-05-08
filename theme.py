from dataclasses import dataclass
from typing import List
import altair


@dataclass
class Font:
    family: str
    small: float
    regular: float
    large: float


@dataclass
class Palettes:
    main: List[str]
    sequential: List[str]


@dataclass
class Colors:
    background: str
    dark_text: str
    light_text: str
    grid: str


class AltairTheme:
    def __init__(self, name, font, colors, palettes):
        self.name = name
        self.font = font
        self.colors = colors
        self.palettes = palettes

    def legend(self):
        return {
            "legend": {
                "padding": 5,
                "labelFont": self.font.family,
                "labelFontSize": self.font.regular,
                #
                "symbolType": "circle",
                "symbolSize": 60,
                #
                "title": "",  # set it to no-title by default
                "titleFont": self.font.family,
                "titleFontSize": self.font.regular,
                "orient": "top-right",
                "fillColor": self.colors.background,
            },
        }

    def axis(self):
        return {
            "domain": True,
            "domainColor": self.colors.background,
            "domainWidth": 2,
            "offset": 5,
            #
            "grid": True,
            #
            "labelFont": self.font.family,
            "labelFontSize": self.font.small,
            "labelPadding": 10,
            "labelAngle": 0,
            #
            "tickColor": self.colors.dark_text,
            "tickSize": 7,
            "tickWidth": 2,
            #
            "titleFont": self.font.family,
            "titleFontSize": self.font.regular,
        }

    def __call__(self):
        return {
            "config": {
                "title": {
                    "anchor": "start",
                    "dy": -30,
                    "font": self.font.family,
                    "fontSize": self.font.large,
                    "fontColor": self.colors.dark_text,
                    "subtitlePadding": -20,
                    "subtitleFontSize": self.font.small,
                    "subtitleFontColor": self.colors.dark_text,
                },
                "range": {
                    "category": self.palettes.main,
                    "diverging": self.palettes.sequential,
                },
                **self.legend(),
                "axisX": {
                    **self.axis(),
                    "titleColor": self.colors.dark_text,
                    "titlePadding": 5,
                    "title": "X Axis Title (units)",
                },
                "axisY": {
                    **self.axis(),
                    "title": "Y Axis Title (units)",
                    "titlePadding": 0,
                    "titleAlign": "left",
                    "titleAngle": 0,  # horizontal
                    "titleY": -20,  # move it up
                },
            }
        }

    def register(self):
        altair.themes.register(self.name, self)
