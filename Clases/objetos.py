import pygame
from pygame.locals import *
import random

class Objeto(pygame.sprite.Sprite):
    def __init__(self,image,identificador,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.identificador = identificador

    def update(self):
        self.rect.x += self.velx
        # posicionar los corazones
        if self.identificador == 5 or self.identificador == 6:
            self.rect.y = 30

    def movimiento(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

# -------------------------------------------------------------------------------
CANTIDADENEMIGOS = 5

class GeneradorPereza(pygame.sprite.Sprite):
    def __init__(self,image,identificador,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.identificador = identificador
        self.cantidadEnemigos = CANTIDADENEMIGOS
        self.salirSpawn = False
        #esto es el temporizador del generador
        self.temp = random.randrange(100,150)
    
    def update(self):
        self.rect.x += self.velx
        if self.temp >= 0:
            self.temp -= 1
        else:
            self.temp = random.randrange(100,150)
#----------------------------------------------------
class GeneradorMama(pygame.sprite.Sprite):
    def __init__(self,image,identificador,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.identificador = identificador
        self.cantidadEnemigos = CANTIDADENEMIGOS
        self.salirSpawn = False
        #esto es el temporizador del generador
        self.temp = random.randrange(100,150)
    
    def update(self):
        self.rect.x += self.velx
        if self.temp >= 0:
            self.temp -= 1
        else:
            self.temp = random.randrange(100,150)


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

# -------------------------------------------------------------------------------
class Cafe(pygame.sprite.Sprite):
    def __init__(self,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.tipo = "cafe"
        
    def update(self):
        # define movimiento
        self.movimiento()

    def movimiento(self):
        self.rect.x += self.velx
#-------------------------------------------------
#Son objetos que no interactuan en ningun sentido con el usuario, son 'adorno'
class Objetos_De_Fondo(pygame.sprite.Sprite):
    def __init__(self,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1] 
        self.velx = 0

    def update(self):
        self.rect.x += self.velx



#1: libro
#2: musica
#3 photoshop
#4: python
#5: puerta
#6: cosito insulto