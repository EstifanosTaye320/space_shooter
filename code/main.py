import pygame
from os.path import join
from random import randint

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1289, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# plain surface
surf = pygame.Surface((100, 200))
surf.fill("orange") # not in the loop

# imports
player_surface = pygame.image.load(join("images", "player.png")).convert_alpha()
player_rect = player_surface.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
player_direction = pygame.math.Vector2(0, 0)
player_speed = 300

star_surface = pygame.image.load(join("images", "star.png")).convert_alpha()
star_locs = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

meteor_surface = pygame.image.load(join("images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surface.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surface = pygame.image.load(join("images", "laser.png")).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

# main loop
while running:
    dt = clock.tick() / 1000
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     print(event.type)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos

    # input
    # print(pygame.mouse.get_rel())
    keys = pygame.key.get_pressed()
    just_pressed = pygame.key.get_just_pressed()

    # draw game
    display_surface.fill("darkgrey") # reset screen
    for loc in star_locs:
        display_surface.blit(star_surface, loc)        
    
    display_surface.blit(meteor_surface, meteor_rect)
    display_surface.blit(laser_surface, laser_rect)

    # player actions
    if just_pressed[pygame.K_SPACE]:
        print("fire laser")

    # player movement
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    player_direction = player_direction.normalize() if bool(player_direction) else player_direction
    player_rect.center += player_direction*player_speed*dt
    display_surface.blit(player_surface, player_rect)

    # update screen
    pygame.display.update()

pygame.quit()