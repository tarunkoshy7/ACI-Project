#!/usr/bin/env python3

import pygame
import random

# Define the screen parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (210, 0, 0)
BLUE = (30, 144, 255)
GREEN = (50, 205, 50)


class Soldier(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)

        self.health = 100
        self.r = 15
        self.vel = 15
        self.color = color

        self.image = pygame.Surface([self.r * 4, self.r * 4])  # Set the dimensions for the image
        self.image.set_colorkey(BLACK)  # Make background transparent
        pygame.draw.circle(self.image, self.color, (self.r * 2, self.r * 2), self.r)
        self.rect = self.image.get_rect()  # Object that gets the position of the image

        pygame.draw.rect(self.image, GREEN, (self.r - 9, self.r - 9, 50, 6))  # Draw the initial healthbar

    def healthbar(self):
        # Red healthbar overlaps green one that was previously drawn
        pygame.draw.rect(self.image, RED, (self.r - 9, self.r - 9, 50, 6))
        # Variable green healthbar that gets updated over the red heathbar depending on the health of the soldier
        pygame.draw.rect(self.image, GREEN, (self.r - 9, self.r - 9, (0.5 * self.health), 6))

    def move(self):
        # TODO: Figure out how to move without hitting anyone else
        num = random.randint(1, 5)

        if (num == 1 and self.rect.x < SCREEN_WIDTH - (4 * self.r) - self.vel):
            self.rect.x += self.vel
        elif (num == 2 and self.rect.y < SCREEN_HEIGHT - (4 * self.r) - self.vel):
            self.rect.y += self.vel
        elif (num == 3 and self.rect.x > self.vel):
            self.rect.x -= self.vel
        elif (num == 4 and self.rect.y > self.vel):
            self.rect.y -= self.vel

    def display_message(self, attack):
        font = pygame.font.SysFont('Papyrus', 18, True)
        text = font.render(attack, False, WHITE)
        textrect = text.get_rect()
        textrect.center = (self.rect.x + self.r * 2), (self.rect.y + self.r * 4)
        screen.blit(text, textrect)

    def light_attack(self, other):
        num = random.randint(1, 10)

        if num <= 8:
            other.health -= random.randint(18, 25)
            other.healthbar()
            self.display_message("Light Attack")

            if other.health <= 0:
                other.health = 0
                other.kill()
        else:
            self.display_message("Attack Missed")

    def heavy_attack(self, other):
        num = random.randint(1, 10)

        if num <= 8:
            other.health -= random.randint(10, 35)
            other.healthbar()
            self.display_message("Heavy Attack")

            if other.health < 0:
                other.health = 0
                other.kill()
        else:
            self.display_message("Attack Missed")

    def heal(self):
        num = random.randint(1, 10)

        if num <= 8:
            self.health += random.randint(18, 25)

            if self.health > 100:
                self.health = 100

            self.healthbar()
            self.display_message("Healed")
        else:
            self.display_message("Heal Failed")

    def retreat(self):
        num = random.randint(1, 10)

        if num <= 5:
            if (self.color == BLUE and self.rect.x < SCREEN_WIDTH - (4 * self.r) - (self.vel * 8)):
                self.rect.x += self.vel * 8
                self.display_message("Retreat")
            elif(self.color == RED and self.rect.x > (self.vel * 8)):
                self.rect.x -= self.vel * 8
                self.display_message("Retreat")
        else:
            self.display_message("Retreat Failed")


"""
--------------- Setup ----------------
"""
# Setup the soliders
red_soldier_list = pygame.sprite.Group()  # Add all of the red soldiers created into a list
blue_soldier_list = pygame.sprite.Group()  # Add all of the blue soldiers created into a list
total_soldier_list = pygame.sprite.Group()  # Add both of the soldiers to a total list to move all of them

# Display the red soldiers
for i in range(10):
    red_soldier = Soldier(RED)

    # Spawn the soldiers randomly on the left side of the screen
    red_soldier.rect.x = random.randrange(red_soldier.r * 2, (SCREEN_WIDTH * 0.5) - red_soldier.r * 2)
    red_soldier.rect.y = random.randrange(red_soldier.r * 2, SCREEN_HEIGHT - red_soldier.r * 2)

    red_soldier_list.add(red_soldier)
    total_soldier_list.add(red_soldier)

# Display the blue soldiers
for i in range(10):
    blue_soldier = Soldier(BLUE)

    # Spawn the soldiers randomly on the right side of the screen
    blue_soldier.rect.x = random.randrange(SCREEN_WIDTH * 0.5 + blue_soldier.r * 2, SCREEN_WIDTH - blue_soldier.r * 2)
    blue_soldier.rect.y = random.randrange(blue_soldier.r * 2, SCREEN_HEIGHT - blue_soldier.r * 2)

    blue_soldier_list.add(blue_soldier)
    total_soldier_list.add(blue_soldier)

pygame.init()

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Battle Simulator")

clock = pygame.time.Clock()  # Setup the clock

"""
--------------- Main Program ---------------
"""
# TODO: Put this all into a game class so more organized

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
                    blue_soldier.light_attack(blue_hit_list[0])
                elif blue_attack == 2:
                    blue_soldier.heavy_attack(blue_hit_list[0])
                elif blue_attack == 3:
                    blue_soldier.heal()
                elif blue_attack == 4:
                    blue_soldier.retreat()

                pygame.time.wait(400)
            else:
                blue_soldier.move()
    else:
        for red_soldier in red_soldier_list:
            red_hit_list = pygame.sprite.spritecollide(red_soldier, blue_soldier_list, False)
            if red_hit_list:
                red_attack = random.randint(1, 4)

                if red_attack == 1:
                    red_soldier.light_attack(red_hit_list[0])
                elif red_attack == 2:
                    red_soldier.heavy_attack(red_hit_list[0])
                elif red_attack == 3:
                    red_soldier.heal()
                elif red_attack == 4:
                    red_soldier.retreat()

                pygame.time.wait(400)
            else:
                red_soldier.move()

    pygame.display.flip()
    clock.tick(60)
    turn += 1
    pygame.time.wait(50)

pygame.quit()
