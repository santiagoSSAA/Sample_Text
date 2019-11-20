import pygame
from pygame.locals import *

VELOCIDAD = 12

class Jugador(pygame.sprite.Sprite):
    def __init__(self,listaSprites):
        pygame.sprite.Sprite.__init__(self)
        # imagen
        self.listaSprites = listaSprites
        self.accion = 0
        self.frame = 0
        self.image = self.listaSprites[self.accion][self.frame]
        # velocidades
        self.velx = 0
        self.vely = 0
        # coordenadas de inicio
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.bottom = 600
        self.numeroFrames = 4
        # contador
        self.contadorAnimacion = 0
        # lista Objetos Obtenidos
        self.objetosObtenidos = []
        # puntos de vida
        self.vida = 3
        """
        parado derecha = 0
        correr derecha = 1
        muerte derecha = 2
        saltar derecha = 3

        parado izquierda = 4
        correr izquierda = 5
        saltar izquierda = 6
        muerte izquierda = 7

        """


    def update(self):
        
        # calcula la gravedad
        self.calcularGravedad(1.8)
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
        self.accion = 5
        self.velx = -VELOCIDAD
        pass

    def derecha(self):
        self.accion = 1
        self.velx = VELOCIDAD
        pass

    def idle(self):
        self.velx = 0
        self.vely = 0
        if self.accion <= 3:
            self.accion = 0
        else:
            self.accion = 4
        pass
    
    def salto(self):
        self.rect.y = self.rect.y - 1
        
        if self.accion <= 3:
            self.accion = 3
        elif self.accion > 3:
            self.accion = 6
        
        self.vely = -23

    def calcularGravedad(self,gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += gravedad
        pass