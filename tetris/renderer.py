from pygame import BLEND_RGBA_MULT, draw, transform, Rect

from core import AssetManager

class Renderer:
    """ 
    Class responsible for drawing using a tile-based system
    (0, 0) is the top left corner

    """
    def __init__(self, controller, game):
        self.controller = controller
        self.game = game

    def draw(self):
        if self.game.playing:
            self.draw_background('background')
            self.draw_grid()
            for block in self.game.blocks:
                self.draw_block(block, style = 'tile')
            self.draw_tetromino(self.game.ghost_tetromino, style = 'ghost')
            self.draw_tetromino(self.game.active_tetromino, style = 'active_tile')
        
            self.draw_game_ui()
        else:
            self.draw_background('game_over_background')
            self.draw_gameover_ui()

    def draw_block(self, block, position: tuple[int, int] = (0, 0), style = None):
        resolution = self.controller.get_resolution()
        tile_size = resolution[1] // self.controller.columns
        offset = (resolution[0] - tile_size * self.controller.rows) // 2

        if style == 'tile' or style == 'active_tile':
            tile_img = transform.scale(AssetManager().images[style], (tile_size, tile_size))
            tile_img.fill(block.color, special_flags=BLEND_RGBA_MULT)
            self.controller.screen.blit(tile_img, ((block.position[0] + position[0]) * tile_size + offset, (block.position[1] + position[1]) * tile_size))

        elif style == 'ghost':
            # darken color
            color = (block.color[0] // 2, block.color[1] // 2, block.color[2] // 2)
            draw.rect(
                self.controller.screen,
                color,
                Rect((block.position[0] + position[0]) * tile_size + offset,
                     (block.position[1] + position[1]) * tile_size,
                     tile_size, tile_size))

        else:
            draw.rect(
                self.controller.screen,
                block.color,
                Rect((block.position[0] + position[0]) * tile_size + offset,
                     (block.position[1] + position[1]) * tile_size,
                     tile_size, tile_size))

    def draw_tetromino(self, tetromino, offset: tuple[int, int] = (0, 0), style = None):
        if tetromino is None:
            return
        for block in tetromino.get_blocks():
            self.draw_block(block, tetromino.position + offset, style)

    def draw_grid(self):
        resolution = self.controller.get_resolution()
        width = resolution[0]
        height = resolution[1]
        tile_size = height // self.controller.columns

        offset = (width - tile_size * self.controller.rows) // 2

        # draw a black rectangle around the grid
        draw.rect(self.controller.screen, (0, 0, 0), Rect(offset, 0, tile_size * self.controller.rows, tile_size * self.controller.columns))
        
        #draw grid at the center of the screen
        color = (64, 0, 64)
        for i in range(self.controller.rows+1):
            draw.line(self.controller.screen, color, (i * tile_size + offset, 0), (i * tile_size + offset, self.controller.columns * tile_size))
        for i in range(self.controller.columns+1):
            draw.line(self.controller.screen, color, (offset, i * tile_size), (self.controller.rows * tile_size + offset, i * tile_size))

    def draw_background(self, background = 'background'):
        resolution = self.controller.get_resolution()
        image = transform.scale(AssetManager().images[background], resolution)

        # conserve aspect ratio
        if image.get_width() > resolution[0]:
            image = transform.scale(image, (resolution[0], image.get_height()))

        elif image.get_height() > resolution[1]:
            image = transform.scale(image, (image.get_width(), resolution[1]))

        self.controller.screen.blit(image, (0, 0))

    def draw_text(self, text, position: tuple[int, int], color: tuple[int, int, int] = (255, 255, 255), background=False):
        font = AssetManager().fonts['font']
        text_surface = font.render(text, True, color)
        if background:
            draw.rect(self.controller.screen, (0, 0, 0), Rect(position, text_surface.get_size()))
        self.controller.screen.blit(text_surface, position)

    def draw_game_ui(self):
        resolution = self.controller.get_resolution()
        x_offset = resolution[0] // 2 + self.controller.get_resolution()[0] // 4
        y_offset = resolution[1] - self.controller.get_resolution()[1] // 4
        # TOP LEFT
        self.draw_text(f"Level: {self.game.level}", (15, 15))
        self.draw_text(f"Score: {self.game.score}", (15, 55))
        self.draw_text(f"Lines: {self.game.lines_cleared}", (15, 105))
        if self.game.combo > 0:
            self.draw_text(f"Combo: {self.game.combo}", (10, 150))

        # BOTTOM LEFT
        self.draw_text("Stored:", (20, y_offset))
        self.draw_tetromino(
            self.game.held_tetromino,
            (-4, self.controller.rows + 7)
        )

        # TOP RIGHT
        self.draw_text("Next:", (x_offset + 10, 25))
        for i in range(3):
            self.draw_tetromino(
                self.game.next_tetrominos[i],
                (self.controller.rows + 4, 4 * i + 5)
            )

    def draw_gameover_ui(self):
        resolution = self.controller.get_resolution()
        x_offset = resolution[0] // 2
        delta = self.controller.get_resolution()[0] // 4
        self.draw_text("GAME OVER", (x_offset - 25, resolution[1] // 2 - 50), background=True)
        self.draw_text(f"Level: {self.game.level}", (x_offset - delta, resolution[1] // 2), background=True)
        self.draw_text(f"Score: {self.game.score}", (x_offset - 10,resolution[1] // 2), background=True)
        self.draw_text(f"Lines: {self.game.lines_cleared}", (x_offset + delta, resolution[1] // 2), background=True)
        self.draw_text("Press R to restart", (x_offset - 60, resolution[1] // 2 + 100), background=True)
