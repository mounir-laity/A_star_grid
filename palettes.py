# -*- encoding: utf-8 -*-
from enum import Enum

# pattern : [fg_color, bg_color, wall_color, start_color, end_color, path_color, explored_color, palette number]
class Palettes(Enum):
    """This represents the possible color palettes possibilities for the A star application."""

    DEFAULT = [
        "#D2D4C8",
        "#8B2635",
        "#2E3532",
        "#E0E2DB",
        "#D3EFBD",
        "dark green",
        "pink",
        0,
    ]
    STEEL = [
        "#EDF2F4",
        "#8D99AE",
        "#2B2D42",
        "#E0E2DB",
        "#D3EFBD",
        "#D90429",
        "#F68D99",
        1,
    ]
    ENERGY = [
        "#EDF5E1",
        "#5CDB95",
        "#05386B",
        "#E0E2DB",
        "#D3EFBD",
        "#4987AB",
        "#DEF3CE",
        2,
    ]
