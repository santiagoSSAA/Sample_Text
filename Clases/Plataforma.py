#clase plataforma
import pygame

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

class Plataforma(pygame.sprite.Sprite):
    """ Plataforma sobre la que el usuario puede saltar """

    def __init__(self, largo, alto ):
        """ Constructor Plataforma.Asume su construccion cuando el usuario le haya pasado
            un array de 5 numeros, tal como se ha definido al principio de este codigo.. """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([largo, alto])
        self.image.fill(VERDE)

        self.rect = self.image.get_rect()
