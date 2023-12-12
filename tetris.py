import random
import pygame
from pygame import Vector2 as vec
from tilerenderer import TileRenderer
from tetromino import Tetromino, Block
from controller import Controller
import config as cfg
import copy
    
class Tetris(Controller):
    def __init__(self):
        super().__init__("Tetris")
        self.tile_renderer = TileRenderer(self.screen, cfg.TILES_PER_ROW, cfg.TILES_PER_COLUMN)
        self.count = 0
        self.speed = 1 # tiles per second
        self.active_tetromino = None # the tetromino that is currently controlled by the player
        self.blocks = [] # blocks that are already placed
        self.bag = [] # bag of shuffled tetrominos

    def init(self):
        self.background_music.play()
        self.spawn_tetromino()

    def spawn_tetromino(self):
        if len(self.bag) == 0:
            self.generate_bag()
        tetromino_data = self.bag.pop()
        self.active_tetromino = Tetromino.from_data(tetromino_data)
        self.active_tetromino.position = vec(cfg.TILES_PER_ROW // 2, 0)

    def generate_bag(self):
        list_of_tetrominos = list(cfg.TETROMINO_DATA.values())
        random.shuffle(list_of_tetrominos)
        self.bag = list_of_tetrominos
    
    def handle_last_collision(self):
        if self.active_tetromino.detect_block_collision(self.blocks) or self.active_tetromino.detect_floor_collision(cfg.TILES_PER_COLUMN):
            for block in self.active_tetromino.blocks:
                absolute_position = block.position + self.active_tetromino.position - vec(0, 1)
                self.blocks.append(Block(absolute_position, block.color))
            self.spawn_tetromino()

    def move_active_tetromino(self, direction):
        clone = Tetromino(self.active_tetromino.blocks)
        clone.position = self.active_tetromino.position + direction
        if clone.detect_wall_collision(cfg.TILES_PER_ROW):
            return
        if clone.detect_block_collision(self.blocks):
            return
        self.active_tetromino.move(direction)

    def rotate_active_tetromino(self, direction):
        #TODO: Handle wall kicks
        # A deep copy is needed because the rotate method modifies the blocks from the original tetromino
        clone = copy.deepcopy(self.active_tetromino)
        clone.position = self.active_tetromino.position
        clone.rotate(direction)
        if clone.detect_wall_collision(cfg.TILES_PER_ROW) or clone.detect_floor_collision(cfg.TILES_PER_COLUMN) or clone.detect_block_collision(self.blocks):
            return

        # After the clone has been tested, the original tetromino can be rotated
        self.active_tetromino.rotate(direction)

    def check_for_full_rows(self):
        rows = {}
        for block in self.blocks:
            if block.position[1] not in rows:
                rows[block.position[1]] = 1
            else:
                rows[block.position[1]] += 1
        for row in rows:
            if rows[row] == cfg.TILES_PER_ROW:
                self.remove_row(row)

    def remove_row(self, row):
        for block in self.blocks:
            if block.position[1] == row:
                self.blocks.remove(block)
        for block in self.blocks:
            if block.position[1] < row:
                block.position += vec(0, 1)

    def update(self):
        if self.is_key_pressed(pygame.K_DOWN):
            self.move_active_tetromino((0, 1))

        if self.count % (60 // self.speed) == 0:
            self.active_tetromino.move((0, 1))

        self.handle_last_collision()
        self.check_for_full_rows()
        self.count += 1

    def draw(self):
        self.tile_renderer.draw_grid()
        for block in self.blocks:
            self.tile_renderer.draw_block(block)
        self.tile_renderer.draw_tetromino(self.active_tetromino)

    def handle_key_down(self, event):
        if event.key == pygame.K_LEFT:
            self.move_active_tetromino((-1, 0))
        elif event.key == pygame.K_RIGHT:
            self.move_active_tetromino((1, 0))
        elif event.key == pygame.K_UP:
            self.rotate_active_tetromino(1)
        elif event.key == pygame.K_z:
            self.rotate_active_tetromino(-1)

if __name__ == "__main__":
    app = Tetris()
    app.run()