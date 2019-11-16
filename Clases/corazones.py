import pygame
from pygame.locals import *

class Corazon(pygame.sprite.Sprite):
    def __init__(self,listaSprites,identificador):
        pygame.sprite.Sprite.__init__(self)
        self.listaSprites = listaSprites
        self.image = self.listaSprites[0][self.estado]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 30
        self.identificador = identificador
        self.estado = 1
    
    def corazonActivo(self):
        self.estado = 0
    
    def corazonInactivo(self):
        self.estado = 1

