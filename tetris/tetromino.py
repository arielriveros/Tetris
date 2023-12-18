import copy
from pygame import Vector2 as vec

from data.data import TETROMINO_DATA, WALL_KICK_DATA

class Block:
    def __init__(self, position, color):
        self.position: tuple[int, int] = position
        self.color: tuple[int, int, int] = color

class Tetromino:
    def __init__(self, name = "", blocks=[], wall_kicks = {}):
        self.name = name
        self.blocks: list[list[Block]] = blocks
        self.position: vec = vec(0, 0)
        self.rotation: int = 0
        self.wall_kicks = wall_kicks

    def get_rotation(self):
        return self.rotation % len(self.blocks)

    def get_blocks(self):
        return self.blocks[self.get_rotation()]
    
    def get_wall_kicks(self):
        return self.wall_kicks[str(self.get_rotation())]
    
    def clone(self):
        clone = copy.deepcopy(self)
        return clone

    def move(self, direction: vec):
        self.position += direction

    def rotate(self, direction: int = 1):
        self.rotation += direction

    def detect_collision(self, columns, rows, blocks):
        collides_with_blocks = False
        collides_with_floor = False
        collides_with_wall = False

        for block in self.get_blocks():
            absolute_position = block.position + self.position
            if absolute_position[0] < 0 or absolute_position[0] > columns - 1:
                collides_with_wall = True
            if absolute_position[1] > rows - 1:
                collides_with_floor = True
            for other_block in blocks:
                if absolute_position == other_block.position:
                    collides_with_blocks = True

        return {
            "blocks": collides_with_blocks,
            "floor": collides_with_floor,
            "wall": collides_with_wall
        }
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def from_data(type):
        data = TETROMINO_DATA[type]
        color = data["color"]
        positions = data["positions"]
        blocks = [[Block(pos, color) for pos in position] for position in positions.values()]
        wall_kicks = WALL_KICK_DATA[data["wall_kick"]]
        return Tetromino(type, blocks, wall_kicks)