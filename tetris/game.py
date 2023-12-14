from config import TETROMINO_DATA, TILES_PER_ROW, TILES_PER_COLUMN, FPS, TETRIS_SCORES
from pygame import Vector2 as vec
import random
import copy
from .tetromino import Tetromino, Block

class TetrisGame:
    """
    Class that handles the game logic
    """
    def __init__(self, controller):
        self.controller = controller
        self.speed = 1 # tiles per second
        self.active_tetromino = None # the tetromino that is currently controlled by the player
        self.ghost_tetromino = None # the ghost tetromino that shows where the active tetromino will land
        self.next_tetrominos = [] # the tetrominos that will spawn next
        self.blocks = [] # blocks that are already placed
        self._bag = [] # bag of shuffled tetrominos
        self._soft_dropping = False # whether the player is soft dropping or not
        
        self.level = 1 # the current level
        self.score = 0 # the player's score
        self.lines_cleared = 0 # the number of lines cleared by the player

    def init(self):
        self.set_speed()
        self.generate_bag()
        self.spawn_active_tetromino()

    def generate_bag(self):
        list_of_tetrominos = list(TETROMINO_DATA.values())
        random.shuffle(list_of_tetrominos)
        self._bag = list_of_tetrominos

    def spawn_active_tetromino(self):
        if len(self._bag) == 0:
            self.generate_bag()
        tetromino_data = self._bag.pop()
        self.active_tetromino = Tetromino.from_data(tetromino_data)
        self.active_tetromino.position = vec(TILES_PER_ROW // 2, 0)

    def update_ghost_tetromino(self):
        if self.active_tetromino is None:
            self.ghost_tetromino = None
            return

        # Create a copy of the active tetromino
        self.ghost_tetromino = copy.deepcopy(self.active_tetromino)

        # Move the ghost tetromino down until it collides
        while not (self.ghost_tetromino.detect_block_collision(self.blocks) or 
                self.ghost_tetromino.detect_floor_collision(TILES_PER_COLUMN)):
            self.ghost_tetromino.move((0, 1))

        # Move it back up one step to be above the collision
        self.ghost_tetromino.move((0, -1))

    def handle_final_collision(self):
        if self.active_tetromino.detect_block_collision(self.blocks) or self.active_tetromino.detect_floor_collision(TILES_PER_COLUMN):
            for block in self.active_tetromino.blocks:
                absolute_position = block.position + self.active_tetromino.position - vec(0, 1)
                self.blocks.append(Block(absolute_position, block.color))
            self.spawn_active_tetromino()
            return True
        return False
    
    def can_move_active_tetromino(self, direction):
        clone = Tetromino(self.active_tetromino.blocks)
        clone.position = self.active_tetromino.position + direction
        return not clone.detect_wall_collision(TILES_PER_ROW) and not clone.detect_block_collision(self.blocks)

    def can_rotate_active_tetromino(self, direction):
        #TODO: Handle wall kicks
        # A deep copy is needed because the rotate method modifies the blocks from the original tetromino
        clone = copy.deepcopy(self.active_tetromino)
        clone.position = self.active_tetromino.position
        clone.rotate(direction)
        return not (clone.detect_wall_collision(TILES_PER_ROW) or clone.detect_floor_collision(TILES_PER_COLUMN) or clone.detect_block_collision(self.blocks))

    def check_for_full_rows(self):
        # save in a dictionary the number of blocks in each row
        rows = {}
        for block in self.blocks:
            if block.position[1] in rows:
                rows[block.position[1]] += 1
            else:
                rows[block.position[1]] = 1
        # check if any row is full
        full_rows = []
        for row in rows:
            if rows[row] == TILES_PER_ROW:
                full_rows.append(row)
        # remove full rows
        if len(full_rows) > 0:
            self.remove_rows(full_rows)

        self.handle_score(len(full_rows), len(self.blocks) == 0)

        return len(full_rows), len(self.blocks) == 0
    
    def soft_drop(self, activate: bool = True):
        self._soft_dropping = activate
        if self.can_move_active_tetromino((0, 1)) and self._soft_dropping:
            self.active_tetromino.move((0, 1))    
        elif self._soft_dropping:
            self.handle_final_collision()

    def remove_rows(self, rows):
        self.blocks = [block for block in self.blocks if block.position[1] not in rows]
        for block in self.blocks:
            block.position += vec(0, sum(block.position[1] < row for row in rows))

    def handle_score(self, rows_cleared, full_clear): 
        if rows_cleared > 0 and not full_clear:
            self.score += TETRIS_SCORES['ROWS'][rows_cleared - 1] * (self._soft_dropping + 1)
        elif full_clear:
            self.score += TETRIS_SCORES['FULL_CLEAR'] * (self._soft_dropping + 1)
        else:
            self.score += (self._soft_dropping * 1)

        self.lines_cleared += rows_cleared

        # level up every 10 lines
        if self.lines_cleared >= self.level * 10:
            self.level += 1
            self.set_speed()
            
    def set_speed(self):
        time = (0.8 - ((self.level - 1) * 0.007)) ** (self.level - 1)
        self.speed = 1 / time

    def update(self):
        if self.controller.frames_elapsed % (FPS // self.speed) == 0:
            self.active_tetromino.move((0, 1))
        if self.handle_final_collision():
            rows_cleared, full_clear = self.check_for_full_rows()

            if full_clear:
                self.controller.assets.full_clear.play()
            elif rows_cleared > 0:
                self.controller.assets.line_clear.play()
            else:
                self.controller.assets.land.play()
        self.update_ghost_tetromino()

        
