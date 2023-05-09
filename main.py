import pygame
from pygame.event import Event
from pygame.locals import *

BLOCK_SIZE = 100

vec = pygame.math.Vector2

ACC = 0.5
FRIC = -0.12

# Define the screen size (width and height)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 60
FramePerSec = pygame.time.Clock()

MAP = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1]]


class GeometryCrash:

    def __init__(self):

        pygame.init()  # Init PyGame

        # Set up the window
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Geometry Crash - by En0ri4n")

        # Set up map view
        self.map_x = 0

        # Set up the player
        self.player = Player(self)

        self.platforms = pygame.sprite.Group()
        self.platforms.add(Tile())

        self.running = True

        while self.running:
            self.loop()

        # If not running, quit all
        pygame.quit()

    def loop(self):
        for current_event in pygame.event.get():
            self.on_event(current_event)  # Listen for all events

        self.player.move()

        self.update()

        self.render()

        pygame.display.update()

        FramePerSec.tick(FPS)

    def update(self):
        platforms_hit = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if platforms_hit:
            self.player.pos.y = platforms_hit[0].rect.top + 1
            self.player.vel.y = 0

        self.map_x = 0

    def render(self):

        # Background (white)
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.player.surf, self.player.rect)

        for platform in self.platforms:
            self.screen.blit(platform.surf, platform.rect)

        # Draw time !
        # pygame.draw.polygon(self.screen, (0, 0, 255), ((10, 10), (10, 20), (20, 20), (20, 10)))

        # Update screen
        pygame.display.flip()

    def on_event(self, current_event: Event):

        if current_event.type == KEYDOWN:  # When the user hit a key
            if current_event.key == K_ESCAPE:  # If this is the escape key, stop the loop
                self.running = False

            self.player.on_key(current_event.key)

        if current_event.type == pygame.QUIT:
            self.running = False
        pass


class Player(pygame.sprite.Sprite):

    def __init__(self, game: GeometryCrash):
        super().__init__()
        self.game = game
        self.surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.surf.fill((128, 200, 200))
        self.rect = self.surf.get_rect()

        self.pos = vec((SCREEN_WIDTH / 2, 50))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self):
        self.acc = vec(0, 0.5)

        self.vel += self.acc
        self.pos += self.vel + 0.8 * self.acc
        self.rect.midbottom = self.pos

    def on_key(self, key):
        if key == K_SPACE:
            self.jump()
        pass

    def jump(self):
        self.vel.y = -12
        pass


class Tile(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.surf.fill((255, 0, 0))
        self.surf.fill((100, 0, 0), (3, 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - BLOCK_SIZE / 2))


GeometryCrash()
