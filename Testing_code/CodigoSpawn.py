import pygame
import math
import random


BLANCO =[255,255,255]
VERDE=[0,255,0]
ROJO=[255,0,0]
NEGRO=[0,0,0]
AZUL=[30,175,227]
ROSA= [255,0,255]
MORADO = [131,0,255]

ANCHO  = 800
ALTO = 600
CENTRO = (ANCHO//2,ALTO//2)


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        ''' Constructor / Atributos'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40,50])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = CENTRO[0]
        self.rect.y =  ALTO - self.rect.height
        self.velx = 0
        self.vely = 0
        self.vidas = 3

    def pos(self):
        ''' retorna posocion del jugador '''
        p = [self.rect.x,self.rect.y]
        return p

    def update(self): #Actualiza el estado de la clase/objeto

        self.rect.x += self.velx
        self.rect.y += self.vely

class Rival(pygame.sprite.Sprite):
    def __init__(self):
        ''' Constructor '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40,50])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.velx = 5
        self.disparar = False
        self.temp = random.randrange(150)

    def pos(self):
        ''' retorna posocion del rival '''
        p = [self.rect.x,self.rect.y]
        return p

    def update(self):
        ''' Actializar objeto '''
        self.rect.x += self.velx
        if self.rect.x > (ANCHO - self.rect.width):
            self.velx = -5
        if self.rect.x < 0:
            self.velx = 5
        self.temp -= 1

class Proyectil(pygame.sprite.Sprite):
    def __init__(self,pos,cl = ROJO):
        ''' Constructor '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,15])
        self.image.fill(cl)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = -7
    def update(self):
        ''' Actualizar objeto '''
        self.rect.y += self.vely

if __name__ == '__main__':

    pygame.init()
    pantalla=pygame.display.set_mode([ANCHO,ALTO])

    #Inicializar grupos
    fuente = pygame.font.Font(None,32)
    jugadores = pygame.sprite.Group() #creo el grupo
    rivales = pygame.sprite.Group()
    proyectil = pygame.sprite.Group()
    balas_r = pygame.sprite.Group()


    #inicializar jugador
    j = Jugador()#creo el objeto
    jugadores.add(j) #adiciono el objeto al grupo
    vidas = j.vidas
    #inicializar Ribvales
    n = 10
    for i in range(n): # crea n rivales
        r = Rival()
        r.rect.x = random.randrange(ANCHO - r.rect.width)
        r.rect.y = random.randrange(ALTO - 180)
        rivales.add(r)

    fin_juego = False

    reloj = pygame.time.Clock()

    pygame.display.flip()
    fin=False

    #CICLO PRINCIPAL
    while (not fin) and (not fin_juego) :
        #GESTION DE EVENTOS
        for event in pygame.event.get():
        # Identifica todos los eventos de la maquina
            if event.type==pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                #Gestion de Teclas
                #objeto se mueve al pulsar
                if event.key == pygame.K_DOWN:
                    j.velx = 0
                    j.vely = 5
                if event.key == pygame.K_UP:
                    j.velx = 0
                    j.vely = -5
                if event.key == pygame.K_LEFT:
                    j.vely = 0
                    j.velx = -5
                if event.key == pygame.K_RIGHT:
                    j.vely = 0
                    j.velx = 5
                if event.key == pygame.K_SPACE:
                    j.vely = 0
                    j.velx = 0

            if event.type == pygame.KEYUP:
                #objeto se mueve al liberar
                j.velx = 0
                j.vely = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                #Gestion del raton
                print j.pos()
                #inicializar proyectil
                b = Proyectil(j.pos())
                proyectil.add(b)


        #GESTION DE CONTROL
        #Control limites del jugador
        if j.rect.x > (ANCHO - j.rect.width):
            j.rect.x = ANCHO - j.rect.width
            j.velx = 0
        elif j.rect.x < 0:
            j.rect.x = 0
            j. velx = 0
        elif j.rect.y > (ALTO - j.rect.height):
            j.rect.y = ALTO - j.rect.height
            j.vely = 0
        elif j.rect.y < 0:
            j.rect.y = 0
            j.vely = 0

        #Gestion de colision de balas
        for b in proyectil:
            #colision con rivales
            ls = pygame.sprite.spritecollide(b,rivales,True)
            #si es falso, el proyectil solo pasa encima del rival, sin eliminarlo
            for e in ls:
                proyectil.remove(b)

            #control de limites
            if b.rect.y < -10:
                proyectil.remove(b)
        #Gesion de Rivales
        for r in rivales:
            if r.temp == 0:
                r.disparar = True
            if r.disparar:
                b = Proyectil(r.pos(),VERDE)
                b.vely = 7 #la bala va hacia abajo
                balas_r.add(b)
                r.disparar = False
                r.temp = random.randrange(100)

        for b in balas_r:
            ls = pygame.sprite.spritecollide(b,jugadores,True)
            for b in ls:
                balas_r.remove(b)
                vidas -= 1
                j = Jugador()
                j.vidas = vidas
                jugadores.add(j)

            if b.rect.y > ALTO + 20:
                balas_r.remove(b)

        # Las vidas del jugador se acaban...
        if vidas <= 0 :
            fin_juego = True

        #GESTION PANTALLA
        #Actualizar objetos

        jugadores.update()
        rivales.update()
        proyectil.update()
        balas_r.update()

        texto = 'vidas:'+ str(j.vidas)
        info = fuente.render(texto,True,BLANCO)

        #Desplegar graficos
        pantalla.fill(NEGRO)
        pantalla.blit(info,[50,10])
        jugadores.draw(pantalla)
        rivales.draw(pantalla)
        proyectil.draw(pantalla)
        balas_r.draw(pantalla)


        pygame.display.flip()
        reloj.tick(10)

    #Fuera del ciclo
    fuente = pygame.font.Font(None,38)
    texto = 'FIN DEL JUEGO'
    info = fuente.render(texto,True,BLANCO)
    pantalla.fill(NEGRO)
    pantalla.blit(info,[300,300])
    pygame.display.flip()

    while not fin:
        #GESTION DE EVENTOS
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                fin=True
