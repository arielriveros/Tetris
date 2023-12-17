import pygame
from tetris.game import TetrisGame
from tetris.renderer import Renderer
from core import Controller
from config import ROWS, COLUMNS, SOUND_OPTIONS, ASSET_DATA

    
class Tetris(Controller):
    def __init__(self):
        super().__init__("Tetris")
        self.rows = ROWS
        self.columns = COLUMNS
        self.game = TetrisGame(self)
        self.tile_renderer = Renderer(self)
        
    def init(self):
        self.load_assets(ASSET_DATA)
        self.assets.bgm.set_volume(SOUND_OPTIONS["BGM_VOLUME"])
        self.assets.game_over.set_volume(SOUND_OPTIONS["BGM_VOLUME"])
        self.assets.move.set_volume(SOUND_OPTIONS["SFX_VOLUME"])
        self.assets.land.set_volume(SOUND_OPTIONS["SFX_VOLUME"])
        self.assets.line_clear.set_volume(SOUND_OPTIONS["SFX_VOLUME"])
        self.assets.full_clear.set_volume(SOUND_OPTIONS["SFX_VOLUME"])

        self.game.init()

    def update(self):
        self.game.soft_drop(self.is_key_pressed(pygame.K_DOWN))
        self.game.update()

    def draw(self):
        self.tile_renderer.draw()

    def handle_key_down(self, event):
        if event.key == pygame.K_LEFT:
            self.game.handle_movement((-1, 0))
        elif event.key == pygame.K_RIGHT:
            self.game.handle_movement((1, 0))
        elif event.key == pygame.K_UP:
            self.game.handle_rotation(1)
        elif event.key == pygame.K_z:
            self.game.handle_rotation(-1)
        elif event.key == pygame.K_SPACE:
            self.game.hard_drop()
        elif event.key == pygame.K_c:
            self.game.hold_active_tetromino()
        elif event.key == pygame.K_r:
            self.game.reset_game()

    def handle_key_up(self, event):
        if event.key == pygame.K_DOWN:
            self.game.reset_soft_drop_lock()
