import pygame
from pygame.locals import *
import random

VELOCIDAD = 3
SUELO = 650

class Mama(pygame.sprite.Sprite):
    def __init__(self,listaSprites):
        pygame.sprite.Sprite.__init__(self)
        self.listaSprites = listaSprites
        self.accion = 0
        self.frame = 0
        self.image = self.listaSprites[self.accion][self.frame]
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        # tipo
        self.tipo = "mama"
        # direccion
        self.direccion = random.randrange(2)
        # temporizador de proyectil
        self.temporizadorProyectil = random.randrange(50,150)
        self.listaPlataformas = []
        """
        0 = derecha
        1 = izquierda
        """
        # numero de frames
        self.rect.x = 0
        self.rect.y = 0
        self.numeroFrames = 4
        # contador
        self.contadorAnimacion = 0

        """
        parado derecha = 0
        correr derecha = 1
        muerte derecha = 2

        parado izquierda = 3
        correr izquierda = 4
        muerte izquierda = 5

        """

    def update(self):

        # Desplazar izquierda/derecha
        self.movimiento()

        # Animar el sprite
        self.animarSprite()

        if self.temporizadorProyectil >= 0:
            self.temporizadorProyectil -= 1
        else:
            self.temporizadorProyectil = random.randrange(50,150)

    def movimiento(self):
        self.rect.x += self.velx
        self.rect.y += self.vely
        pass

    def animarSprite(self):
        self.image = self.listaSprites[self.accion][self.frame]
        if self.contadorAnimacion % 4 == 0:
            if self.frame < self.numeroFrames - 1:
                self.frame += 1
            else:
                self.frame = 0
            pass

    # Definir movimientos
    def izquierda(self):
        self.accion = 4
        self.velx = -VELOCIDAD
        pass

    def derecha(self):
        self.accion = 1
        self.velx = VELOCIDAD
        pass

    def idle(self):
        self.velx = 0
        self.vely = 0
        if self.accion <= 2:
            self.accion = 0
        else:
            self.accion = 3
        pass
# -------------------------------------------------------------------------------
class Pereza(pygame.sprite.Sprite):
    def __init__(self,listaSprites):
        pygame.sprite.Sprite.__init__(self)
        self.listaSprites = listaSprites
        self.frame = 0
        self.image = self.listaSprites[0][self.frame]
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        # tipo
        self.tipo = "pereza"
        # numero de frames
        self.rect.x = random.randrange(300,1200)
        self.rect.y = 560
        self.numeroFrames = 3
        # contador
        self.contadorAnimacion = 0
        # tiempo de vida
        self.vida = random.randrange(100,301)

    def update(self):
        # Define el movimiento
        self.movimiento()
        # Animar el sprite
        self.animarSprite()
        self.vida -=1
        pass

    def movimiento(self):
        self.rect.x += self.velx
        self.rect.y += self.vely
        pass

    def animarSprite(self):
        self.image = self.listaSprites[0][self.frame]
        if self.contadorAnimacion % 10 == 0:
            if self.frame < self.numeroFrames - 1:
                self.frame += 1
            else:
                self.frame = 0
            pass

    def idle(self):
        self.velx = 0
        self.vely = 0
# -------------------------------------------------------------------------------
VELOCIDADPROYECTIL = 11
class Chancla(pygame.sprite.Sprite):
    def __init__(self,listaSprites):
        pygame.sprite.Sprite.__init__(self)
        self.listaSprites = listaSprites
        self.frame = 0
        self.accion = 0
        self.image = self.listaSprites[self.accion][self.frame]
        # velocidades
        self.velx = 0
        self.vely = 0
        # coordenadas de inicio
        self.rect = self.image.get_rect()
        self.numeroFrames = 4
        # contador
        self.contadorAnimacion = 0
        # direccion
        self.direccion = 0

    def update(self):
        # Define el movimiento
        self.movimiento()
        # Animar el sprite
        self.animarSprite()

    def movimiento(self):
        self.rect.x += self.velx
        self.rect.y += self.vely
    
    def animarSprite(self):
        self.image = self.listaSprites[self.accion][self.frame]
        if self.contadorAnimacion % 4 == 0:
            if self.frame < self.numeroFrames - 1:
                self.frame += 1
            else:
                self.frame = 0
            pass
    
    # Definir movimientos
    def izquierda(self):
        self.accion = 1
        self.velx = -VELOCIDADPROYECTIL
        pass

    def derecha(self):
        self.accion = 0
        self.velx = VELOCIDADPROYECTIL
        pass
# -------------------------------------------------------------------------------