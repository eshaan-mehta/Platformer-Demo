import pygame

from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 1080, 720
CLOCK = pygame.time.Clock()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Allo")