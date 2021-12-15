from enum import Enum

# pattern : fg_color, bg_color, wall_color, start_color, end_color, path_color, explored_color
class Palettes(Enum):
    DEFAULT = [
        "#D2D4C8",
        "#8B2635",
        "#2E3532",
        "#E0E2DB",
        "#D3EFBD",
        "dark green",
        "pink",
    ]
