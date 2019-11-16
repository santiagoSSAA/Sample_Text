import pygame
from pygame.locals import *
import random

VELOCIDAD = 0

class Objeto(pygame.sprite.Sprite):
    def __init__(self,image,identificador):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = random.randrange(30,1000)
        self.rect.y = random.randrange(350,550)
        self.identificador = identificador

    def update(self):
        # define movimiento
        self.movimiento()
        # posicionar los corazones
        if self.identificador == 5 or self.identificador == 6:
            self.rect.y = 30

    def movimiento(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

    def izquierda(self):
        self.velx = -VELOCIDAD

    def derecha(self):
        self.velx = VELOCIDAD

    def idle(self):
        self.velx = 0