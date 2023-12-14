import pygame
from tetris.game import TetrisGame
from tetris.renderer import Renderer
from core import Controller
from config import TILES_PER_ROW, TILES_PER_COLUMN, SOUND_OPTIONS, ASSET_DATA

    
class Tetris(Controller):
    def __init__(self):
        super().__init__("Tetris")
        self.rows = TILES_PER_COLUMN
        self.columns = TILES_PER_ROW
        self.game = TetrisGame(self)
        self.tile_renderer = Renderer(self)
        
    def init(self):
        self.load_assets(ASSET_DATA)
        self.assets.bgm.set_volume(SOUND_OPTIONS["BGM_VOLUME"])
        self.assets.bgm.play(-1)

        self.assets.move.set_volume(SOUND_OPTIONS["SFX_VOLUME"])
        self.assets.land.set_volume(SOUND_OPTIONS["SFX_VOLUME"])
        self.assets.line_clear.set_volume(SOUND_OPTIONS["SFX_VOLUME"])
        self.assets.full_clear.set_volume(SOUND_OPTIONS["SFX_VOLUME"])

        self.game.spawn_active_tetromino()

    def update(self):
        self.game.update()
        self.game.soft_drop(self.is_key_pressed(pygame.K_DOWN))

    def draw(self):
        self.tile_renderer.draw()

    def handle_key_down(self, event):
        if event.key == pygame.K_LEFT and self.game.can_move_active_tetromino((-1, 0)):
            self.game.active_tetromino.move((-1, 0))
            self.assets.move.play()
        elif event.key == pygame.K_RIGHT and self.game.can_move_active_tetromino((1, 0)):
            self.game.active_tetromino.move((1, 0))
            self.assets.move.play()
        elif event.key == pygame.K_UP and self.game.can_rotate_active_tetromino(1):
            self.game.active_tetromino.rotate(1)
        elif event.key == pygame.K_z and self.game.can_rotate_active_tetromino(-1):
            self.game.active_tetromino.rotate(-1)
