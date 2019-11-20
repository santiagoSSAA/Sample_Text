import pygame

class Nivel(object):
    """ Esta es una super clase generica usada para definir un nivel.
        Crea una clase hija especifica para cada nivel con una info especifica. """

    def __init__(self, protagonista):
        """ Constructor. Requerido para cuando las plataformas moviles colisionan con el protagonista. """
        self.listade_plataformas = pygame.sprite.Group()
        self.listade_enemigos = pygame.sprite.Group()
        self.protagonista = protagonista


        # Imagen de fondo
        self.imagende_fondo = None


    # Actualizamos todo en este nivel
    def update(self):
        """ Actualizamos todo en este nivel."""
        self.listade_plataformas.update()
        self.listade_enemigos.update()

    def draw(self, pantalla):
        """ Dibujamos todo en este nivel. """

        # Dibujamos todas las listas de sprites que tengamos
        self.listade_plataformas.draw(pantalla)
        self.listade_enemigos.draw(pantalla)

