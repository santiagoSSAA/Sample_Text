import pygame
from pygame.locals import *
import Clases.Plataforma as p

#----------------------
ANCHO= 1280
ALTO= 720
SUELO = 660

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
        self.rect.x = 25
        self.rect.y = 600
        self.numeroFrames = 4
        # contador
        self.contadorAnimacion = 0
        # lista Objetos Obtenidos
        self.objetosObtenidos = []
        # puntos de vida
        self.vida = 3
        #esto nos sirve para implementar los demas niveles
        self.nivel = None
        
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
        self.calcularGravedad()

        self.rect.x += self.velx
        
        # Comprobamos si hemos chocado contra algo
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        for bloque in lista_impactos_bloques:
            # Si nos estamos desplazando hacia la derecha, hacemos que nuestro lado derecho sea el lado izquierdo del objeto que hemos tocado-
            if self.velx > 0:
                self.rect.right = bloque.rect.left
            elif self.velx < 0:
                # En caso contrario, si nos desplazamos hacia la izquierda, hacemos lo opuesto.
                self.rect.left = bloque.rect.right

        # Desplazar arriba/abajo
        self.rect.y += self.vely

        # Comprobamos si hemos chocado contra algo
        lista_impactos_bloques = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        for bloque in lista_impactos_bloques:

            # Restablecemos nuestra posicion basandonos en la parte superior/inferior del objeto.
            if self.vely > 0:
                self.rect.bottom = bloque.rect.top
            elif self.vely < 0:
                self.rect.top = bloque.rect.bottom

            # Detenemos nuestro movimiento vertical
            self.vely = 0

        for bloque in lista_impactos_bloques:
                if ((self.rect.right-50)  < bloque.rect.left) or (self.rect.left > (bloque.rect.right- 20)):
                    # TODO: aqui es para que el jugador al salir de la plataforma, vaya cayendo, pero como tengo un lapso y no
                    # se como hacer que caiga, pongo su posicion en y en el SUELO :v 
                    self.rect.y = SUELO


        # TODO: falta corregir el hecho de que si salta desde una plataforma y su cabeza choca con otra, cuando toque la plataforma vuelva a su posicion original


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
        self.velx = -10
        pass

    def derecha(self):
        self.accion = 1
        self.velx = 10
        pass

    def stop(self):
        """ Es llamado cuando el usuario abandona el teclado """

    def idle(self):
        self.velx = 0
        self.vely = 0
        if self.accion <= 3:
            self.accion = 0
        else:
            self.accion = 4
        pass
    
    def salto(self):
        '''Llamado cuando el usuario pulsa el boton de 'saltar'. '''
        self.rect.y = self.rect.y - 1
        
        if self.accion <= 3:
            self.accion = 3
        elif self.accion > 3:
            self.accion = 6
        
        self.vely = -23

    def salto_plataforma(self):
        """ Llamado cuando el usuario pulsa el boton de 'saltar'. """

        # Descendemos un poco y observamos si hay una plataforma debajo nuestro.
        # Descendemos 2 pixiels (con una plataforma que esta  descendiendo, no funciona bien
    # si solo descendemos uno).
        self.rect.y += 2
        lista_impactos_plataforma = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        self.rect.y -= 2

        # Si esta listo para saltar, aumentamos nuestra velocidad hacia arriba
        if len(lista_impactos_plataforma) > 0 or self.rect.bottom >= SUELO:
            self.salto()
        


    def calcularGravedad(self):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += 1.55
        pass

        '''
        #Observamos si nos encontramos sobre el suelo.
        if self.rect.y >= SUELO - self.rect.height and self.vely >= 0:
            self.vely = 0
            self.rect.y = SUELO - self.rect.height
        '''