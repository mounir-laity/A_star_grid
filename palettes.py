from enum import Enum

# pattern : [fg_color, bg_color, wall_color, start_color, end_color, path_color, explored_color]
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
    STEEL = [
        "#EDF2F4",
        "#8D99AE",
        "#2B2D42",
        "#E0E2DB",
        "#D3EFBD",
        "#D90429",
        "#F68D99",
    ]
    # https://coolors.co/edf5e1-5cdb95-05386b-e0e2db-def3ce-4987ab-379683
    ENERGY = [
        "#EDF5E1",
        "#5CDB95",
        "#05386B",
        "#E0E2DB",
        "#D3EFBD",
        "#4987AB",
        "#DEF3CE",
    ]
