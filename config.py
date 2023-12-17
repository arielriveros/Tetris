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

TETROMINO_DATA = {
    "L": {
        "name": "L",
        "positions": [[0, -1], [0, 0], [0, 1], [1, 1]],
        "color": (255, 0, 0)
    },
    "J": {
        "name": "J",
        "positions": [[0, -1], [0, 0], [0, 1], [-1, 1]],
        "color": (0, 255, 0)
    },
    "O": {
        "name": "O",
        "positions": [[0, 0], [0, 1], [1, 0], [1, 1]],
        "color": (0, 0, 255)
    },
    "I": {
        "name": "I",
        "positions": [[0, -1], [0, 0], [0, 1], [0, 2]],
        "color": (255, 255, 0)
    },
    "S": {
        "name": "S",
        "positions": [[0, 0], [0, 1], [1, 0], [1, -1]],
        "color": (255, 0, 255)
    },
    "Z": {
        "name": "Z",
        "positions": [[0, 0], [0, 1], [-1, 0], [-1, -1]],
        "color": (0, 255, 255)
    },
    "T": {
        "name": "T",
        "positions": [[0, 0], [0, 1], [0, -1], [-1, 0]],
        "color": (255, 255, 255)
    }
}

TETRIS_SCORES = {
    "ROWS": [100, 300, 500, 800],
    "PERFECT_CLEAR": [800, 1200, 1800, 2000],

    "SOFT_DROP": 1,
    "HARD_DROP": 2,
    "COMBO": 50,
}