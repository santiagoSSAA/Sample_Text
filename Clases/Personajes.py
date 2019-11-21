import pygame
from pygame.locals import *

VELOCIDAD = 12
SUELO = 650

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

        # Desplazar izquierda/derecha
        self.rect.x += self.velx
        
        # Colisiones jugador con plataformas
        ColisionesPlataformas = pygame.sprite.spritecollide(self, self.lista_plataformas, False)
        for cada_plataforma in ColisionesPlataformas:
            # Si nos estamos desplazando hacia la derecha, hacemos que nuestro lado derecho sea el lado izquierdo del objeto que hemos tocado-
            if self.velx > 0:
                self.rect.right = cada_plataforma.rect.left
            elif self.velx < 0:
                # En caso contrario, si nos desplazamos hacia la izquierda, hacemos lo opuesto.
                self.rect.left = cada_plataforma.rect.right

        # Desplazar arriba/abajo
        self.rect.y += self.vely

        # Comprobamos si hemos chocado contra algo
        ColisionesPlataformas = pygame.sprite.spritecollide(self, self.lista_plataformas, False)
        for cada_plataforma in ColisionesPlataformas:
            # Restablecemos nuestra posicion basandonos en la parte superior/inferior del objeto.
            if self.vely > 0:
                self.rect.bottom = cada_plataforma.rect.top
            elif self.vely < 0:
                self.rect.top = cada_plataforma.rect.bottom

            # Detenemos nuestro movimiento vertical
            self.vely = 0

        ColisionesPlataformas = pygame.sprite.spritecollide(self, self.lista_plataformas, False)
        for cada_plataforma in ColisionesPlataformas:
                if ((self.rect.right-50)  < cada_plataforma.rect.left) or (self.rect.left > (cada_plataforma.rect.right- 20)):
                    self.calcularGravedad(1.8)
        # Animar el sprite
        self.animarSprite()
        
        # activar/desactivar stun
        if self.tiempoStun <= 0:
            self.tiempoStun = 0

        # activar/desactivar slow
        if self.tiempoSlow <= 0:
            self.tiempoSlow = 0
        # activar/desactivar speed
        if self.tiempoSpeed <= 0:
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

    def salto_en_plataforma(self):
        """ Llamado cuando el usuario pulsa el boton de 'saltar'. """

        # Descendemos un poco y observamos si hay una plataforma debajo nuestro.
        # Descendemos 2 pixiels 
        self.rect.y += 2
        ColisionesPlataformas = pygame.sprite.spritecollide(self, self.lista_plataformas, False)
        self.rect.y -= 2


        # Si esta listo para saltar, aumentamos nuestra velocidad hacia arriba
        if len(ColisionesPlataformas) > 0 or self.rect.bottom >= SUELO:
            self.salto()

    def calcularGravedad(self,gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += gravedad
        pass