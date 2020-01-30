#!/usr/bin/env python3

import pygame
import random
import soldier

# Define the screen parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (210, 0, 0)
BLUE = (30, 144, 255)
GREEN = (50, 205, 50)

pygame.init()  # Initialize the pygame module

# Setup the soliders
red_soldier_list = pygame.sprite.Group()  # Add all of the red soldiers created into a list
blue_soldier_list = pygame.sprite.Group()  # Add all of the blue soldiers created into a list
total_soldier_list = pygame.sprite.Group()  # Add both of the soldiers to a total list to move all of them

# Display the red soldiers
for i in range(10):
    red_soldier = soldier.Soldier(RED)

    # Spawn the soldiers randomly on the left side of the screen
    red_soldier.rect.x = random.randrange(red_soldier.r * 2, (SCREEN_WIDTH * 0.5) - red_soldier.r * 2)
    red_soldier.rect.y = random.randrange(red_soldier.r * 2, SCREEN_HEIGHT - red_soldier.r * 2)

    red_soldier_list.add(red_soldier)
    total_soldier_list.add(red_soldier)

# Display the blue soldiers
for i in range(10):
    blue_soldier = soldier.Soldier(BLUE)

    # Spawn the soldiers randomly on the right side of the screen
    blue_soldier.rect.x = random.randrange(SCREEN_WIDTH * 0.5 + blue_soldier.r * 2, SCREEN_WIDTH - blue_soldier.r * 2)
    blue_soldier.rect.y = random.randrange(blue_soldier.r * 2, SCREEN_HEIGHT - blue_soldier.r * 2)

    blue_soldier_list.add(blue_soldier)
    total_soldier_list.add(blue_soldier)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Battle Simulator")

clock = pygame.time.Clock()  # Setup the clock


def run():
    done = False  # Loop until user clicks the close button
    turn = 2  # Used to check which teams turn it is

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)
        total_soldier_list.draw(screen)

        if turn % 2 == 0:
            for blue_soldier in blue_soldier_list:
                # Checks all of the red soldiers that collide with the blue soldier going through the loop
                blue_hit_list = pygame.sprite.spritecollide(blue_soldier, red_soldier_list, False)
                # Checks if list is empty or not and attacks the first soldier encountered
                if blue_hit_list:
                    blue_attack = random.randint(1, 4)

                    if blue_attack == 1:
                        blue_soldier.light_attack(screen, blue_hit_list[0])
                    elif blue_attack == 2:
                        blue_soldier.heavy_attack(screen, blue_hit_list[0])
                    elif blue_attack == 3:
                        blue_soldier.heal(screen)
                    elif blue_attack == 4:
                        blue_soldier.retreat(screen)

                    pygame.time.wait(50)
                # elif (len(red_soldier_list.sprites()) > 0):
                #     random_red = random.randint(0, len(red_soldier_list.sprites()) - 1)
                #     blue_soldier.offense(red_soldier_list.sprites()[random_red], blue_soldier_list)
                else:
                    blue_soldier.move()
        else:
            for red_soldier in red_soldier_list:
                red_hit_list = pygame.sprite.spritecollide(red_soldier, blue_soldier_list, False)
                if red_hit_list:
                    red_attack = random.randint(1, 4)

                    if red_attack == 1:
                        red_soldier.light_attack(screen, red_hit_list[0])
                    elif red_attack == 2:
                        red_soldier.heavy_attack(screen, red_hit_list[0])
                    elif red_attack == 3:
                        red_soldier.heal(screen)
                    elif red_attack == 4:
                        red_soldier.retreat(screen)

                    pygame.time.wait(50)
                # elif (len(blue_soldier_list.sprites()) > 0):
                #     random_blue = random.randint(0, len(blue_soldier_list.sprites()) - 1)
                #     red_soldier.offense(blue_soldier_list.sprites()[random_blue], red_soldier_list)
                else:
                    red_soldier.move()

        pygame.display.flip()
        clock.tick(60)
        turn += 1

    pygame.quit()
