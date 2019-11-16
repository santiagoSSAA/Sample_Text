#Mover el Fondo
#mover los objetos junto con el fondo
import pygame
import random
import ConfigParser
#music ogg douwnload


ANCHO = 640
ALTO = 576

VERDE=[0,255,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
ROJO=[255,0,0]
AZUL=[30,175,227]
ROSA= [255,0,255]
MORADO = [131,0,255]


def Recortar(imagen,fila,columna,RecoAncho,RecoAlto):
    info = imagen.get_rect()
    M=[]
    for f in range(fila):
        #print f
        ls=[]
        for c in range(columna):
            cuadro = imagen.subsurface(32*c,32*f,RecoAncho,RecoAlto)
            ls.append(cuadro)
        M.append(ls)
    return M

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        ''' Constructor / Atributos'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([60,60])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y =  0
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

class Bloque(pygame.sprite.Sprite):
    def __init__(self,pto):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([60,80])
        self.image.fill(ROSA)
        self.rect=self.image.get_rect()
        #Sonido para el bloque
        self.grito = pygame.mixer.Sound('grito.ogg')

        self.rect.x=pto[0]
        self.rect.y=pto[1]
        self.velx = 0

    def update(self):
        self.rect.x += self.velx



#------------------------------------------
#AQUI EMPIEZA LO WENO
if __name__ == '__main__':
    '''Programa principal'''
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])

    #Previa

    Fuente = pygame.font.Font(None,50)
    msj = 'pulsa espacio para Iniciar'
    msj1= 'pepo'
    musica = pygame.mixer.Sound('grito.ogg')
    musica.play()
    ty = ALTO
    reloj=pygame.time.Clock()
    fin = False
    seguir = False
    while (not fin) and (not seguir):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    seguir = True
        pantalla.fill(NEGRO)
        texto = Fuente.render(msj,True,VERDE)
        texto1 = Fuente.render(msj1,True,BLANCO)
        pantalla.blit(texto,[100,200])
        pantalla.blit(texto1,[100,300])
        pygame.display.flip()
        ty -= 5
        reloj.tick(40)
    #-----------------------------------------------
    #VARIABLES DEL JUEGO
    Fondo = pygame.image.load('hola.jpg')
    info = Fondo.get_rect()
    #print info
    Ancho_Fondo = info[2]

    jugadores = pygame.sprite.Group() #creo el grupo
    bloques = pygame.sprite.Group()


    fx = 0
    fy = -500
    fvelx = 0
    limAncho = ANCHO - 50
    limAncho_ = -1


    j = Jugador()#creo el objeto
    jugadores.add(j) #adiciono el objeto al grupo

    b = Bloque([900,200])
    bloques.add(b)



    fin = False
    reloj=pygame.time.Clock()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                fvelx = 0
        #LImites jugador y fondo
        if j.rect.right > limAncho:
            j.rect.right = limAncho
            j.velx = 0
            fvelx = -5


        elif j.rect.left < limAncho_:
            j.rect.left = limAncho_
            j. velx = 0
            fvelx = +5
        elif j.rect.y > (ALTO - j.rect.height):
            j.rect.y = ALTO - j.rect.height
            j.vely = 0
        elif j.rect.y < 0:
            j.rect.y = 0
            j.vely = 0
        #bloque tiene misma vel que el fondo
        for b in bloques:
            if fx > (ANCHO - Ancho_Fondo):
                b.velx = fvelx
            else:
                b.velx = 0

        jugadores.update()
        bloques.update()

        pantalla.blit(Fondo,[fx,fy])

        jugadores.draw(pantalla)
        bloques.draw(pantalla)

        pygame.display.flip()
        reloj.tick(60)
        if fx > (ANCHO - Ancho_Fondo):
            fx += fvelx
