from config import TETROMINO_DATA, FPS, TETRIS_SCORES
from pygame import Vector2 as vec
import random
from .tetromino import Tetromino, Block

class TetrisGame:
    """
    Class that handles the game logic
    """
    def __init__(self, controller):
        self.controller = controller
        # tetrominos
        self.active_tetromino   = None # the tetromino that is currently controlled by the player
        self.ghost_tetromino    = None # the ghost tetromino that shows where the active tetromino will land
        self.held_tetromino     = None # the tetromino that is currently held by the player

        # iterables
        self.next_tetrominos    = [] # queue of tetrominos that will spawn next
        self.blocks             = [] # blocks that are already placed
        self.rows               = {} # dictionary that stores the number of blocks in each row
        self.full_rows          = [] # list of rows that are full
        self.bag                = [] # bag of shuffled tetrominos

        # flags
        self.playing            = True  # whether the game is running or not
        self.release_held       = True  # should release the held tetromino or not
        self.soft_dropping      = False # whether the player is soft dropping or not
        self.soft_drop_lock     = False # prevents soft dropping after landing a tetromino
        self.hard_dropped       = False # whether the player has hard dropped the active tetromino or not

        # counters
        self.hard_drop_height   = 0 # the height of the hard drop
        self.combo              = -1 # the number of consecutive line clears
        self.speed              = 1 # tiles per second
        self.level              = 1 # the current level
        self.score              = 0 # the player's score
        self.lines_cleared      = 0 # the number of lines cleared by the player
        self.best_score         = 0 # the player's best score of the session

    def init(self):
        self.begin_game()

    def begin_game(self):
        if not self.playing:
            return
        self.reset_game_state()
        self.set_speed()
        self.generate_bag()
        self.generate_next_tetrominos()
        self.spawn_active_tetromino()
        self.controller.assets.game_over.stop()
        self.controller.assets.bgm.play(-1)

    def reset_game_state(self):
        self.active_tetromino   = None
        self.ghost_tetromino    = None
        self.held_tetromino     = None
        self.next_tetrominos    = []
        self.blocks             = []
        self.rows               = {}
        self.full_rows          = []
        self.bag                = []
        self.release_held       = True
        self.soft_dropping      = False
        self.soft_drop_lock     = False
        self.hard_dropped       = False
        self.hard_drop_height   = 0
        self.combo              = -1
        self.speed              = 1
        self.level              = 1
        self.score              = 0
        self.lines_cleared      = 0

    def end_game(self):
        if not self.playing:
            return
        self.playing = False
        self.controller.assets.bgm.stop()
        self.controller.assets.game_over.play()

    def reset_game(self):
        if self.playing:
            return
        self.reset_game_state()
        self.playing = True
        self.begin_game()

    def generate_bag(self):
        list_of_tetrominos = list(TETROMINO_DATA.keys())
        random.shuffle(list_of_tetrominos)
        self.bag = list_of_tetrominos

    def generate_next_tetrominos(self):
        for _ in range(3):
            if len(self.bag) == 0:
                self.generate_bag()
            tetromino_type = self.bag.pop()
            self.next_tetrominos.append(Tetromino.from_data(tetromino_type))

    def spawn_active_tetromino(self):
        tetromino = None
        # first try to get the held tetromino
        if self.held_tetromino is not None and not self.release_held:        
            tetromino = self.held_tetromino
            self.held_tetromino = None
            self.release_held = True
        # if there is no held tetromino, get the next tetromino from the next tetromino queue
        else:
            tetromino = self.next_tetrominos.pop(0)
        # set it as the active tetromino
        self.active_tetromino = tetromino
        # regenerate the queue if it's empty
        if len(self.bag) == 0:
            self.generate_bag()
        # add the next tetromino to the queue from the shuffled bag
        self.next_tetrominos.append(Tetromino.from_data(self.bag.pop()))
        # set the position of the active tetromino to the top of the board
        self.active_tetromino.position = vec(self.controller.rows // 2, -2)

        # check if the tetromino is colliding with blocks and end the game if it is
        result = self.active_tetromino.detect_collision(self.controller.rows, self.controller.columns, self.blocks)
        if result["blocks"]:
            self.end_game()

    def update_ghost_tetromino(self):
        # If there is no active tetromino, there is no ghost tetromino
        if self.active_tetromino is None:
            self.ghost_tetromino = None
            return
        # Create a copy of the active tetromino
        self.ghost_tetromino = self.active_tetromino.clone()
        # check if the ghost tetromino is colliding with blocks or the floor and move it up until it's colliding
        result = self.ghost_tetromino.detect_collision(self.controller.rows, self.controller.columns, self.blocks)
        while not result["floor"] and not result["blocks"]:
            self.ghost_tetromino.move((0, 1))
            result = self.ghost_tetromino.detect_collision(self.controller.rows, self.controller.columns, self.blocks)

        # Move it back up one step to be above the collision
        self.ghost_tetromino.move((0, -1))
    
    def land_active_tetromino(self):
        for block in self.active_tetromino.get_blocks():
            absolute_position = block.position + self.active_tetromino.position - vec(0, 1)
            self.blocks.append(Block(absolute_position, block.color))
        self.soft_drop_lock = True
        self.spawn_active_tetromino()

    def can_move_active_tetromino(self, direction):
        clone = self.active_tetromino.clone()
        clone.position = self.active_tetromino.position + direction
        result = clone.detect_collision(self.controller.rows, self.controller.columns, self.blocks)
        return not (result["blocks"] or result["wall"] or result["floor"])

    def apply_wall_kick(self, direction):
        wall_kick_tests = self.active_tetromino.get_wall_kicks()['L' if direction == 1 else 'R']
        clone = self.active_tetromino.clone()
        clone.rotate(direction)
        for test in wall_kick_tests:            
            clone.position = self.active_tetromino.position + vec(*test)
            result = clone.detect_collision(self.controller.rows, self.controller.columns, self.blocks)
            if not (result["blocks"] or result["wall"] or result["floor"]):
                return True, test
        return False, None


    def check_full_rows(self):
        for block in self.blocks:
            self.rows[block.position[1]] = self.rows.get(block.position[1], 0) + 1

        # check if any row is full by comparing the number of blocks in each row with the number of max tiles per row
        self.full_rows = [r for r in self.rows if self.rows[r] == self.controller.rows]
        
        # reset the rows dictionary
        self.rows = {}

    def clear_rows(self):
        self.blocks = [block for block in self.blocks if block.position[1] not in self.full_rows]
        for block in self.blocks:
            block.position += vec(0, sum(block.position[1] < row for row in self.full_rows))

    def soft_drop(self, activate: bool = True):
        self.soft_dropping = activate and not self.soft_drop_lock
        if self.soft_dropping:
            self.active_tetromino.move((0, 1))

    def reset_soft_drop_lock(self):
        self.soft_drop_lock = False

    def hard_drop(self):
        height = int(self.ghost_tetromino.position[1] - self.active_tetromino.position[1] - 1)
        # move the tetromino to the ghost tetromino position with an offset of 1 in the y axis so it collides
        self.active_tetromino.position = self.ghost_tetromino.position + vec(0, 1)
        # set the hard drop flag to true so it can be handled in the score
        self.hard_dropped = True
        self.hard_drop_height = height

    def handle_score(self):
        score = 0
        full_clear = len(self.blocks) == 0
        rows_cleared = len(self.full_rows)
        if rows_cleared > 0 and not full_clear:
            score = TETRIS_SCORES['ROWS'][rows_cleared - 1]
            self.controller.assets.line_clear.play()
        elif full_clear:
            score = TETRIS_SCORES['FULL_CLEAR'][rows_cleared - 1]
            self.controller.assets.full_clear.play()
        else:
            self.controller.assets.land.play()

        self.score += score * self.level
        
        # add soft drop score bonus
        self.score += (self.soft_dropping * TETRIS_SCORES['SOFT_DROP'])

        # add hard drop score bonus
        self.score += (self.hard_dropped * TETRIS_SCORES['HARD_DROP'] * self.hard_drop_height)
        # reset hard drop flag after adding the score
        self.hard_dropped = False

        self.lines_cleared += rows_cleared
        # level up every 10 lines
        if self.lines_cleared >= self.level * 10:
            self.level += 1
            self.set_speed()
            self.controller.assets.level_up.play()

    def set_speed(self):
        # calculate the speed based on the level
        time = (0.8 - ((self.level - 1) * 0.007)) ** (self.level - 1)
        self.speed = 1 / time

    def handle_movement(self, direction):
        if self.can_move_active_tetromino(direction) and self.playing:
            self.active_tetromino.move(direction)
            self.controller.assets.move.play()

    def handle_rotation(self, direction):
        if self.playing:
            test, delta = self.apply_wall_kick(direction)
            if test:
                self.active_tetromino.rotate(direction)
                self.active_tetromino.move(vec(*delta))
            self.controller.assets.move.play()

    def hold_active_tetromino(self):
        # if there is no held tetromino, hold the active tetromino and spawn a new one
        if self.held_tetromino is None and self.playing:
            self.held_tetromino = Tetromino.from_data(str(self.active_tetromino))
            self.spawn_active_tetromino()
            self.release_held = False

    def update(self):
        if not self.playing:
            return
        # detect collision each frame
        result = self.active_tetromino.detect_collision(self.controller.rows, self.controller.columns, self.blocks)
        if result["blocks"] or result["floor"]:
            # if the tetromino is colliding with blocks or the floor, land it
            self.land_active_tetromino()
            # check if any row is full and handle score
            self.check_full_rows()

            # handle score on landing
            self.handle_score()

            # if there are full rows clear them and increase the combo
            if len(self.full_rows) > 0:
                self.combo += 1
                self.clear_rows()
            # if there are no full rows reset the combo
            else:
                self.combo = -1

        self.update_ghost_tetromino()
        if self.controller.frames_elapsed % (FPS // self.speed) == 0:
            self.active_tetromino.move((0, 1))
        
