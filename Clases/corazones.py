import pygame
from pygame.locals import *

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

