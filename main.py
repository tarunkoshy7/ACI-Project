#!/usr/bin/env python3

import pygame
import random


class Soldier(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)

        self.health = 100
        self.r = 15
        self.vel = 10
        self.color = color

        self.image = pygame.Surface([self.r * 2, self.r * 2])  # Set the dimensions for the image
        self.image.set_colorkey(BLACK)  # Make background transparent
        pygame.draw.circle(self.image, self.color, (self.r, self.r), self.r)
        self.rect = self.image.get_rect()

    def move():
        pass

    def attack1():
        pass

    def attack2():
        pass

    def heal():
        pass

    def retreat():
        pass


"""
--------------- Setup ----------------
"""
# Define the screen parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (210, 0, 0)
BLUE = (30, 144, 255)

# Setup the soliders
red_soldier_list = pygame.sprite.Group()
blue_soldier_list = pygame.sprite.Group()
total_soldier_list = pygame.sprite.Group()

for i in range(10):
    red_soldier = Soldier(RED)

    red_soldier.rect.x = random.randrange(red_soldier.r * 2, (SCREEN_WIDTH * 0.5) - red_soldier.r * 2)
    red_soldier.rect.y = random.randrange(red_soldier.r * 2, SCREEN_HEIGHT - red_soldier.r * 2)

    red_soldier_list.add(red_soldier)
    total_soldier_list.add(red_soldier)

for i in range(10):
    blue_soldier = Soldier(BLUE)

    blue_soldier.rect.x = random.randrange(SCREEN_WIDTH * 0.5 + blue_soldier.r * 2, SCREEN_WIDTH - blue_soldier.r * 2)
    blue_soldier.rect.y = random.randrange(blue_soldier.r * 2, SCREEN_HEIGHT - blue_soldier.r * 2)

    blue_soldier_list.add(blue_soldier)
    total_soldier_list.add(blue_soldier)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Battle Simulator")

clock = pygame.time.Clock()

"""
--------------- Main Program ---------------
"""
done = False  # Loop until user clicks the close button

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic goes here ---

    # --- Screen clearing goes here ---
    screen.fill(BLACK)

    # --- Drawing code goes here ---
    total_soldier_list.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
