from core import AssetManager
from data.data import TETROMINO_DATA, TETRIS_SCORES
from data.data_test import TESTING_SUITE
from pygame import Vector2 as vec
import random
from .tetromino import Tetromino, Block

class Marathon:
    """
    Class that handles the game logic
    """
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        # tetrominos
        self.active_tetromino   = None # the tetromino that is currently controlled by the player
        self.ghost_tetromino    = None # the ghost tetromino that shows where the active tetromino will land
        self.held_tetromino     = None # the tetromino that is currently held by the player

        # iterables
        self.next_tetrominos    = [] # queue of tetrominos that will spawn next
        self.blocks             = [] # blocks that are already placed
        self.blocks_per_row     = {} # dictionary that stores the number of blocks in each row
        self.full_rows          = [] # list of rows that are full
        self.bag                = [] # bag of shuffled tetrominos

        # flags
        self.playing            = True  # whether the game is running or not
        self.hold_lock          = False # prevents holding the active tetromino more than once per tetromino
        self.soft_dropping      = False # whether the player is soft dropping or not
        self.soft_drop_lock     = False # prevents soft dropping after landing a tetromino
        self.hard_dropped       = False # whether the player has hard dropped the active tetromino or not

        # counters
        self.soft_drop_counter  = 0 # the number of soft drops
        self.hard_drop_height   = 0 # the height of the hard drop
        self.combo              = -1 # the number of consecutive line clears
        self.speed              = 1 # tiles per second
        self.level              = 1 # the current level
        self.score              = 0 # the player's score
        self.lines_cleared      = 0 # the number of lines cleared by the player

    def reset_game_state(self):
        # resets the game state
        return self.__init__(self.rows, self.columns)

    def end_game(self):
        # ends the game and plays the game over music
        if not self.playing:
            return
        self.playing = False
        AssetManager().stop_sound("bgm_1")
        AssetManager().play_sound("game_over")

    def generate_bag(self):
        # first make a list with all 7 tetrominos
        list_of_tetrominos = list(TETROMINO_DATA.keys())
        # then shuffle it
        random.shuffle(list_of_tetrominos)
        self.bag = list_of_tetrominos

        # if the next tetrominos queue is empty, generate the first 3 tetrominos
        # this will happen only when the game starts
        self.init_next_tetrominos()

    def init_next_tetrominos(self):
        if len(self.next_tetrominos) > 0:
            return
        for _ in range(3):
            if len(self.bag) == 0:
                self.generate_bag()
            tetromino_type = self.bag.pop()
            self.next_tetrominos.append(Tetromino.from_data(tetromino_type))

    def spawn_active_tetromino(self):
        # get the next tetromino from the queue and
        # set it as the active tetromino
        self.active_tetromino = self.next_tetrominos.pop(0)
        # regenerate the queue if it's empty
        if len(self.bag) == 0:
            self.generate_bag()
        # add the next tetromino to the queue from the shuffled bag
        self.next_tetrominos.append(Tetromino.from_data(self.bag.pop()))
        # set the position of the active tetromino to the top of the board
        self.active_tetromino.position = vec(self.rows // 2, -2)

        # check if the tetromino is colliding with blocks and end the game if it is
        result = self.active_tetromino.detect_collision(self.rows, self.columns, self.blocks)
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
        result = self.ghost_tetromino.detect_collision(self.rows, self.columns, self.blocks)
        while not result["floor"] and not result["blocks"]:
            self.ghost_tetromino.move((0, 1))
            result = self.ghost_tetromino.detect_collision(self.rows, self.columns, self.blocks)

        # Move it back up one step to be above the collision
        self.ghost_tetromino.move((0, -1))
    
    def land_active_tetromino(self):
        # add the blocks of the active tetromino to the blocks list
        for block in self.active_tetromino.get_blocks():
            absolute_position = block.position + self.active_tetromino.position - vec(0, 1)
            self.blocks.append(Block(absolute_position, block.color))
        # locks the player of soft dropping after landing
        self.soft_drop_lock = True
        # resets the hold lock
        if self.hold_lock:
            self.hold_lock = False
        # spawn a new tetromino after landing
        self.spawn_active_tetromino()

    def can_move_active_tetromino(self, direction):
        # before moving check if a copy collides if applied
        clone = self.active_tetromino.clone()
        clone.position = self.active_tetromino.position + direction
        result = clone.detect_collision(self.rows, self.columns, self.blocks)
        return not (result["blocks"] or result["wall"] or result["floor"])

    def apply_wall_kick(self, direction):
        # test every wall kick test and return the first one that doesn't collide
        # returns a tuple with a boolean that indicates if a wall kick was applied
        # and the delta of the wall kick
        wall_kick_tests = self.active_tetromino.get_wall_kicks()['L' if direction == 1 else 'R']
        clone = self.active_tetromino.clone()
        clone.rotate(direction)
        for test in wall_kick_tests:            
            clone.position = self.active_tetromino.position + vec(*test)
            result = clone.detect_collision(self.rows, self.columns, self.blocks)
            if not (result["blocks"] or result["wall"] or result["floor"]):
                return True, test
        return False, None

    def check_full_rows(self):
        # count the number of blocks in each row
        for block in self.blocks:
            self.blocks_per_row[block.position[1]] = self.blocks_per_row.get(block.position[1], 0) + 1
        # check if any row is full by comparing the number of blocks in each row with the number of max tiles per row
        self.full_rows = [r for r in self.blocks_per_row if self.blocks_per_row[r] == self.rows]
        # reset the rows dictionary
        self.blocks_per_row = {}

    def clear_rows(self):
        # remove the blocks in the full rows
        self.blocks = [block for block in self.blocks if block.position[1] not in self.full_rows]
        for block in self.blocks:
            block.position += vec(0, sum(block.position[1] < row for row in self.full_rows))

    def begin_game(self):
        if not self.playing:
            return
        self.set_speed()
        self.generate_bag()
        self.spawn_active_tetromino()
        AssetManager().stop_sound("game_over")
        AssetManager().play_sound("bgm_1", -1)

    def reset_game(self):
        if self.playing:
            return
        self.reset_game_state()
        self.playing = True
        self.begin_game()

    def handle_movement(self, direction):
        if self.can_move_active_tetromino(direction) and self.playing:
            self.active_tetromino.move(direction)
            AssetManager().play_sound("move")

    def handle_rotation(self, direction):
        if self.playing:
            test, delta = self.apply_wall_kick(direction)
            if not test: return
            
            self.active_tetromino.rotate(direction)
            self.active_tetromino.move(vec(*delta))
            AssetManager().play_sound("move")

    def handle_score(self):
        score = 0
        rows_cleared = len(self.full_rows)
        # a full clear is when there are no blocks left after clearing the rows
        full_clear = len(self.blocks) - rows_cleared * self.rows == 0 and rows_cleared > 0
        if full_clear:
            score = TETRIS_SCORES['PERFECT_CLEAR'][rows_cleared - 1]
            AssetManager().play_sound("full_clear")
        elif rows_cleared > 0 and not full_clear:
            score = TETRIS_SCORES['ROWS'][rows_cleared - 1]
            AssetManager().play_sound("line_clear")
        
        else:
            AssetManager().play_sound("land")

        self.score += score * self.level
        
        # add soft drop score bonus
        self.score += (self.soft_drop_counter * TETRIS_SCORES['SOFT_DROP'])
        # reset soft drop counter after adding the score
        self.soft_drop_counter = 0

        # add hard drop score bonus
        self.score += (self.hard_dropped * TETRIS_SCORES['HARD_DROP'] * self.hard_drop_height)
        # reset hard drop flag after adding the score
        self.hard_dropped = False

        # add combo score bonus
        if self.combo > 0:
            self.score += (self.combo * TETRIS_SCORES['COMBO'] * self.level)

        self.lines_cleared += rows_cleared
        # level up every 10 lines
        if self.lines_cleared >= self.level * 10:
            self.level += 1
            self.set_speed()
            AssetManager().play_sound("level_up")

    def handle_hold(self):
        if not self.playing: return
        # if there is no held tetromino, hold the active tetromino and spawn a new one
        if self.held_tetromino is None:
            self.held_tetromino = Tetromino.from_data(str(self.active_tetromino))
            self.spawn_active_tetromino()
            self.hold_lock = True
        # if there is a held tetromino, swap it with the active tetromino
        # only if the hold lock is not active
        elif not self.hold_lock:
            active_tmp = str(self.held_tetromino)
            self.held_tetromino = Tetromino.from_data(str(self.active_tetromino))
            self.active_tetromino = Tetromino.from_data(active_tmp)
            self.active_tetromino.position = vec(self.rows // 2, -2)
            self.hold_lock = True

    def soft_drop(self, activate: bool = True):
        # soft drop if the player is holding the down key and the soft drop lock is not active
        self.soft_dropping = activate and not self.soft_drop_lock
        if self.soft_dropping:
            self.active_tetromino.move((0, 1))
            self.soft_drop_counter += 1

    def reset_soft_drop_lock(self):
        # reset the soft drop lock when the soft drop key is released
        self.soft_drop_lock = False

    def hard_drop(self):
        # calculate the height of the hard drop
        height = int(self.ghost_tetromino.position[1] - self.active_tetromino.position[1])
        # move the tetromino to the ghost tetromino position with an offset of 1 in the y axis so it collides
        self.active_tetromino.position = self.ghost_tetromino.position + vec(0, 1)
        # set the hard drop flag to true so it can be handled in the score
        self.hard_dropped = True
        self.hard_drop_height = height

    def update(self, fps, time):
        if not self.playing:
            return
        # detect collision each frame
        result = self.active_tetromino.detect_collision(self.rows, self.columns, self.blocks)
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
        if time % (fps // self.speed) == 0:
            self.active_tetromino.move((0, 1))
        
    def set_speed(self):
        self.speed = 1 / (0.8 - ((self.level - 1) * 0.007)) ** (self.level - 1)

class MarathonTest(Marathon):
    def __init__(self, test, rows, columns):
        super().__init__(rows, columns)
        self.test_data = TESTING_SUITE[test]
        self.parse_blocks_from_string(self.test_data['TESTING_GRID'])

    def parse_blocks_from_string(self, string):
        self.blocks = []
        pos = 0
        for i in range(len(string)):
            if string[i] == '.':
                pos += 1
            elif string[i] == '#':
                x = pos % self.rows
                y = pos // self.rows - 1 
                pos += 1
                self.blocks.append(Block(vec(x, y), (255, 255, 255)))

    def generate_bag(self):
        self.bag = list(self.test_data['TESTING_TETROMINOS'])
        self.bag.reverse()
        self.init_next_tetrominos()

    def set_speed(self):
        self.speed = self.test_data['TESTING_SPEED']

    def reset_game(self):
        pass
