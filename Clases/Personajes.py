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
        #para implementar los niveles
        self.Nivel = None
        self.lista_plataformas = []

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
        # variables para controlar los efectos
        self.tiempoStun = 0
        self.tiempoSlow = 0
        self.tiempoSpeed = 0

    def update(self):
        # calcula la gravedad
        self.calcularGravedad(1.8)
        # Define el movimiento
        self.movimiento()
        # Animar el sprite
        self.animarSprite()
        
        # activar/desactivar stun
        if self.tiempoStun > 0:
            self.stun()
        else:
            self.tiempoStun = 0
        # activar/desactivar slow
        if self.tiempoSlow > 0:
            self.slow()
        else:
            self.tiempoSlow = 0
        # activar/desactivar speed
        if self.tiempoSpeed > 0:
            self.speed()
        else:
            self.tiempoSpeed = 0
            


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

        if self.tiempoSlow > 0:
            self.velx = self.velx //3
        elif self.tiempoSpeed > 0:
            self.velx = self.velx*2
        elif self.tiempoStun > 0:
            self.velx = 0

        pass

    def derecha(self):
        self.accion = 1
        self.velx = VELOCIDAD

        if self.tiempoSlow > 0:
            self.velx = self.velx //3
        elif self.tiempoSpeed > 0:
            self.velx = self.velx*2
        elif self.tiempoStun > 0:
            self.velx = 0

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
        self.vely = -(VELOCIDAD*2)
        
        if self.accion <= 3:
            self.accion = 3
        elif self.accion > 3:
            self.accion = 6

        if self.tiempoSlow > 0:
            self.vely = self.vely //2
        elif self.tiempoStun > 0:
            self.vely = 0
        elif self.tiempoSpeed > 0:
            self.vely = self.vely *2

    def stun(self):
        """self.velx = 0
        self.vely = 0"""
        pass

    def slow(self):
        """self.velx = self.velx //3
        if self.vely != 0:
            self.vely = self.vely //3"""
        pass

    def speed(self):
        """self.velx = self.velx*2
        if self.vely != 0:
            self.vely = self.vely *2"""
        pass

    def calcularGravedad(self,gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += gravedad
        pass