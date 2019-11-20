import pygame
from pygame.locals import *
import random

class Objeto(pygame.sprite.Sprite):
    def __init__(self,image,identificador):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = random.randrange(150,1000)
        self.rect.y = random.randrange(450,550)
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

# -------------------------------------------------------------------------------
CANTIDADENEMIGOS = 5

class Generador(pygame.sprite.Sprite):
    def __init__(self,image,identificador,suelo):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = random.randrange(500,1000)
        self.rect.y = suelo - 50
        self.identificador = identificador
        self.cantidadEnemigos = CANTIDADENEMIGOS
        self.salirSpawn = False
        #esto es el temporizador del generador
        self.temp = random.randrange(100,150)
    
    def update(self):
        # define movimiento
        self.movimiento()
        if self.temp >= 0:
            self.temp -= 1
        else:
            self.temp = random.randrange(100,150)

    def movimiento(self):
        self.rect.x += self.velx
        self.rect.y += self.vely
# -------------------------------------------------------------------------------
class Corazon(pygame.sprite.Sprite):
    def __init__(self,listaSprites,identificador):
        pygame.sprite.Sprite.__init__(self)
        self.listaSprites = listaSprites
        self.image = self.listaSprites[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 30
        self.identificador = identificador
    
    def corazonActivo(self):
        self.image = self.listaSprites[0][0]
    
    def corazonInactivo(self):
        self.image = self.listaSprites[0][1]