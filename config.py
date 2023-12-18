# Configs
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
RESIZABLE = False
FPS = 60
ROWS = 10
COLUMNS = 20

SOUND_OPTIONS = {
    "ACTIVE_BGM": True,
    "BGM_VOLUME": 0.1,
    "ACTIVE_SFX": True,
    "SFX_VOLUME": 0.5
}

ASSET_DATA = [
    {
        "name": "bgm",
        "type": "sounds",
        "path": "assets/bgm.mp3"
    },
    {
        "name": "game_over",
        "type": "sounds",
        "path": "assets/game_over.mp3"
    },
    {
        "name": "move",
        "type": "sounds",
        "path": "assets/move.mp3"
    },
    {
        "name": "land",
        "type": "sounds",
        "path": "assets/land.mp3"
    },
    {
        "name": "line_clear",
        "type": "sounds",
        "path": "assets/line_clear.mp3"
    },
    {
        "name": "full_clear",
        "type": "sounds",
        "path": "assets/full_clear.mp3"
    },
    {
        "name": "level_up",
        "type": "sounds",
        "path": "assets/next_level.mp3"
    },
    {
        "name": "tile",
        "type": "image",
        "path": "assets/tile.png"
    },
    {
        "name": "background",
        "type": "image",
        "path": "assets/background.png"
    },
    {
        "name": "font",
        "type": "font",
        "path": "assets/retro.ttf",
        "size": 16
    }
]

COLOR_DATA = {
    "ORANGE": (255, 128, 0),
    "DARK_BLUE": (64, 64, 255),
    "YELLOW": (255, 255, 0),
    "CYAN": (0, 255, 255),
    "LIGHT_GREEN": (0, 255, 128),
    "RED": (255, 0, 0),
    "MAGENTA": (255, 0, 255),
}

TETROMINO_DATA = {
    "I": {
        "positions": {
            "0": [(-2, 0), (-1, 0), ( 0, 0), ( 1, 0)],
            "1": [(-1, 2), (-1, 1), (-1, 0), (-1,-1)],
            "2": [(-2, 1), (-1, 1), ( 0, 1), ( 1, 1)],
            "3": [( 0, 2), ( 0, 1), ( 0, 0), ( 0,-1)]
        },
        "color": COLOR_DATA["CYAN"],
        "wall_kick": "W_K_2"
    },
    "J": {
        "positions": {
            "0": [(-2, 0), (-1, 0), ( 0, 0), (-2,-1)],
            "1": [(-1,-1), (-1, 0), (-1, 1), (-2, 1)],
            "2": [(-2, 0), (-1, 0), ( 0, 0), ( 0, 1)],
            "3": [(-1,-1), (-1, 0), (-1, 1), ( 0,-1)]
        },
        "color": COLOR_DATA["DARK_BLUE"],
        "wall_kick": "W_K_1"
    },
    "L": {
        "positions": {
            "0": [(-2, 0), (-1, 0), (0, 0), (0, -1)],
            "1": [(-1, 1), (-1, 0), (-1,-1), (-2,-1)],
            "2": [(-2, 0), (-1, 0), (0, 0), (-2, 1)],
            "3": [(-1, 1), (-1, 0), (-1,-1), (0, 1)]
        },
        "color": COLOR_DATA["ORANGE"],
        "wall_kick": "W_K_1"
    },
    "O": {
        "positions": {
            "0": [(0, -1), (0, 0), (-1, -1), (-1, 0)]
        },
        "color": COLOR_DATA["YELLOW"],
        "wall_kick": "W_K_0"
    },
    
    "S": {
        "positions": {
            "0": [(-1, 0), (0, 0), (0,-1), (1,-1)],
            "1": [( 0, 1), (0, 0), (-1, 0), (-1,-1)],
            "2": [(-1, 1), (0, 1), (0, 0), (1, 0)],
            "3": [( 1, 1), (1, 0), (0, 0), (0,-1)]
        },
        "color": COLOR_DATA["LIGHT_GREEN"],
        "wall_kick": "W_K_1"
    },
    "T": {
        "positions": {
            "0": [(-1, 0), (-2, 0), ( 0, 0), (-1, -1)],
            "1": [(-1, 0), (-1,-1), (-1, 1), (-2, 0)],
            "2": [(-1, 0), (-2, 0), ( 0, 0), (-1, 1)],
            "3": [(-1, 0), (-1,-1), (-1, 1), ( 0, 0)]
        },
        "color": COLOR_DATA["MAGENTA"],
        "wall_kick": "W_K_1"
    },
    "Z": {
        "positions":{
            "0": [(-1,-1), (-2,-1), (-1, 0), ( 0, 0)],
            "1": [(-1,-1), (-1, 0), (-2, 0), (-2, 1)],
            "2": [(-1, 0), (-2, 0), (-1, 1), ( 0, 1)],
            "3": [( 0,-1), ( 0, 0), (-1, 0), (-1, 1)]
        },
        "color": COLOR_DATA["RED"],
        "wall_kick": "W_K_1"
    }
}

# 0 -> 1 -> 2 -> 3 -> 0 counter-clockwise
# L = left, R = right
# TODO: addition in Y axis is inverted, fix this
WALL_KICK_DATA = {
    "W_K_0": {
        "0": {
            "L": [(0, 0)],
            "R": [(0, 0)]
        }
    },
    "W_K_1": {
        "0": {
            "L": [(0, 0), ( 1, 0), ( 1, -1), (0, 2), ( 1, 2)],
            "R": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
        },
        "1": {
            "L": [(0, 0), (-1, 0), (-1, -1), (0, -2), (-1, -2)],
            "R": [(0, 0), (-1, 0), (-1, -1), (0, -2), (-1, -2)]
        },
        "2": {
            "L": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
            "R": [(0, 0), ( 1, 0), ( 1, -1), (0, 2), ( 1, 2)]
        },
        "3": {
            "L": [(0, 0), ( 1, 0), ( 1,-1), (0, -2), ( 1, -2)],
            "R": [(0, 0), ( 1, 0), ( 1, 1), (0, -2), ( 1, -2)]
        }
    },
    "W_K_2": {
        "0": {
            "L": [( 0, 0), (-1, 0), ( 2, 0), (-1,-2), ( 2, 1)],
            "R": [( 0, 0), (-2, 0), ( 1, 0), (-2, 1), ( 1,-2)]
        },
        "1": {
            "L": [( 0, 0), (-2, 0), ( 1, 0), (-2, 1), ( 1,-2)],
            "R": [( 0, 0), ( 1, 0), (-2, 0), ( 1, 2), (-2,-1)]
        },
        "2": {
            "L": [( 0, 0), ( 1, 0), (-2, 0), ( 1, 2), (-2, 1)],
            "R": [( 0, 0), ( 2, 0), (-1, 0), ( 2,-1), (-1,-2)]
        },
        "3": {
            "L": [( 0, 0), ( 2, 0), (-1, 0), ( 2,-1), (-1, 2)],
            "R": [( 0, 0), (-1, 0), ( 2, 0), (-1,-2), ( 2, 1)]
        }
    }
}

TETRIS_SCORES = {
    "ROWS": [100, 300, 500, 800],
    "PERFECT_CLEAR": [800, 1200, 1800, 2000],

    "SOFT_DROP": 1,
    "HARD_DROP": 2,
    "COMBO": 50,
}