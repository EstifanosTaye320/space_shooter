import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 300
    
    def update(self, dt, *args, **kwargs):
        just_pressed = pygame.key.get_just_pressed()
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction*self.speed*dt
        
        if just_pressed[pygame.K_SPACE]:
            print("fire lazer")

        return super().update(*args, **kwargs)

class Star(pygame.sprite.Sprite):
    def __init__(self, image, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1289, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
for _ in range(20):
    Star(star_surf, all_sprites)
    
player = Player(all_sprites)

# meteor_surface = pygame.image.load(join("images", "meteor.png")).convert_alpha()
# meteor_rect = meteor_surface.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

# laser_surface = pygame.image.load(join("images", "laser.png")).convert_alpha()
# laser_rect = laser_surface.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("darkgrey")
    all_sprites.update(dt)
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()