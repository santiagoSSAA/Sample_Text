#clase plataforma
import pygame
import Libreria.libreriaFrames as lf


# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

class Plataforma(pygame.sprite.Sprite):
    """ Plataforma sobre la que el usuario puede saltar """

    def __init__(self, imagen,pos,tipo):
        """ Constructor Plataforma.Asume su construccion cuando el usuario le haya pasado
            un array de 5 numeros, tal como se ha definido al principio de este codigo.. """
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.tipo = tipo

    def update(self):
        self.rect.x += self.velx