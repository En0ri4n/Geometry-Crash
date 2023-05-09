import pygame
from pygame.event import Event
from pygame.locals import *
import math

BLOCK_SIZE = 50

vec = pygame.math.Vector2

ACC = 0.5
FRIC = -0.12

# Define the screen size (width and height)
WIDTH_COUNT = 15
HEIGHT_COUNT = 10
SCREEN_WIDTH = WIDTH_COUNT * BLOCK_SIZE
SCREEN_HEIGHT = HEIGHT_COUNT * BLOCK_SIZE

FPS = 60
FramePerSec = pygame.time.Clock()

MAP = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


# noinspection PyTypeChecker
class GeometryCrash:

    def __init__(self):

        pygame.init()  # Init PyGame

        # Set up the window
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Geometry Crash - by En0ri4n")

        # Set up map view
        self.map_x = 0.0

        # Set up the player
        self.player = Player(self, SCREEN_WIDTH / 2, 0)

        self.platforms = pygame.sprite.Group()

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
            if platforms_hit[0].rect.left < self.player.rect.right:
                self.death()
            elif platforms_hit[0].rect.top < self.player.rect.bottom:
                self.player.pos.y = platforms_hit[0].rect.top + 1
                self.player.vel.y = 0
                self.player.jumping = False

        self.platforms.empty()

        for y in range(len(MAP)):
            for x in range(len(MAP[0])):
                if MAP[y][x] == 1 and self.is_tile_visible(x):
                    self.platforms.add(Tile(self, self.get_map_offset() + x * BLOCK_SIZE, y * BLOCK_SIZE))

        self.map_x += 3

    def is_tile_visible(self, x):
        return self.map_x - BLOCK_SIZE < x * BLOCK_SIZE <= self.map_x + SCREEN_WIDTH

    def get_map_offset(self):
        return -self.map_x

    def get_current_tile_index(self, x) -> int:
        return math.floor(self.map_x / BLOCK_SIZE) + x

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

    def death(self):
        self.map_x = 0
        self.player.set_pos(10, SCREEN_HEIGHT / 2)


class Player(pygame.sprite.Sprite):

    def __init__(self, game: GeometryCrash, x, y):
        super().__init__()
        self.game = game
        self.surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.surf.fill((128, 200, 200))
        self.rect = self.surf.get_rect()

        self.pos = vec((x, y))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.jumping = False

    def move(self):
        self.acc = vec(0, 0.5)  # Gravity

        self.vel += self.acc
        self.pos += self.vel + 0.8 * self.acc
        self.rect.midbottom = self.pos

    def on_key(self, key):
        if key == K_SPACE:
            self.jump()
        pass

    def jump(self):
        if not self.jumping:
            self.vel.y = -12
            self.jumping = True

    def set_pos(self, x, y):
        self.pos = vec((x, y))
        pass


class Tile(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()
        self.surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.surf.fill((255, 0, 0))
        self.surf.fill((100, 0, 0), (3, 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))
        self.rect = self.surf.get_rect(center=(x + BLOCK_SIZE / 2, y + BLOCK_SIZE / 2))


GeometryCrash()
