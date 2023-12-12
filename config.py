# Configs
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
TILES_PER_ROW = 10
TILES_PER_COLUMN = 20
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