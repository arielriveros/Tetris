from pygame import Vector2 as vec

class Block:
    def __init__(self, position, color):
        self.position: vec = position
        self.color: tuple[int, int, int] = color

class Tetromino:
    def __init__(self, blocks, type = None):
        self.type = type
        self.blocks: tuple[Block, ...] = blocks
        self.position: vec = vec(0, 0)

    def move(self, direction: vec):
        self.position += direction

    def rotate(self, direction: int = 1):
        for block in self.blocks:
            block.position = vec(-block.position[1], block.position[0]) * -direction

    def detect_collision(self, columns, rows, blocks):
        collides_with_blocks = self._detect_block_collision(blocks)
        collides_with_floor = self._detect_floor_collision(rows)
        collides_with_wall = self._detect_wall_collision(columns)
        return {
            "blocks": collides_with_blocks,
            "floor": collides_with_floor,
            "wall": collides_with_wall
        }

    def _detect_wall_collision(self, columns):
        for block in self.blocks:
            absolute_position = block.position + self.position
            if absolute_position[0] < 0 or absolute_position[0] > columns - 1:
                return True
        return False
    
    def _detect_floor_collision(self, rows):
        for block in self.blocks:
            absolute_position = block.position + self.position
            if absolute_position[1] > rows - 1:
                return True
        return False
    
    def _detect_block_collision(self, blocks):
        for block in self.blocks:
            absolute_position = block.position + self.position
            for other_block in blocks:
                if absolute_position == other_block.position:
                    return True
        return False
    
    @staticmethod
    def from_data(data):
        type = data["name"]
        positions = data["positions"]
        color = data["color"]
        blocks = []
        for position in positions:
            blocks.append(Block(position, color))
        return Tetromino(tuple(blocks), type)