import pygame
from os.path import join
from random import randint, uniform, choice

# sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 400
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 300

    def laster_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self, dt, *args, **kwargs):
        just_pressed = pygame.key.get_just_pressed()
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction*self.speed*dt
        
        if just_pressed[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            Lazer(laser_surface, self.rect.midtop, all_sprites, lazer_sprites)
            laser_sound.play()

        self.laster_timer()

        return super().update(*args, **kwargs)

class Star(pygame.sprite.Sprite):
    def __init__(self, image, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Lazer(pygame.sprite.Sprite):
    def __init__(self, surf, pos, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt, *args, **kwargs):
        self.rect.centery -= 400*dt
        
        if self.rect.bottom < 0:
            self.kill()
        
        return super().update(*args, **kwargs)

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, *groups):
        super().__init__(*groups)
        self.original_image = surf
        self.image = self.original_image
        self.pos = (randint(0, WINDOW_WIDTH), randint(-200, -100))
        self.rect = self.image.get_frect(center=self.pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.math.Vector2((uniform(-0.5, 0.5), 1))
        self.speed = randint(400, 500)
        self.rotation_speed = randint(50, 70)
        self.rotation_direction = choice((-1, 1))
        self.rotation = 0

    def update(self, dt, *args, **kwargs):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        self.rotation += self.rotation_direction * self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)
        return super().update(*args, **kwargs)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, *groups):
        super().__init__(*groups)
        self.image = frames[0]
        self.rect = self.image.get_frect(center=pos)
        self.frames = frames
        self.current_index = 0
        explosion_sound.play()

    def update(self, dt, *args, **kwargs):
        self.current_index += 40 * dt
        if self.current_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.current_index)]

        return super().update(*args, **kwargs)

# collisions
def collision():
    global running
    for lazer in lazer_sprites:
        if pygame.sprite.spritecollide(lazer, meteor_sprites, True):
            AnimatedExplosion(frames, lazer.rect.midtop, all_sprites)
            lazer.kill()

    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        running = False

# display score
def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(40, 10).move(0, -8), 5, 10)
    display_surface.blit(text_surf, text_rect)

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1289, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# sprite groups
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
lazer_sprites = pygame.sprite.Group()

# imports
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
laser_surface = pygame.image.load(join("images", "laser.png")).convert_alpha()
meteor_surface = pygame.image.load(join("images", "meteor.png")).convert_alpha()
font = pygame.font.Font(join("images", "Oxanium-Bold.ttf"), 50)
frames = [pygame.image.load(join("images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join("audio", "laser.wav"))
laser_sound.set_volume(0.1)

explosion_sound = pygame.mixer.Sound(join("audio", "explosion.wav"))
explosion_sound.set_volume(0.1)

game_music_sound = pygame.mixer.Sound(join("audio", "game_music.wav"))
game_music_sound.set_volume(0.1)
game_music_sound.play(loops=-1)

# objects
player = Player(all_sprites)
for _ in range(20):
    Star(star_surf, all_sprites)

# custom event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 200)

# main loop
while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surface, all_sprites, meteor_sprites)


    display_surface.fill("#3e2e3e")
    all_sprites.update(dt)

    collision()
    display_score()
        
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()