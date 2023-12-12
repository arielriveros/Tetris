from pygame import draw, Surface, Rect

""" 
Class responsible for drawing using a tile-based system
(0, 0) is the top left corner

"""
class TileRenderer:
    def __init__(self, screen: Surface, columns: int, rows: int):
        self.columns: int = columns
        self.rows: int = rows
        self.screen: Surface = screen

    def draw_block(self, block, position: tuple[int, int] = (0, 0)):
        tile_size = self.screen.get_height() // self.rows
        offset = (self.screen.get_width() - tile_size * self.columns) // 2
        draw.rect(
            self.screen,
            block.color,
            Rect(
                (block.position[0] + position[0]) * tile_size + offset,
                (block.position[1] + position[1]) * tile_size,
                tile_size, tile_size)
            )

    def draw_tetromino(self, tetromino):
        for block in tetromino.blocks:
            self.draw_block(block, tetromino.position)

    def draw_grid(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        tile_size = height // self.rows

        offset = (width - tile_size * self.columns) // 2
        
        #draw grid at the center of the screen
        color = (64, 0, 64)
        for i in range(self.columns+1):
            draw.line(self.screen, color, (i * tile_size + offset, 0), (i * tile_size + offset, self.rows * tile_size))
        for i in range(self.rows+1):
            draw.line(self.screen, color, (offset, i * tile_size), (self.columns * tile_size + offset, i * tile_size))
