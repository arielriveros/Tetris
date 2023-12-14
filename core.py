import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Assets(dict):
    def __init__(self):
        super().__init__()

    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        self[name] = value

    def load_assets(self, assets):
        for asset in assets:
            loaded_asset = None
            if asset["type"] == "sounds":
                loaded_asset = pygame.mixer.Sound(asset["path"])
            elif asset["type"] == "image":
                loaded_asset = pygame.image.load(asset["path"])
            elif asset["type"] == "font":
                loaded_asset = pygame.font.Font(asset["path"], asset["size"])
            else:
                loaded_asset = None
        
            self[asset["name"]] = loaded_asset

class Controller:
    def __init__(self, title):
        # pygame
        pygame.init()
        # screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(title)

        # assets
        self.assets = Assets()
    
        # clock
        self.clock = pygame.time.Clock()
        self.running = True
        self.frames_elapsed = 0

    def _update(self):
        pygame.display.update()
        self.clock.tick(FPS)
        self.update()
        self.screen.fill((0, 0, 0))

    def _quit(self):
        pygame.quit()
        exit()

    def _handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)

    def load_assets(self, assets):
        self.assets.load_assets(assets)

    def get_resolution(self):
        return self.screen.get_width(), self.screen.get_height()

    def is_key_pressed(self, key):
        return pygame.key.get_pressed()[key]

    # override
    def init(self):
        pass
    # override
    def update(self):
        pass
    # override
    def draw(self):
        pass
    # override
    def handle_key_down(self, event):
        pass
    # override
    def handle_key_up(self, event):
        pass

    def run(self):
        self.init()
        while self.running:
            self._handle_pygame_events()
            self._update()
            self.draw()
            self.frames_elapsed += 1
        self._quit()