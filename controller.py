import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
pygame.init()

class Controller:
    def __init__(self, title):
        # screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(title)

        self.background_music = pygame.mixer.Sound("assets/bgm.mp3")
        self.background_music.set_volume(0.25)
        self.background_music.play(loops=-1)
    
        # clock
        self.clock = pygame.time.Clock()
        self.running = True

    def _update(self):
        pygame.display.update()
        self.clock.tick(FPS)
        self.update()
        self.screen.fill((0, 0, 0))

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)

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

    def _quit(self):
        pygame.quit()
        exit()

    def run(self):
        self.init()
        while self.running:
            self._update()
            self._handle_events()
            self.draw()
        self._quit()