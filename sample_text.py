#ODIO WINDOWS XD 2.0
import pygame
from pygame.locals import *
# -------------------------------------------------------------------------------
import Libreria.libreriaFrames as lf
# -------------------------------------------------------------------------------
import Clases.Personajes as pp
import Clases.enemigos as e
import Clases.objetos as o
import Clases.background as b
import Clases.Nivel as n
#---------------------------
import Clases.Plataforma as pl
import random
# -------------------------------------------------------------------------------
ANCHO = 1280
ALTO = 720
SUELO = 660
LIMITE = ANCHO - 130
LIMITEINFERIOR = ANCHO-LIMITE
FPS = 35
NUMEROVIDAS = 5
# Colores (van implementando la splataformas, despues pueden ser eliminados)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
#---------------------------------------------------
#NOTA: coloco estas clases aqui porque no he podido importarlas Y que funcione el programa
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


# Creamos las plataformas para el nivel
class Nivel_01(Nivel):
    """ Definicion para el nivel 1. """

    def __init__(self, protagonista):
        """ Creamos el nivel 1. """

        # llamamos al constructor padre
        Nivel.__init__(self, protagonista)

        # Array con la informacion sobre el largo, alto, x, e y
        nivel = [ [210, 20, 500, 500],
                  [210, 20, 200, 400],
                  [210, 20, 600, 300],
                  ]

        # Iteramos sobre el array anterior y anadimos plataformas
        for plataforma in nivel:
            bloque = pl.Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.protagonista = self.protagonista
            self.listade_plataformas.add(bloque)


# -------------------------------------------------------------------------------
def main():
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    pygame.display.set_caption("Nivel 1 :v")
    reloj = pygame.time.Clock()
    temporizador = 300
    rapidez = FPS
    # Texto de vidas
    fuente = pygame.font.Font(None,24)
    info = fuente.render("VIDAS",True,[0,0,0])
    contadorTiempo = 1
    # Grupos de sprites
    modificadores = pygame.sprite.Group()
    generadores = pygame.sprite.Group()
    proyectiles = pygame.sprite.Group()
    corazones = pygame.sprite.Group()
    jugadores = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    objetos = pygame.sprite.Group()
    fondos = pygame.sprite.Group()
    plataformas = pygame.sprite.Group()

    # variables ventanas
    finDeJuego = False

    # Cargar imagenes
    spriteSantiago = pygame.image.load("Sprites/Sprite_Sheet_Santiago.png")
    spriteMama = pygame.image.load("Sprites/Sprite_Sheet_mama.png")
    spriteObjetos = pygame.image.load("Sprites/Sprite_Sheet_Objetos.png")
    spriteBackground = pygame.image.load("Sprites/background.gif")
    spritePereza= pygame.image.load("Sprites/Sprite_Sheet_Pereza.png")
    spriteChancla = pygame.image.load("Sprites/Sprite_Sheet_Chancla.png")

    # lista de sprites
    listaSpritesSantiago = lf.recortarSprite(pantalla,spriteSantiago,4,8)
    listaSpritesObjeto = lf.recortarSprite(pantalla,spriteObjetos,3,4)
    listaSpritesMama = lf.recortarSprite(pantalla,spriteMama,4,6)
    listaSpritesPereza = lf.recortarSprite(pantalla,spritePereza,3,1)
    listaSpritesChancla = lf.recortarSprite(pantalla,spriteChancla,4,2)
    # Sprites y clase Santiago
    jugador = pp.Jugador(listaSpritesSantiago)
    jugador.vida = NUMEROVIDAS
    jugadores.add(jugador)

    # Creamos todos los niveles
    listade_niveles = []
    listade_niveles.append(Nivel_01(jugador))

    # Establecemos el nivel actual
    nivel_actual_no = 0
    nivel_actual = listade_niveles[nivel_actual_no]
    #Le asignamos al jugador el nivel
    jugador.nivel = nivel_actual


    # Sprites y clase objeto
    # Sprites y clase Objetos
    for i in range(1,5):
        objeto = None
        if i  == 1:
            objeto = o.Objeto(listaSpritesObjeto[0][2],i)
        else:
            objeto = o.Objeto(listaSpritesObjeto[2][i-2],i)
        objetos.add(objeto)
    
    # Sprites y clase Corazones
    numero_Corazones = jugador.vida
    for i in range(1,numero_Corazones+1):
        c = o.Corazon(listaSpritesObjeto,i)
        corazones.add(c)
        if numero_Corazones <= 5:
            c.rect.x = 10 + (35*i)
        else:
            if i <= 5:
                c.rect.x = 10 + (35*i)
            else:
                if i%5 != 0:
                    c.rect.x = 10 + (35*(i%5))
                    c.rect.y = c.rect.y + (35*(i//5))
                else:
                    c.rect.x = 10 + (35*(5))
                    c.rect.y = c.rect.y + (35*(i//5))


    # crea puertas (generadores de enemigos)
    numero_Puertas = random.randrange(2,5)
    for i in range(numero_Puertas):
        puerta = o.Generador(listaSpritesObjeto[3][2],5,SUELO)
        generadores.add(puerta)
    


    # Sprites y clase imagen
    background = b.Imagen(spriteBackground,1)
    fondos.add(background)

    # ----------------------------------------------------------------------------------------------------
    while True and (not finDeJuego):
        # Logica del tiempo
        if contadorTiempo < rapidez:
            contadorTiempo +=1
        else:
            temporizador -= 1

            # reducir los tiempos del efecto del jugador
            if jugador.tiempoSlow > 0:
                jugador.tiempoSlow -=1
            elif jugador.tiempoStun > 0:
                jugador.tiempoStun -= 1
            elif jugador.tiempoSpeed > 0:
                jugador.tiempoSpeed -= 1

            contadorTiempo = 1

        # Logica del temporizador
        if temporizador < 90:
            rapidez = FPS // 3
        
        if temporizador <= 0:
            finDeJuego = True

        # Crea el temporizador
        fuenteTemporizador = pygame.font.Font(None,36)
        tempoInfo = fuenteTemporizador.render(("Tiempo: "+ str(temporizador)),True,[0,0,0])

        # Analizar vidas restantes
        if jugador.vida < 1:
            finDeJuego = True

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Manejo de las teclas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    jugador.derecha()
                if event.key == pygame.K_LEFT:
                    jugador.izquierda()
                if event.key == pygame.K_UP:
                    if jugador.rect.bottom > SUELO or jugador.salto_plataforma():
                        print(jugador.rect.bottom)
                        jugador.salto()
                    
            
            # Detener el personaje en caso de no oprimir nada
            if event.type == pygame.KEYUP:
                if event.key != pygame.K_UP:
                    jugador.idle()
                    background.idle()
            
        # ----------------------------------------------------------------------------------------------------
        # Control
        for j in jugadores:
            # Reconocer que hay un suelo
            if j.rect.bottom > SUELO:
                j.rect.bottom = SUELO
                j.vely = 0
                # Definir posicion de idle o run al caer al suelo
                if j.velx > 0:
                    j.accion = 1
                elif j.velx <0:
                    j.accion = 5
                else:
                    if j.accion < 3:
                        j.accion = 0
                    else:
                        j.accion = 4
            
            # Reconocer extremo a partir del cual se mueve el mapa
            if j.rect.right > LIMITE and background.rect.right > ANCHO and j.accion in [1,3]:
                j.rect.right = LIMITE
                background.izquierda(j.velx)
            elif background.rect.left < 0 and j.rect.right < LIMITEINFERIOR and j.accion in [5,6]:
                j.rect.right = LIMITEINFERIOR
                background.derecha(-j.velx)
            elif j.rect.left < 0:
                j.rect.left = 0
            elif j.rect.right > background.rect.right:
                j.rect.right = background.rect.right
            else:
                background.idle()
            # Aumentar el contador de animacion del jugador
            if j.contadorAnimacion < FPS:
                j.contadorAnimacion += 1
            else:
                j.contadorAnimacion = 1

        for ene in enemigos:
            
            # Acciones para la mama
            if ene.tipo == "mama":
                ene.idle()
                # Eleccion direccion movimiento mama
                if ene.direccion == 0:
                    ene.derecha()
                elif ene.direccion == 1:
                    ene.izquierda()
                
                # Disparo de proyectiles
                if ene.temporizadorProyectil == 0 and len(proyectiles) < 6:
                    chancla = e.Chancla(listaSpritesChancla)
                    
                    if ene.direccion == 0:
                        chancla.direccion =0
                        chancla.derecha()
                    elif ene.direccion == 1:
                        chancla.direccion = 1
                        chancla.izquierda()
                    
                    proyectiles.add(chancla)
                    chancla.rect.x = ene.rect.x
                    chancla.rect.y = ene.rect.y
                        
                # Movimiento mama (definir los limites de movimiento en la mama)
                if ene.rect.right >= background.rect.right:
                    ene.direccion = 1
                elif ene.rect.left <= 180:
                    ene.direccion = 0
                
                # Calculo de velocidades mama-entorno
                if background.velx != 0:
                    ene.velx += background.velx
                
                # Aumentar el contador de animacion del enemigo
                if ene.contadorAnimacion < FPS:
                    ene.contadorAnimacion += 1
                else:
                    ene.contadorAnimacion = 1
                pass
            elif ene.tipo == "pereza":
                # Aumentar el contador de animacion del enemigo
                if ene.contadorAnimacion < FPS:
                    ene.contadorAnimacion += 1
                else:
                    ene.contadorAnimacion = 1
                pass

                # Calculo de velocidades pereza-entorno
                ene.velx = background.velx

            # Acciones para pereza
            if ene.tipo == "pereza":
                if ene.vida == 0:
                    enemigos.remove(ene)

        for ob in objetos:
            # Sincronizar el movimiento de los objetos con el del fondo
            if ob.rect.y != 30:
                ob.velx = background.velx
            else:
                ob.velx = 0

        for g in generadores:
            if len(enemigos) < (0*len(generadores)):
                if g.temp == 0:
                    g.salirSpawn = True
                if g.salirSpawn:
                    selectorEnemigo = random.randrange(1,3)
                    if selectorEnemigo == 1:
                        enemigo = e.Mama(listaSpritesMama)
                        enemigo.rect.x = g.rect.x               
                        enemigo.rect.bottom =g.rect.bottom
                    elif selectorEnemigo == 2:
                        enemigo = e.Pereza(listaSpritesPereza)
                        enemigo.rect.x = g.rect.x + random.randrange(-50,51)
                        enemigo.rect.bottom = g.rect.bottom + 65
                    enemigos.add(enemigo)
                    g.salirSpawn = False
            
            # Sincronizar el movimiento de los generadores con el del entorno
            g.velx = background.velx
        
        for c in corazones:
            # Desaparicion de vidas
            if jugador.vida < NUMEROVIDAS:
                if c.identificador == jugador.vida+1:
                    c.corazonInactivo()
        
        # Sincronizar la velocidad del proyectil con la del background
        for pro in proyectiles:
            if pro.direccion ==  0:
                pro.derecha()
            elif pro.direccion == 1:
                pro.izquierda()
            
            if pro.rect.x < 0 or pro.rect.x > ANCHO:
                proyectiles.remove(pro)
            
            if background.velx != 0:
                pro.velx += background.velx

        # ----------------------------------------------------------------------------------------------------
        # Colisiones con objetos
        ColisionesObjetos = pygame.sprite.spritecollide(jugador, objetos, False)
        if len(ColisionesObjetos) > 0:
            ColisionesObjetos[0].rect.x = 300 + (50*(ColisionesObjetos[0].identificador))
            ColisionesObjetos[0].rect.y = 30
            jugador.objetosObtenidos.append(ColisionesObjetos[0].identificador)

        # Colisiones jugador a Enemigos
        ColisionesEnemigos = pygame.sprite.spritecollide(jugador, enemigos, False)
        for i in ColisionesEnemigos:
            if i.tipo != "pereza" and abs(jugador.rect.bottom - i.rect.top) <= 7 and jugador.vely > 0 :
                enemigos.remove(i)
      
        # Colisiones Enemigo contra jugadores
        for ene in enemigos:
            rangoChoque = 50
            ColisionJugadorEnemigo = pygame.sprite.spritecollide(ene, jugadores, False)
            for i in ColisionJugadorEnemigo:
                if ene.tipo == "mama" and i.rect.y == ene.rect.y and abs(i.rect.x - ene.rect.x) <= rangoChoque:
                    vidas = jugador.vida
                    jugadores.remove(i)
                    vidas -= 1
                    jugador = pp.Jugador(listaSpritesSantiago)
                    jugador.vida = vidas
                    jugadores.add(jugador)

                elif ene.tipo == "pereza":
                    if jugador.tiempoSlow == 0:
                        jugador.tiempoSlow = 5

                # actualizar el movimiento del jugador con el efecto incluido
                if jugador.accion == 0:
                    jugador.idle()
                elif jugador.accion <= 3:
                    jugador.derecha()
                    if jugador.rect.y != 0:
                        jugador.accion = 1
                else:
                    jugador.izquierda()
                    if jugador.rect.y != 0:
                        jugador.accion = 5

        # Colisiones Chanclas contra jugador
        for ch in proyectiles:
            colisionJugadorChanclas = pygame.sprite.spritecollide(ch, jugadores,False)
            for i in colisionJugadorChanclas:
                jugador.vida -= 1
                if jugador.tiempoStun == 0:
                    jugador.tiempoStun = 1
                proyectiles.remove(ch)

                # actualizar el movimiento del jugador con el efecto incluido
                if jugador.accion == 0:
                    jugador.idle()
                elif jugador.accion <= 3:
                    jugador.derecha()
                    if jugador.rect.y != 0:
                        jugador.accion = 1
                else:
                    jugador.izquierda()
                    if jugador.rect.y != 0:
                        jugador.accion = 5

        
        # Colisiones entre enemigos
        rangoDeChoque = 10
        for ene in enemigos:
            if ene.tipo == "mama":
                ColisionEntreEnemigos = pygame.sprite.spritecollide(ene, enemigos, False)
                for i in ColisionEntreEnemigos:
                    if i.tipo != "pereza" and abs(ene.rect.left - i.rect.right) <= rangoDeChoque:
                        i.direccion = 1
                        ene.direccion = 0
                    if i.tipo != "pereza" and abs(ene.rect.right - i.rect.left) <= rangoDeChoque:
                        i.direccion = 0
                        ene.direccion = 1
                pass

        # Colisiones Jugador con generadores
        for g in generadores:
            ColisionesGeneradores = pygame.sprite.spritecollide(jugador, generadores, False)
            for i in ColisionesGeneradores:
                if abs(jugador.rect.bottom - i.rect.top) <=10 and jugador.vely > 0 :
                    generadores.remove(i)
        # ----------------------------------------------------------------------------------------------------
        # Actualizaciones
        fondos.update()
        jugadores.update()
        enemigos.update()
        objetos.update()
        generadores.update()
        corazones.update()

        nivel_actual.update()
        plataformas.update()
        proyectiles.update()
        # Llenar pantala en caso de no tener background
        pantalla.fill([0,0,0])
        # Dibujar los objetos en la pantalla
        fondos.draw(pantalla)
        enemigos.draw(pantalla)
        jugadores.draw(pantalla)
        objetos.draw(pantalla)
        generadores.draw(pantalla)
        corazones.draw(pantalla)

        plataformas.draw(pantalla)
        nivel_actual.draw(pantalla)

        proyectiles.draw(pantalla)
        # dibujar el texto
        pantalla.blit(info,[55,20])
        pantalla.blit(tempoInfo,[ANCHO - 180,25])
        # Refrescar la pantalla
        pygame.display.flip()
        reloj.tick(FPS)
    
    # ---------------------------------------------------------------------------
    # Ciclo de fin de juego
    while True and (finDeJuego):

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Manejo de las teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                finDeJuego = False

        # Texto de fin del juego
        fuente = pygame.font.Font(None,38)
        info = fuente.render('FIN DEL JUEGO',True,[255,255,255])
        
        # dejar estatico el fondo:
        for fon in fondos:
            fon.velx = 0

        fondos.update()
        fondos.draw(pantalla)
        pantalla.blit(info,[ANCHO//2-100,ALTO//2])
        pygame.display.flip()
        pygame.quit()


        
    
    pass
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()