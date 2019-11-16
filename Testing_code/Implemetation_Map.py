#Mapa unido a una animacion
import pygame
import random
import ConfigParser

ANCHO = 640
ALTO = 576
VERDE=[0,255,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
ROJO=[255,0,0]

def Recortar(pantalla,imagen, numeroColumnas, numeroFilas):
    # Aqui se almacenaran todos los sprites recortados de la imagen
    listaSprites = []

    # Aqui se calcula el tamano individual de cada frame
    anchoSprite = imagen.get_rect()[2] // numeroColumnas
    altoSprite = imagen.get_rect()[3] // numeroFilas

    # Aqui se recorta cada sprite de la imagen
    for alto in range(numeroFilas):
        linea = []
        for ancho in range(numeroColumnas):
            rect = (ancho*anchoSprite,alto*altoSprite,anchoSprite,altoSprite)
            sprite = imagen.subsurface(rect)
            linea.append(sprite)
        listaSprites.append(linea)

    """
    # Imprimir el array
    for alto in range(numeroFilas):
        for ancho in range(numeroColumnas):
            pantalla.blit(listaSprites[alto][ancho],[ancho*anchoSprite,alto*altoSprite])
    """

    return listaSprites

class Jugador(pygame.sprite.Sprite):
    def __init__(self,m):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.direccion=0
        self.con=0
        self.image=self.m[self.direccion][self.con]
        #self.image=self.m[self.con][self.direccion]
        self.rect=self.image.get_rect()
        self.velx=0
        self.vely=0

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely
        self.image=self.m[self.direccion][self.con]
        #self.image=self.m[self.con][self.direccion]
        if self.con < 2:
            self.con +=1
        else:
            self.con = 0

class Bloque(pygame.sprite.Sprite):
    def __init__(self,archivo,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=archivo
        self.rect=self.image.get_rect() #devuelve ancho, alto, x, y
        self.rect.x = pos[0]
        self.rect.y = pos[1]



#------------------------------------------
#AQUI EMPIEZA LO WENO
if __name__ == '__main__':
    '''Programa principal'''
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    Fondo = pygame.image.load('Mapa1.png')

    #importo el mapa
    mapa = ConfigParser.ConfigParser()
    mapa.read('mapa.map')

    archivo = mapa.get('info','img') #img: terrenogen.png (1024x384)
    imagen_sprites = pygame.image.load(archivo)
    imagenGato = pygame.image.load('animals.png') #sprite del gato

    jugadores=pygame.sprite.Group()
    archivo = mapa.get('info','img') #img: terrenogen.png (1024x384)
    bloques=pygame.sprite.Group()

    mp = mapa.get('info', 'mapa')# aqui guardo el mapa en la variable mp
    mp = mp.split('\n')
    fila = mp[1] #me paro en la fila 1 del mapa
    objeto = fila[3]
    print objeto
    #objeto: es numeral (#)

    fl = int(mapa.get(objeto, 'fil'))
    cl = int(mapa.get(objeto, 'col'))


    #fondo de pantalla

    gato = Recortar(pantalla,imagenGato,12,8) #recorta imagenes del animals.png
    j=Jugador(gato)
    jugadores.add(j)

    muro = Recortar(pantalla,imagen_sprites,32,12) #recorta imagenes de terrenogen.png
    pantalla.blit(muro[0][0], [200,200] )

#FUNCION QUE PONE LOS SPRITES DEL MAPA EN PANTALLA
    conteoy = 0 #Conteo pixeles y
    for cada_fila in mp:
        conteox = 0 #conteo pixeles x
        for cada_elemento in cada_fila:
            #aqui, pone los sprites
            tipo = mapa.get(cada_elemento,'tipo')
            if  tipo == 'vacio':
                pass
            elif tipo == 'muro':
                b = Bloque(muro[6][18],[conteox,conteoy])
                bloques.add(b)
            elif tipo == 'agua':
                b = Bloque(muro[3][13],[conteox,conteoy])
                bloques.add(b)

            conteox += 32
        conteoy += 32
#----------------------------

    fin = False
    reloj=pygame.time.Clock()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    j.direccion=2
                    j.velx=10
                    j.vely=0
                if event.key == pygame.K_LEFT:
                    j.direccion=1
                    j.velx=-10
                    j.vely=0
                if event.key == pygame.K_UP:
                    j.direccion=3
                    j.velx=0
                    j.vely=-10
                if event.key == pygame.K_DOWN:
                    j.direccion=0
                    j.velx=0
                    j.vely=10
            if event.type == pygame.KEYUP:
                j.velx=0
                j.vely=0

        #colision
        ls_col=pygame.sprite.spritecollide(j,bloques,False)
        for b in ls_col:
            if j.velx>0:
                if j.rect.right > b.rect.left:
                    j.rect.right = b.rect.left
                    j.velx=0

            if j.velx<0:
                if j.rect.left < b.rect.right:
                    j.rect.left = b.rect.right
                    j.velx=0

            if j.vely>0:
                if j.rect.bottom > b.rect.top:
                    j.rect.bottom = b.rect.top
                    j.vely=0

            if j.vely<0:
                if j.rect.top < b.rect.bottom:
                    j.rect.top = b.rect.bottom
                    j.vely=0

        jugadores.update()
        bloques.update()
        pantalla.blit(Fondo,[0,0])
        jugadores.draw(pantalla)
        bloques.draw(pantalla)
        pygame.display.flip()
        reloj.tick(10)
