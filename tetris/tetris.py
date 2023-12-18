import pygame
from tetris.game import Marathon, MarathonTest
from tetris.renderer import Renderer
from core import AssetManager, Controller
from data.config import FPS, ROWS, COLUMNS, SOUND_OPTIONS, ASSET_DATA

    
class Tetris(Controller):
    def __init__(self, test=None):
        super().__init__("Tetris")
        self.rows = ROWS
        self.columns = COLUMNS
        self.game = Marathon(self.rows, self.columns) if test is None else MarathonTest(test, self.rows, self.columns)
        self.tile_renderer = Renderer(self, self.game)

        # load assets before initializing the game
        AssetManager().load_assets(ASSET_DATA)
        pygame.display.set_icon(AssetManager().images["icon"])
        
    def init(self):
        # set sound volumes
        for sound in AssetManager().sounds:
            if "bgm" in sound or sound == "game_over":
                AssetManager().sounds[sound].set_volume(SOUND_OPTIONS["BGM_VOLUME"])
            else:
                AssetManager().sounds[sound].set_volume(SOUND_OPTIONS["SFX_VOLUME"])

        self.game.begin_game()

    def update(self):
        self.game.soft_drop(self.is_key_pressed(pygame.K_DOWN))
        self.game.update(FPS, self.frames_elapsed)

    def draw(self):
        self.tile_renderer.draw()

    def handle_key_down(self, event):
        if event.key == pygame.K_LEFT:
            self.game.handle_movement((-1, 0))
        elif event.key == pygame.K_RIGHT:
            self.game.handle_movement((1, 0))
        elif event.key == pygame.K_UP:
            self.game.handle_rotation(-1)
        elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
            self.game.handle_rotation(1)
        elif event.key == pygame.K_SPACE:
            self.game.hard_drop()
        elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
            self.game.handle_hold()
        elif event.key == pygame.K_r:
            self.game.reset_game()

    def handle_key_up(self, event):
        if event.key == pygame.K_DOWN:
            self.game.reset_soft_drop_lock()
