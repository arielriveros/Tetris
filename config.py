# Configs
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
TILES_PER_ROW = 10
TILES_PER_COLUMN = 20

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
        "name": "move",
        "type": "sounds",
        "path": "assets/move.mp3"
    },
    #{
    #    "name": "rotate",
    #    "type": "sounds",
    #    "path": "assets/sounds/rotate.wav"
    #},
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
    #{
    #    "name": "game_over",
    #    "type": "sounds",
    #    "path": "assets/sounds/game_over.wav"
    #},
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
    #{
    #    "name": "font",
    #    "type": "font",
    #    "path": "assets/fonts/font.ttf",
    #    "size": 32
    #}
]

TETROMINO_DATA = {
    "L": {
        "positions": [[0, -1], [0, 0], [0, 1], [1, 1]],
        "color": (255, 0, 0)
    },
    "J": {
        "positions": [[0, -1], [0, 0], [0, 1], [-1, 1]],
        "color": (0, 255, 0)
    },
    "O": {
        "positions": [[0, 0], [0, 1], [1, 0], [1, 1]],
        "color": (0, 0, 255)
    },
    "I": {
        "positions": [[0, -1], [0, 0], [0, 1], [0, 2]],
        "color": (255, 255, 0)
    },
    "S": {
        "positions": [[0, 0], [0, 1], [1, 0], [1, -1]],
        "color": (255, 0, 255)
    },
    "Z": {
        "positions": [[0, 0], [0, 1], [-1, 0], [-1, -1]],
        "color": (0, 255, 255)
    },
    "T": {
        "positions": [[0, 0], [0, 1], [0, -1], [-1, 0]],
        "color": (255, 255, 255)
    }
}

TETRIS_SCORES = {
    "1_ROW": 100,
    "2_ROWS": 300,
    "3_ROWS": 500,
    "4_ROWS": 800,

    "1_ROW_PERFECT_CLEAR": 800,
    "2_ROWS_PERFECT_CLEAR": 1200,
    "3_ROWS_PERFECT_CLEAR": 1800,
    "4_ROWS_PERFECT_CLEAR": 2000,

    "SOFT_DROP": 1,
    "HARD_DROP": 2,
    "COMBO": 50,
}