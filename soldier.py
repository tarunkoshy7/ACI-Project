#!/usr/bin/env python3
# This class defines the properties of a soldier

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
        pygame.sprite.Sprite.__init__(self)  # Sprite module in pygame makes it easier to handle collision mechanics

        self.health = 100
        self.r = 15
        self.vel = 10
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
        # Function for random movement

        num = random.randint(1, 5)

        if(num == 1 and self.rect.y < SCREEN_HEIGHT - (4 * self.r) - self.vel * 2):
            self.rect.y += self.vel
        elif(num == 2 and self.rect.y > self.vel * 2):
            self.rect.y -= self.vel
        elif(num == 3 and self.rect.x > self.vel * 2.5):
            self.rect.x -= self.vel
        elif(num == 4 and self.rect.x < SCREEN_WIDTH - (4 * self.r) - self.vel * 2):
            self.rect.x += self.vel

    def offense(self, other, allies):
        # Function for aggressive movement

        hit = pygame.sprite.spritecollide(self, allies, False)

        if (other.rect.x > self.rect.x and other.rect.x < SCREEN_WIDTH - (4 * self.r) - self.vel):
            self.rect.x += self.vel
        elif (other.rect.x < self.rect.x and other.rect.x > self.vel):
            self.rect.x -= self.vel
        if (other.rect.y > self.rect.y and other.rect.y < SCREEN_HEIGHT - (4 * self.r) - self.vel):
            self.rect.y += self.vel
        elif(other.rect.y < self.rect.y and other.rect.y > self.vel):
            self.rect.y -= self.vel
        elif(len(hit) >= 2):
            self.move()

    def display_message(self, screen, attack):
        font = pygame.font.SysFont('Papyrus', 18, True)
        text = font.render(attack, False, WHITE)
        textrect = text.get_rect()
        textrect.center = (self.rect.x + self.r * 2), (self.rect.y + self.r * 4)
        screen.blit(text, textrect)

    def light_attack(self, screen, other):
        num = random.randint(1, 10)

        if num <= 9:
            other.health -= 20
            other.healthbar()
            self.display_message(screen, "Light Attack")

            if other.health <= 0:
                other.health = 0
                other.kill()
            return True
        else:
            self.display_message(screen, "Attack Missed")
            return False

    def heavy_attack(self, screen, other):
        num = random.randint(1, 10)

        if num <= 6:
            other.health -= 35
            other.healthbar()
            self.display_message(screen, "Heavy Attack")

            if other.health < 0:
                other.health = 0
                other.kill()
            return True
        else:
            self.display_message(screen, "Attack Missed")
            return False

    def heal(self, screen):
        num = random.randint(1, 10)

        if num <= 8:
            self.health += 25

            if self.health > 100:
                self.health = 100

            self.healthbar()
            self.display_message(screen, "Healed")
            return True
        else:
            self.display_message(screen, "Heal Failed")
            return False

    def retreat(self, screen):
        num = random.randint(1, 10)

        if num <= 5:
            if (self.color == BLUE and self.rect.x < SCREEN_WIDTH - (4 * self.r) - (self.vel * 8)):
                self.rect.x += self.vel * 8
                self.display_message(screen, "Retreat")
            elif(self.color == RED and self.rect.x > (self.vel * 8)):
                self.rect.x -= self.vel * 8
                self.display_message(screen, "Retreat")
            return True
        else:
            self.display_message(screen, "Retreat Failed")
            return False

    def getPosition(self):
        return (int(round(self.rect.x, -1)), int(round(self.rect.y, -1)))
