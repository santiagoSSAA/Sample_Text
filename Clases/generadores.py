import pygame
from pygame.locals import *
import random

VELOCIDAD = 1
CANTIDADENEMIGOS = 5

class Generador(pygame.sprite.Sprite):
    def __init__(self,image,identificador,suelo):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = random.randrange(200,1000)
        self.rect.y = suelo
        self.identificador = identificador
        self.cantidadEnemigos = CANTIDADENEMIGOS
    
    def update(self):
        # define movimiento
        self.movimiento()

    def movimiento(self):
        self.rect.x += self.velx
        self.rect.y += self.vely
    
    def izquierda(self):
        self.velx = -VELOCIDAD

    def derecha(self):
        self.velx = VELOCIDAD

    def idle(self):
        self.velx = 0