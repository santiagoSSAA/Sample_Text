import pygame
from pygame.locals import *

class Imagen(pygame.sprite.Sprite):
    def __init__(self,imagen,identificador):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.velx = 0
        self.rect.x = 0
        self.identificador = identificador

    def update(self):        
        self.movimiento()

    def movimiento(self):
        self.rect.x += self.velx

    # Definir movimientos
    def izquierda(self):
        self.velx = -10
        pass

    def derecha(self):
        self.velx = 10
        pass

    def idle(self):
        self.velx = 0