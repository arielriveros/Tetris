from pygame import draw, transform, Rect

class Renderer:
    """ 
    Class responsible for drawing using a tile-based system
    (0, 0) is the top left corner

    """
    def __init__(self, controller):
        self.controller = controller

    def draw(self):
        self.draw_background()
        if self.controller.game.playing:
            self.draw_grid()
            for block in self.controller.game.blocks:
                self.draw_block(block, stylized=True)
            self.draw_tetromino(self.controller.game.ghost_tetromino)
            self.draw_tetromino(self.controller.game.active_tetromino, stylized=True)
        
            self.draw_game_ui()
        else:
            self.draw_gameover_ui()

    def draw_block(self, block, position: tuple[int, int] = (0, 0), stylized: bool = False):
        resolution = self.controller.get_resolution()
        tile_size = resolution[1] // self.controller.columns
        offset = (resolution[0] - tile_size * self.controller.rows) // 2
        draw.rect(
            self.controller.screen,
            block.color,
            Rect(
                (block.position[0] + position[0]) * tile_size + offset,
                (block.position[1] + position[1]) * tile_size,
                tile_size, tile_size)
            )
        if stylized:
            tile_img = transform.scale(self.controller.assets.tile, (tile_size, tile_size))
            tile_img.set_alpha(128)
            self.controller.screen.blit(tile_img, ((block.position[0] + position[0]) * tile_size + offset, (block.position[1] + position[1]) * tile_size))

    def draw_tetromino(self, tetromino, offset: tuple[int, int] = (0, 0), stylized: bool = False):
        if tetromino is None:
            return
        for block in tetromino.blocks:
            self.draw_block(block, tetromino.position + offset, stylized)

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

    def draw_background(self):
        resolution = self.controller.get_resolution()
        image = transform.scale(self.controller.assets.background, resolution)

        # conserve aspect ratio
        if image.get_width() > resolution[0]:
            image = transform.scale(image, (resolution[0], image.get_height()))

        elif image.get_height() > resolution[1]:
            image = transform.scale(image, (image.get_width(), resolution[1]))

        self.controller.screen.blit(image, (0, 0))

    def draw_text(self, text, position: tuple[int, int], color: tuple[int, int, int] = (255, 255, 255)):
        font = self.controller.assets.font
        text_surface = font.render(text, True, color)
        draw.rect(self.controller.screen, (0, 0, 0), Rect(position, text_surface.get_size()))
        self.controller.screen.blit(text_surface, position)

    def draw_game_ui(self):
        resolution = self.controller.get_resolution()
        x_offset = resolution[0] // 2 + self.controller.get_resolution()[0] // 4
        y_offset = resolution[1] - self.controller.get_resolution()[1] // 4
        # TOP LEFT
        self.draw_text(f"Level:", (10, 10))
        self.draw_text(f"Score: {self.controller.game.score}", (10, 50))
        self.draw_text(f"Lines: {self.controller.game.lines_cleared}", (10, 100))
        if self.controller.game.combo > 0:
            self.draw_text(f"Combo: {self.controller.game.combo}", (10, 150))

        # BOTTOM LEFT
        self.draw_text("Stored:", (10, y_offset))
        self.draw_tetromino(
            self.controller.game.held_tetromino,
            (-5, self.controller.rows + 6),
            stylized=True
        )

        # TOP RIGHT
        self.draw_text("Next:", (x_offset, 10))
        for i in range(3):
            self.draw_tetromino(
                self.controller.game.next_tetrominos[i],
                (self.controller.rows + 3, 5 * i + 5),
                stylized=True
            )

    def draw_gameover_ui(self):
        resolution = self.controller.get_resolution()
        x_offset = resolution[0] // 2
        delta = self.controller.get_resolution()[0] // 4
        self.draw_text("GAME OVER", (x_offset - 25, resolution[1] // 2 - 50))
        self.draw_text(f"Level: {self.controller.game.level}", (x_offset - delta, resolution[1] // 2))
        self.draw_text(f"Score: {self.controller.game.score}", (x_offset - 10,resolution[1] // 2))
        self.draw_text(f"Lines: {self.controller.game.lines_cleared}", (x_offset + delta, resolution[1] // 2))
        self.draw_text("Press R to restart", (x_offset - 60, resolution[1] // 2 + 100))
