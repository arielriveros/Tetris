import pygame
from data.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, RESIZABLE

def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class AssetManager():
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_assets(self, assets):
        for asset in assets:
            if asset["type"] == "sounds":
                self.sounds[asset["name"]] = pygame.mixer.Sound(asset["path"])
            elif asset["type"] == "image":
                self.images[asset["name"]] = pygame.image.load(asset["path"])
            elif asset["type"] == "font":
                self.fonts[asset["name"]] = pygame.font.Font(asset["path"], asset["size"])
            else:
                raise Exception("Invalid asset type")
            
    def play_sound(self, name, loops = 0):
        if name in self.sounds:
            self.sounds[name].play(loops = loops)

    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()

class Controller:
    def __init__(self, title):
        # pygame
        pygame.init()
        # screen

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
        pygame.display.set_caption(title)
    
        # clock
        self.clock = pygame.time.Clock()
        self.running = True
        self.frames_elapsed = 0

    def __update(self):
        pygame.display.update()
        self.clock.tick(FPS)
        self.update()
        self.screen.fill((0, 0, 0))

    def __quit(self):
        pygame.quit()
        exit()

    def __handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)

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
            self.__handle_pygame_events()
            self.__update()
            self.draw()
            self.frames_elapsed += 1
        self.__quit()