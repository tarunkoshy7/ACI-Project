#!/usr/bin/env python3

import pygame
import fully_observable
import partially_observable
import no_intelligence

# Define the screen parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Option:
    hovered = False

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (WHITE)
        else:
            return (100, 100, 100)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


def openFile():
    if option.text == "Fully Observable Environment":
        fully_observable.run()
    if option.text == "Partially Observable Environment":
        partially_observable.run()
    if option.text == "Random":
        no_intelligence.run()


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Battle Simulator")
menu_font = pygame.font.SysFont('Papyrus', 40, True)
options = [Option("Fully Observable Environment", (150, SCREEN_HEIGHT * 1/4)),
           Option("Partially Observable Environment", (120, SCREEN_HEIGHT * 1/2)),
           Option("Random", (350, SCREEN_HEIGHT * 3/4))]

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.event.pump()
    screen.fill(BLACK)

    for option in options:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
        else:
            option.hovered = False

        if option.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            openFile()
            done = True

        option.draw()
        pygame.display.flip()
