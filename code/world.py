import sys
import os
import pygame
from gboid import Gboid
from planet import Planet
import random
import math
# import agent

pygame.init()

WIDTH = 1200
HEIGHT = 800
FR = 4

DISP = pygame.display.set_mode((WIDTH, HEIGHT)) # each grid box is 200x200px
pygame.display.set_caption('Gravity Boids')

run = True

boids = []
planets = []
num_boids = 150
num_planets = 30

for i in range(num_boids):
    boids.append(Gboid(WIDTH, HEIGHT, FR))

for i in range(num_planets):
    planets.append(Planet(20, int(random.uniform(0, WIDTH)), int(random.uniform(0, HEIGHT))))


print('\n\n\n')

def draw_boids(boids):
    for i in boids:
        # print(i.px)
        pygame.draw.line(DISP, (70,70,70), (i.px, i.py), (i.px+i.vx*.5,i.py+i.vy*.5), 7)

def draw_planets(planets):
    for i in planets:
        pygame.draw.circle(DISP, (0, 0, 10), (i.px, i.py), i.mass*1)

def evolve_boids(boids):
    for i in range(len(boids)):
        boids[i].evolve(boids, planets)
    
    return boids


while run: # Main world loop
    # pygame.time.delay(10)
    DISP.fill((200, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    boids = evolve_boids(boids) # TODO: Make this proper and efficient
    draw_boids(boids)
    draw_planets(planets)


    pygame.display.update()

pygame.quit()
sys.exit()


def draw_boids(boids):
    for i in boids:
        pygame.draw.rectangle(DISP, (70,70,70), (i.px), (i.py), (i.px+i.vx*4, i.py.i.vy*4))
        i.evolve()