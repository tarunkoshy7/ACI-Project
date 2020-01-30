#!/usr/bin/env python3

import pygame
import random
import soldier
import numpy as np
from math import sqrt, pow
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
VELOCITY = 10
RADIUS = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (210, 0, 0)
BLUE = (30, 144, 255)
GREEN = (50, 205, 50)

# CHANGE NUMBER OF SOLDIERS HERE
numberOfRedSoldiers = 10
numberOfBlueSoldiers = 10

actionSpace = {1: "up", 2: "down", 3: "left", 4: "right", 5: "light attack", 6: "heavy attack", 7: "heal",
               8: "retreat"}
stateSpace = dict()

count = 1
for i in range(int((SCREEN_WIDTH - (4 * RADIUS) - VELOCITY) / VELOCITY)):
    for j in range(int((SCREEN_HEIGHT - (4 * RADIUS) - VELOCITY) / VELOCITY)):
        stateSpace[count] = ((VELOCITY + (i * VELOCITY), VELOCITY + (j * VELOCITY)))
        count += 1

stateSpace[count] = "combat 75+"
count += 1
stateSpace[count] = "combat 35+"
count += 1
stateSpace[count] = "combat 0+"

qTable = np.zeros((len(stateSpace), len(actionSpace)))

pygame.init()  # Initialize the pygame module

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Battle Simulator")

clock = pygame.time.Clock()  # Setup the clock

# Setup the soliders
red_soldier_list = pygame.sprite.Group()  # Add all of the red soldiers created into a list
blue_soldier_list = pygame.sprite.Group()  # Add all of the blue soldiers created into a list
total_soldier_list = pygame.sprite.Group()  # Add both of the soldiers to a total list to move all of them


def setup():
    # Display the red soldiers
    for i in range(numberOfRedSoldiers):
        red_soldier = soldier.Soldier(RED)

        # Spawn the soldiers randomly on the left side of the screen
        red_soldier.rect.x = random.randrange(int(round(stateSpace[1][0], -1)),
                                              int(round(stateSpace[int(len(stateSpace) / 2)][0], -1)))
        red_soldier.rect.y = random.randrange(int(round(stateSpace[1][1], -1)),
                                              int(round(stateSpace[int(len(stateSpace) - 3)][1], -1)))

        red_soldier_list.add(red_soldier)
        total_soldier_list.add(red_soldier)

    # Display the blue soldiers
    for i in range(numberOfBlueSoldiers):
        blue_soldier = soldier.Soldier(BLUE)

        # Spawn the soldiers randomly on the right side of the screen
        blue_soldier.rect.x = random.randrange(int(round(stateSpace[int(len(stateSpace) / 2)][0], -1)),
                                               int(round(stateSpace[int(len(stateSpace) - 3)][0], -1)))
        blue_soldier.rect.y = random.randrange(int(round(stateSpace[1][1], -1)),
                                               int(round(stateSpace[int(len(stateSpace) - 3)][1], -1)))

        blue_soldier_list.add(blue_soldier)
        total_soldier_list.add(blue_soldier)


def getState(soldier):
    collision = pygame.sprite.spritecollide(soldier, blue_soldier_list, False)

    if(collision and soldier.health >= 75):
        return 3870
    elif(collision and soldier.health >= 35):
        return 3871
    elif(collision and soldier.health >= 0):
        return 3872
    else:
        return list(stateSpace.keys())[list(stateSpace.values()).index((soldier.getPosition()))]


def doAction(soldier, currentAction):
    collision = pygame.sprite.spritecollide(soldier, blue_soldier_list, False)

    if collision:
        oldEnemyHealth = collision[0].health
    else:
        oldEnemyHealth = 0

    oldSoldierHealth = soldier.health

    if(currentAction == 1 and soldier.rect.y < SCREEN_HEIGHT - (4 * soldier.r) - soldier.vel * 2):
        soldier.rect.y += soldier.vel
    elif(currentAction == 2 and soldier.rect.y > soldier.vel * 2):
        soldier.rect.y -= soldier.vel
    elif(currentAction == 3 and soldier.rect.x > soldier.vel * 2.5):
        soldier.rect.x -= soldier.vel
    elif(currentAction == 4 and soldier.rect.x < SCREEN_WIDTH - (4 * soldier.r) - soldier.vel * 2):
        soldier.rect.x += soldier.vel
    elif(currentAction == 5 and collision):
        soldier.light_attack(screen, collision[0])
    elif(currentAction == 6 and collision):
        soldier.heavy_attack(screen, collision[0])
    elif(currentAction == 7 and collision):
        soldier.heal(screen)
    elif(currentAction == 8 and collision):
        soldier.retreat(screen)

    return oldEnemyHealth, oldSoldierHealth


def rewardFunction(soldier, oldEnemyHealth, oldSoldierHealth, currentAction, currentState):
    # CHANGE THE REWARD GIVEN HERE
    reward = 0
    collision = pygame.sprite.spritecollide(soldier, blue_soldier_list, False)

    if(stateSpace[currentState] == "combat 75+"):
        # in this state, we want to maximize the damage dealt
        if collision:
            reward += (oldEnemyHealth - collision[0].health) * 10

        if reward == 0:
            reward -= 10

    elif(stateSpace[currentState] == "combat 35+"):
        # either healing or attacking is acceptable here
        if collision:
            reward += (oldEnemyHealth - collision[0].health) * 10
            reward += (soldier.health - oldSoldierHealth) * 10

        if(currentAction == 8 and soldier.retreat):
            # retreat reward manually assigned since no way to classify in terms of health
            reward += 10

        if reward == 0:
            reward -= 10

    elif(stateSpace[currentState] == "combat 0+"):
        # the priority here is to stay alive
        if collision:
            reward += (soldier.health - oldSoldierHealth) * 10

        if(currentAction == 8 and soldier.retreat):
            reward += 20

        if reward == 0:
            reward -= 10

    elif(blue_soldier_list):
        xMinDistance = 10000
        yMinDistance = 10000

        # closestEnemy = random.choice(blue_soldier_list.sprites())
        for blue_soldier in blue_soldier_list:
            xDistance = sqrt(pow(blue_soldier.rect.x - soldier.rect.x, 2))
            yDistance = sqrt(pow(blue_soldier.rect.y - soldier.rect.y, 2))
            if(xDistance < xMinDistance and yDistance < yMinDistance):
                xMinDistance = xDistance
                yMinDistance = yDistance
                closestEnemy = blue_soldier

        if(currentAction == 1):
            if(closestEnemy.rect.y > soldier.rect.y):
                reward += 1
            else:
                reward -= 20
        elif(currentAction == 2):
            if(closestEnemy.rect.y < soldier.rect.y):
                reward += 1
            else:
                reward -= 20
        elif(currentAction == 3):
            if(closestEnemy.rect.x < soldier.rect.x):
                reward += 1
            else:
                reward -= 20
        elif(currentAction == 4):
            if(closestEnemy.rect.x > soldier.rect.x):
                reward += 1
            else:
                reward -= 20
        elif(currentAction == 5 or 6 or 7 or 8):
            reward -= 150

    return reward


def train(soldier):
    # CHANGE Q-LEARNING PARAMETERS HERE
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1
    currentState = getState(soldier)

    if(stateSpace[currentState] == "combat 75+" or "combat 35+" or "combat 0+"):
        if(random.uniform(0, 1) < epsilon):
            currentAction = random.randint(5, 8)
        else:
            currentAction = np.argmax(qTable[currentState - 1]) + 1
    else:
        if(random.uniform(0, 1) < epsilon):
            currentAction = random.randint(1, 4)
        else:
            currentAction = np.argmax(qTable[currentState - 1]) + 1

    oldEnemyHealth, oldSoldierHealth = doAction(soldier, currentAction)

    reward = rewardFunction(soldier, oldEnemyHealth, oldSoldierHealth, currentAction, currentState)
    qValueOld = qTable[currentState - 1, currentAction - 1]
    nextState = getState(soldier)
    nextMax = np.max(qTable[nextState - 1])

    qValueNew = (1 - alpha) * qValueOld + alpha * (reward + gamma * nextMax)
    qTable[currentState - 1, currentAction - 1] = qValueNew


def pause():

    pause = True

    while pause:
        pygame.event.pump()
        font = pygame.font.SysFont('Papyrus', 24, True)
        font2 = pygame.font.SysFont('Calibri', 20, True)
        text = font.render('PAUSED', False, WHITE)
        textrect = text.get_rect()
        textrect.center = (SCREEN_WIDTH / 2), (40)
        screen.blit(text, textrect)

        text1 = font2.render("At health >= 75: %s" % qTable[3869], False, WHITE)
        textrect1 = text1.get_rect()
        textrect1.center = (SCREEN_WIDTH / 2), (500)
        screen.blit(text1, textrect1)

        text2 = font2.render("At health >= 35: %s" % qTable[3870], False, WHITE)
        textrect2 = text2.get_rect()
        textrect2.center = (SCREEN_WIDTH / 2), (520)
        screen.blit(text2, textrect2)

        text3 = font2.render("At health >= 0: %s" % qTable[3871], False, WHITE)
        textrect3 = text3.get_rect()
        textrect3.center = (SCREEN_WIDTH / 2), (540)
        screen.blit(text3, textrect3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
        pygame.display.flip()
        clock.tick(60)


def run():
    setup()
    start = time.time()
    done = False  # Loop until user clicks the close button
    turn = 2  # Used to check which teams turn it is
    roundNumber = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

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

                #  COMMENT THIS ELIF STATEMENT TO REMOVE AGGRESSIVE BEHAVIOR
                elif (len(red_soldier_list.sprites()) > 0):
                    random_red = random.randint(0, len(red_soldier_list.sprites()) - 1)
                    blue_soldier.offense(red_soldier_list.sprites()[random_red], blue_soldier_list)
                else:
                    blue_soldier.move()
        else:
            for red_soldier in red_soldier_list:
                train(red_soldier)

        if(not red_soldier_list or not blue_soldier_list):
            roundNumber += 1
            numSoldiers = 0
            totalHealth = 0
            end = time.time()
            timeTaken = end - start

            if(red_soldier_list):
                for red_soldier in red_soldier_list:
                    numSoldiers += 1
                    totalHealth += red_soldier.health

            if(not red_soldier_list):
                for blue_soldier in blue_soldier_list:
                    blue_soldier.kill()
            elif(not blue_soldier_list):
                for red_soldier in red_soldier_list:
                    red_soldier.kill()

            print("\nRound %d complete!" % roundNumber)
            print("%d red soldiers remaining with a total health of %d." % (numSoldiers, totalHealth))
            print("Total time taken to complete round: %f seconds\n" % timeTaken)
            print("At health >= 75:\n %s" % qTable[3869])
            print("At health >= 35:\n %s" % qTable[3870])
            print("At health >= 0:\n %s" % qTable[3871])

            setup()
            start = time.time()

        pygame.display.flip()
        clock.tick(60)
        turn += 1
