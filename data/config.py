# Configs
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
RESIZABLE = False
FPS = 60
ROWS = 10
COLUMNS = 20

SOUND_OPTIONS = {
    'ACTIVE_BGM': True,
    'BGM_VOLUME': 0.1,
    'ACTIVE_SFX': True,
    'SFX_VOLUME': 0.5
}

ASSET_DATA = [
    {
        'name': 'bgm_1',
        'type': 'sounds',
        'path': 'assets/music/bgm.mp3'
    },
    {
        'name': 'game_over',
        'type': 'sounds',
        'path': 'assets/music/game_over.mp3'
    },
    {
        'name': 'move',
        'type': 'sounds',
        'path': 'assets/sounds/move.mp3'
    },
    {
        'name': 'land',
        'type': 'sounds',
        'path': 'assets/sounds/land.mp3'
    },
    {
        'name': 'line_clear',
        'type': 'sounds',
        'path': 'assets/sounds/line_clear.mp3'
    },
    {
        'name': 'full_clear',
        'type': 'sounds',
        'path': 'assets/sounds/full_clear.mp3'
    },
    {
        'name': 'level_up',
        'type': 'sounds',
        'path': 'assets/sounds/next_level.mp3'
    },
    {
        'name': 'tile',
        'type': 'image',
        'path': 'assets/images/tile.png'
    },
    {
        'name': 'active_tile',
        'type': 'image',
        'path': 'assets/images/active_tile.png'
    },
    {
        'name': 'background',
        'type': 'image',
        'path': 'assets/images/background.png'
    },
    {
        'name': 'game_over_background',
        'type': 'image',
        'path': 'assets/images/game_over.png'
    },
    {
        'name': 'icon',
        'type': 'image',
        'path': 'assets/images/icon.png'
    },
    {
        'name': 'font',
        'type': 'font',
        'path': 'assets/fonts/retro.ttf',
        'size': 16
    }
]