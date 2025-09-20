import pygame
from obj import Obj
from random import randint
from bird import Bird

pygame.init()

# Dimensions of the screen
width = 360
height = 640

# Movement speed of the sprites
animation_speed = 4
fall_speed = 4

# Gravity force applied to the bird
gravity = 1

# Game state
is_playing = True

# Game window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

# Background
bg = Obj('sprites/flappybird-city-day.png', 0, 0, width, height)

# Bird
bird = Bird("sprites/flappybird-down-red.png", width / 4, height / 2, int(width / 6), int(height / 10))

pipe_y = randint(-180, 0)

# Pipes and coin
pipe = Obj("sprites/block-green.png", width, pipe_y, int(width / 5), int(height / 2.5))
coin = Obj('sprites/gold.png', pipe.sprite.rect[0] + 14, pipe_y + 325, int(width / 8), int(height / 13))
pipe2 = Obj("sprites/block-green.png", width, pipe_y + 450, int(width / 5), int(height / 2.5))

# Ground
ground = Obj("sprites/flappy-bird-base.png", 0, int(height - height / 5), width, int(height / 5))
ground2 = Obj("sprites/flappy-bird-base.png", width, int(height - height / 5), width, int(height / 5))

score = 0

def Draw():
    pygame.font.init()
    font_default = pygame.font.get_default_font()
    font_size = pygame.font.SysFont(font_default, 38, True)
    score_text = "{}".format(str(score))
    score_render = font_size.render(score_text, True, (255, 255, 255))

    window.blit(bg.sprite.image, bg.sprite.rect)
    window.blit(bird.sprite.image, bird.sprite.rect)
    window.blit(pipe.sprite.image, pipe.sprite.rect)
    window.blit(coin.sprite.image, coin.sprite.rect)
    window.blit(pygame.transform.flip(pipe2.sprite.image, False, True), pipe2.sprite.rect)
    window.blit(score_render, (int(width / 2), int(height / 15)))
    window.blit(ground.sprite.image, ground.sprite.rect)
    window.blit(ground2.sprite.image, ground2.sprite.rect)

    if is_playing:
        # Move the ground
        ground.sprite.rect[0] -= animation_speed
        ground2.sprite.rect[0] -= animation_speed
        if ground.sprite.rect[0] == -width:
            ground.sprite.rect[0] = 0
        if ground2.sprite.rect[0] == 0:
            ground2.sprite.rect[0] = width

        # Move coin
        coin.sprite.rect[0] -= animation_speed

        # Move pipes
        pipe.sprite.rect[0] -= animation_speed
        pipe2.sprite.rect[0] -= animation_speed
        if pipe.sprite.rect[0] == -100:
            pipe.sprite.rect[0] = width
            pipe2.sprite.rect[0] = width
            coin.sprite.rect[0] = pipe.sprite.rect[0] + 14
            pipe_y = randint(-180, 0)
            pipe.sprite.rect[1] = pipe_y
            pipe2.sprite.rect[1] = pipe_y + 450
            coin.sprite.rect[1] = pipe_y + 325

        # Bird falling animation
        bird.sprite.rect[1] += fall_speed
        if bird.sprite.rect[1] >= ground.sprite.rect[1] - bird.sprite.rect[3]:
            bird.sprite.rect[1] = ground.sprite.rect[1] - bird.sprite.rect[3]

    else:
        # Display restart message
        font_restart = pygame.font.SysFont(None, 36)
        text_restart = font_restart.render("Click anywhere to restart", True, (255, 0, 0))
        text_rect = text_restart.get_rect(center=(width // 2, height // 2))
        window.blit(text_restart, text_rect)

def Collision():
    global score, is_playing

    hit_pipe = pygame.sprite.spritecollide(bird.sprite, pipe.group, False)
    hit_pipe2 = pygame.sprite.spritecollide(bird.sprite, pipe2.group, False)
    hit_coin = pygame.sprite.spritecollide(bird.sprite, coin.group, False)

    if hit_pipe or hit_pipe2:
        is_playing = False
    elif hit_coin:
        score += 1
        coin.sprite.rect[1] = -50  # Move coin out of view

# FPS
clock = pygame.time.Clock()

# Main loop
loop = True
while loop:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            if is_playing:
                if bird.sprite.rect[1] > 10:
                    fall_speed += 12 * -1
            else:
                # Restart game
                is_playing = True
                bird.sprite.rect[1] = height // 2
                pipe_y = randint(-180, 0)
                pipe.sprite.rect[0] = width
                pipe.sprite.rect[1] = pipe_y
                pipe2.sprite.rect[0] = width
                pipe2.sprite.rect[1] = pipe_y + 450
                coin.sprite.rect[0] = pipe.sprite.rect[0] + 14
                coin.sprite.rect[1] = pipe_y + 325
                score = 0
                fall_speed = 4


    # Apply gravity
    if fall_speed < 10:
        fall_speed += gravity
    elif fall_speed > 10:
        fall_speed = 1

    # Prevent bird from flying off the top
    if bird.sprite.rect[1] < 0:
        bird.sprite.rect[1] = 0
        fall_speed = 4

    if is_playing:
        Draw()
        Collision()
        bird.Upade_anim()
    else:
        Draw()

    pygame.display.update()
