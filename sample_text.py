#ODIO WINDOWS XD 2.0
import pygame
from pygame.locals import *
# -------------------------------------------------------------------------------
import Libreria.libreriaFrames as lf
# -------------------------------------------------------------------------------
import Clases.Personaje_principal as pp
import Clases.enemigos as e
import Clases.objetos as o
import Clases.background as b
import Clases.generadores as ge
import Clases.corazones as cor
import random
# -------------------------------------------------------------------------------
ANCHO = 1280
ALTO = 720
SUELO = 660
LIMITE = 1150
LIMITEINFERIOR = ANCHO-LIMITE
FPS = 35
NUMEROVIDAS = 5
# -------------------------------------------------------------------------------
def main():
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    reloj = pygame.time.Clock()

    # Texto de vidas
    fuente = pygame.font.Font(None,24)
    info = fuente.render("VIDAS",True,[0,0,0])
    # Grupos de sprites
    modificadores = pygame.sprite.Group()
    generadores = pygame.sprite.Group()
    spawnMamas = pygame.sprite.Group()
    corazones = pygame.sprite.Group()
    jugadores = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    objetos = pygame.sprite.Group()
    fondos = pygame.sprite.Group()

    # variables ventanas
    finDeJuego = False

    # Cargar imagenes
    spriteSantiago = pygame.image.load("Sprites/Sprite_Sheet_Santiago.png").convert_alpha()
    spriteMama = pygame.image.load("Sprites/Sprite_Sheet_mama.png").convert_alpha()
    spriteObjetos = pygame.image.load("Sprites/Sprite_Sheet_Objetos.png").convert_alpha()
    spriteBackground = pygame.image.load("Sprites/background.png").convert_alpha()

    # lista de sprites
    listaSpritesSantiago = lf.recortarSprite(pantalla,spriteSantiago,4,8)
    listaSpritesObjeto = lf.recortarSprite(pantalla,spriteObjetos,3,4)
    listaSpritesMama = lf.recortarSprite(pantalla,spriteMama,4,6)

    # Sprites y clase Santiago
    jugador = pp.Jugador(listaSpritesSantiago)
    jugador.vida = NUMEROVIDAS
    jugadores.add(jugador)

    # Sprites y clase objeto
    for i in range(1,5):
        objeto = None
        if i  == 1:
            objeto = o.Objeto(listaSpritesObjeto[0][2],i)
        else:
            objeto = o.Objeto(listaSpritesObjeto[2][i-2],i)
        objetos.add(objeto)
    
    # Sprites y clase corazones
    numero_Corazones = jugador.vida
    for i in range(1,numero_Corazones+1):
        c = cor.Corazon(listaSpritesObjeto,i)
        corazones.add(c)
        c.rect.x = 10 + (35*i)


    # crea puertas (generadores de enemigos)
    numero_Puertas = random.randrange(1,5)
    for i in range(numero_Puertas):
        puerta = ge.Generador(listaSpritesObjeto[3][2],5,SUELO)
        generadores.add(puerta)

    # Sprites y clase imagen
    background = b.Imagen(spriteBackground,1)
    fondos.add(background)

    while True and (not finDeJuego):
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
                    if jugador.rect.bottom > SUELO:
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
            if j.rect.right > LIMITE and j.accion in [1,3]:
                j.rect.right = LIMITE
                background.izquierda()
            elif background.rect.left < 0 and j.rect.right < LIMITEINFERIOR and j.accion in [5,6]:
                j.rect.right = LIMITEINFERIOR
                background.derecha()
            elif j.rect.left < 0:
                j.rect.left = 0
            else:
                background.idle()
            
            # Aumentar el contador de animacion del jugador
            if j.contadorAnimacion < FPS:
                j.contadorAnimacion += 1
            else:
                j.contadorAnimacion = 1

        for ene in enemigos:
            ene.idle()
            # Eleccion direccion movimiento mama
            if ene.direccion == 0:
                ene.derecha()
            elif ene.direccion == 1:
                ene.izquierda()
            
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

        for ob in objetos:
            # Sincronizar el movimiento de los objetos con el del fondo
            if ob.rect.y != 30:
                ob.velx = background.velx

        #Creador Spawns Mama
        for g in generadores:
            if len(enemigos) < (3*len(generadores)):
                if g.temp == 0:
                    g.salirSpown = True
                if g.salirSpown:
                    spMama = e.Mama(listaSpritesMama)
                    spMama.rect.x = g.rect.x               
                    spMama.rect.bottom =g.rect.bottom
                    enemigos.add(spMama)
                    g.salirSpown = False
                    g.temp = random.randrange(100,150)
            
            # Sincronizar el movimiento de los generadores con el del entorno
            g.velx = background.velx
        
        for c in corazones:
            # Desaparicion de vidas
            if jugador.vida < NUMEROVIDAS:
                if c.identificador == jugador.vida+1:
                    c.corazonInactivo()
        # ----------------------------------------------------------------------------------------------------
        # Colisiones con objetos
        listaColisiones = pygame.sprite.spritecollide(jugador, objetos, False)
        if len(listaColisiones) > 0:
            listaColisiones[0].rect.x = 300 + (50*(listaColisiones[0].identificador))
            listaColisiones[0].rect.y = 30
            jugador.objetosObtenidos.append(listaColisiones[0].identificador)

        #Colisiones jugador a Enemigos
        for ene in enemigos:
            ColisionesEnemigos = pygame.sprite.spritecollide(jugador, enemigos, False)
            for i in ColisionesEnemigos:
                if abs(jugador.rect.bottom - i.rect.top) <= 5 and jugador.vely > 0 :
                    enemigos.remove(i)
      
        #Colisiones Enemigos contra el jugador
        for ene in enemigos:
            ColisionJugadorEnemigo = pygame.sprite.spritecollide(ene, jugadores, False)
            for i in ColisionJugadorEnemigo:
                if abs(ene.rect.left - i.rect.right) <= 10 or abs(ene.rect.right - i.rect.left) <= 10:
                    vidas = jugador.vida
                    jugadores.remove(i)
                    vidas -= 1
                    jugador = pp.Jugador(listaSpritesSantiago)
                    jugadores.add(jugador)
                    jugador.idle()
                    jugador.vida = vidas

        # ----------------------------------------------------------------------------------------------------
        # Actualizaciones
        fondos.update()
        jugadores.update()
        enemigos.update()
        objetos.update()
        generadores.update()
        spawnMamas.update()
        corazones.update()
        # Llenar pantala en caso de no tener background
        pantalla.fill([0,0,0])
        # Dibujar los objetos en la pantalla
        fondos.draw(pantalla)
        enemigos.draw(pantalla)
        jugadores.draw(pantalla)
        objetos.draw(pantalla)
        generadores.draw(pantalla)
        spawnMamas.draw(pantalla)
        corazones.draw(pantalla)
        pantalla.blit(info,[55,20])
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

        # Texto de fin del juego
        fuente = pygame.font.Font(None,38)
        texto = 'FIN DEL JUEGO'
        info = fuente.render(texto,True,[255,255,255])
        fondos.update()
        fondos.draw(pantalla)
        pantalla.blit(info,[ANCHO//2-100,ALTO//2])
        pygame.display.flip()

        
    
    pass
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()