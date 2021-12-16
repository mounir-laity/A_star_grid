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
    # https://coolors.co/2b2d42-8d99ae-edf2f4-ef233c-d90429
    VIVE_LA_FRANCE = [
        "#EDF2F4",
        "#2B2D42",
        "#2E3532",
        "#E0E2DB",
        "#D3EFBD",
        "dark green",
        "pink",
    ]
