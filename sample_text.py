#ODIO WINDOWS XD 2.0
import pygame
import configparser
from pygame.locals import *
# -------------------------------------------------------------------------------
import Libreria.libreriaFrames as lf
# -------------------------------------------------------------------------------
import Clases.Personajes as pp
import Clases.enemigos as e
import Clases.objetos as o
import Clases.background as ba
import Clases.plataforma as pl
import random
# -------------------------------------------------------------------------------
ANCHO = 1280
ALTO = 750
SUELO = ALTO - 100
LIMITE = ANCHO //2
LIMITEINFERIOR = ANCHO-LIMITE
FPS = 35
NUMEROVIDAS = 1
# -------------------------------------------------------------------------------
def main():
    # Definir los parametros iniciales de pygame
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    reloj = pygame.time.Clock()

    temporizador = 300
    rapidez = FPS
    contadorTiempo = 1

    # Importar las plataformas
    mapa = configparser.ConfigParser()
    mapa.read('Libreria/mapaN1.map')
    terreno_plataforma = mapa.get('info','terreno') 

    # Grupos de sprites
    generadoresPereza = pygame.sprite.Group()
    generadoresMama = pygame.sprite.Group()
    modificadores = pygame.sprite.Group()
    plataformas = pygame.sprite.Group()
    proyectiles = pygame.sprite.Group()
    corazones = pygame.sprite.Group()
    jugadores = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    objetos = pygame.sprite.Group()
    fondos = pygame.sprite.Group()

    # variables ventanas
    finDeJuego = False
    Pausa = False
    InicioJuego = True


    musica_intro = pygame.mixer.Sound('Libreria/menu_inicio.wav')
    musica_intro.play()
    

    # Cargar imagenes
    spriteSantiago = pygame.image.load("Sprites/Sprite_Sheet_Santiago.png")
    spriteMama = pygame.image.load("Sprites/Sprite_Sheet_mama.png")
    spriteObjetos = pygame.image.load("Sprites/Sprite_Sheet_Objetos.png")
    spriteBackground = pygame.image.load("Sprites/background.gif")
    spritePereza= pygame.image.load("Sprites/Sprite_Sheet_Pereza.png")
    spriteChancla = pygame.image.load("Sprites/Sprite_Sheet_Chancla.png")
    spriteGeneradorPereza = pygame.image.load("Sprites/trash.png")
    spriteTerreno =  pygame.image.load(terreno_plataforma)
    blurbackground = pygame.image.load("Sprites/blur_background.png").convert_alpha()
    backgroundInicio = pygame.image.load("Sprites/INICIO.png")

    # Generar la lista de sprites para las entidades del juego
    listaSpritesSantiago = lf.recortarSprite(pantalla,spriteSantiago,4,8)
    listaSpritesObjeto = lf.recortarSprite(pantalla,spriteObjetos,3,4)
    listaSpritesMama = lf.recortarSprite(pantalla,spriteMama,4,6)
    listaSpritesPereza = lf.recortarSprite(pantalla,spritePereza,3,1)
    listaSpritesChancla = lf.recortarSprite(pantalla,spriteChancla,4,2)

    #listaSpritesTerreno = lf.recortarSprite(pantalla,spriteTerreno,32,12)

    # Definir el objeto jugador con sus respectivas vidas
    jugador = pp.Jugador(listaSpritesSantiago)
    jugador.vida = NUMEROVIDAS
    jugadores.add(jugador)

    # Definir los objetos "corazon" representando la vida del jugador
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

    # Definir el background
    background = ba.Imagen(spriteBackground,1)
    fondos.add(background)

    # ----------------------------------------------------------------------------------------------------
    # Definir el objeto que almacena el mapa
    mp = mapa.get('info', 'mapa')# aqui guardo el mapa en la variable mp
    mp = mp.split('\n') #aqui lo guardo en listas
    fila_terreno = int(mapa.get('-', 'fil'))
    columna_terreno = int(mapa.get('-', 'col'))

    #FUNCION QUE PONE LOS SPRITES DEL MAPA EN PANTALLA
    conteoy = 0 #Conteo pixeles y
    for cada_fila in mp:
        conteox = 0 #conteo pixeles x
        for cada_elemento in cada_fila:
            #aqui, pone los sprites
            tipo = mapa.get(cada_elemento,'tipo')
            if  tipo == 'vacio':
                pass
            elif tipo == 'plataforma':
                p = pl.Plataforma(spriteTerreno,[conteox,conteoy])
                plataformas.add(p)
                jugador.lista_plataformas.append(p)
                for ene in enemigos:
                    if ene.tipo == 'mama':
                        ene.listaPlataformas.append(p)
            elif tipo == 'puerta':
                p = o.GeneradorMama(listaSpritesObjeto[3][2],5,[conteox,conteoy])
                generadoresMama.add(p)
            elif tipo == 'libro':
                l = o.Objeto(listaSpritesObjeto[0][2],1,[conteox,conteoy])
                objetos.add(l)
            elif tipo == 'photoshop':
                ph = o.Objeto(listaSpritesObjeto[2][1],3,[conteox,conteoy])
                objetos.add(ph)
            elif tipo == 'cafe':
                c = o.Cafe(listaSpritesObjeto[3][0],[conteox,conteoy])
                objetos.add(c)
            elif tipo == 'python':
                p = o.Objeto(listaSpritesObjeto[3][2],4,[conteox,conteoy])
                objetos.add(p)
            elif tipo == 'musica':
                m = o.Objeto(listaSpritesObjeto[2][0],2,[conteox,conteoy])
                objetos.add(m)
            elif tipo == 'perezita':
                p = o.GeneradorPereza(spriteGeneradorPereza,6,[conteox,conteoy])
                generadoresPereza.add(p)


            conteox += 50
        conteoy += 50

    # ----------------------------------------------------------------------------------------------------
    while True:
        #musica_ingame = pygame.mixer.Sound('Libreria/Juego_principal.wav')
        # Analizar vidas restantes
        if jugador.vida < 1:
            finDeJuego = True

        # Crea el temporizador
        fuenteTemporizador = pygame.font.Font(None,36)
        tempoInfo = fuenteTemporizador.render(("Tiempo: "+ str(temporizador)),True,[0,0,0])

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Manejo de las teclas (in game)
            if (not Pausa) and (not finDeJuego) and (not InicioJuego):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        jugador.derecha()
                    if event.key == pygame.K_LEFT:
                        jugador.izquierda()
                    if event.key == pygame.K_UP:
                        if jugador.rect.bottom > SUELO or jugador.salto_en_plataforma():
                            jugador.salto()
                    if event.key == pygame.K_p:
                        Pausa = True  
                        #musica_ingame.pause()

                if event.type == pygame.KEYUP:
                    if event.key != pygame.K_UP:
                        jugador.idle()
                        background.idle()

            # Manejo de las teclas (pausa)
            if Pausa and (not finDeJuego) and (not InicioJuego):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        Pausa = False
                        #musica_ingame.unpause()
                    if event.key == pygame.K_ESCAPE:
                        return

            
            # Manejo de las teclas (fin de juego):
            if finDeJuego and (not InicioJuego):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                        return
            
            # Manejo de las teclas (Inicio del juego):
            if InicioJuego:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        musica_intro.stop()
                        InicioJuego = False
                        #musica_ingame.play()
                    if event.key == pygame.K_ESCAPE:
                        return

        # Modos de juego
        if InicioJuego:
            # Evitar que el personaje se caiga al vacio mientras está la ventana de inicio
            for j in jugadores:
                # Reconocer que hay un suelo
                if j.rect.bottom > SUELO:
                    j.rect.bottom = SUELO
                    j.vely = 0

            # dejar estatico el fondo:
            for fon in fondos:
                fon.velx = 0
            pass

        elif (not InicioJuego) and (not Pausa) and (not finDeJuego): # ----------------------------------------------------------------------

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
                    if ene.rect.bottom >= SUELO:
                        if ene.rect.right >= background.rect.right:
                            ene.direccion = 1
                        elif ene.rect.left <= 180:
                            ene.direccion = 0
                    
                    if ene.rect.bottom < SUELO:
                        ene.rect.y += 2
                        ColisionesMamaPlataforma = pygame.sprite.spritecollide(ene, plataformas, False)
                        ene.rect.y -=2

                        for i in ColisionesMamaPlataforma:
                            print (i.rect.left, " ", ene.rect.left)
                            if ene.rect.left >= i.rect.left:
                                ene.direccion = 0   
                            if ene.rect.right <= i.rect.right:
                                ene.direccion = 1


                    
                    


                        
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

            for g in generadoresMama:
                # Generar mamas
                if len(enemigos) < (3*len(generadoresMama)):
                    if g.temp == 0:
                        g.salirSpawn = True
                    if g.salirSpawn:
                        enemigo = e.Mama(listaSpritesMama)
                        enemigo.rect.x = g.rect.x               
                        enemigo.rect.bottom =g.rect.bottom
                        enemigos.add(enemigo) 
                        g.salirSpawn = False
                # Sincronizar el movimiento de los generadores con el del entorno
                g.velx = background.velx

            for g in generadoresPereza:
                #generar perezas
                if len(enemigos) < (3*len(generadoresPereza)):
                    if g.temp == 0:
                        enemigo = e.Pereza(listaSpritesPereza)
                        enemigo.rect.x = g.rect.x + random.randrange(-30,31)
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

            for mod in modificadores:
                mod.velx = background.velx

            for pla in plataformas:
                pla.velx = background.velx
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
            for g in generadoresMama:
                ColisionesGeneradores = pygame.sprite.spritecollide(jugador, generadoresMama, False)
                for i in ColisionesGeneradores:
                    if abs(jugador.rect.bottom - i.rect.top) <=10 and jugador.vely > 0 :
                        generadoresMama.remove(i)
            
            # Colisiones entre jugador y generadores de pereza
            for g in generadoresPereza:
                ColisionesGeneradores = pygame.sprite.spritecollide(jugador, generadoresPereza, False)
                for i in ColisionesGeneradores:
                    if abs(jugador.rect.bottom - i.rect.top) <=10 and jugador.vely > 0 :
                        generadoresPereza.remove(i)
            

            # Colisiones entre jugador y modificadores
            for mod in modificadores:
                ColisionesModificadores = pygame.sprite.spritecollide(jugador, modificadores,False)
                for i in ColisionesModificadores:
                    if jugador.tiempoSpeed == 0:
                        jugador.tiempoSpeed = 2
                    if temporizador + 10 <= 300:
                        temporizador += 10
                    else:
                        temporizador = 300
                    modificadores.remove(i)

            '''

            #colisiones mama
            for ene in enemigos:
                if ene.tipo == 'mama':
                    ene.rect.y += 2
                    ColisionesMamaPlataforma = pygame.sprite.spritecollide(ene, ene.listaPlataformas, False)
                    ene.rect.y -= 2

                    if ene.rect.bottom < SUELO or len(ColisionesMamaPlataforma) > 0:
                        print ('yayyy')
                        #TODO: revisar donde se generan las mamas y hacer que aparezcan un poquito mas abajo
                        #y ahi si hacer el codigo de las colisiones.
                        for i in ColisionesMamaPlataforma:
                            print ('puta vida')
                            if ene.rect.left >= i.rect.left:
                                ene.direccion = 0   
                            if ene.rect.right <= i.rect.right:
                                ene.direccion = 1
                '''

        elif Pausa: # ------------------------------------------------------------------------

            # evitar que el jugador caiga al vacio en la pausa
            for j in jugadores:
                if j.rect.bottom > SUELO:
                    j.rect.bottom = SUELO
                    j.vely = 0

            # Texto de pausa
            fuente = pygame.font.Font(None,38)
            pausa = fuente.render('PAUSA',True,[255,255,255])
            pantalla.blit(pausa,[ANCHO//2,ALTO//2])

            # Poner el fondo estatico
            for fon in fondos:
                fon.velx = 0

            pass
        elif finDeJuego: # --------------------------------------------------------------------------------------

            for j in jugadores:
                # Reconocer que hay un suelo
                if j.rect.bottom > SUELO:
                    j.rect.bottom = SUELO
                    j.vely = 0

            # Texto de fin del juego
            fuente = pygame.font.Font(None,38)
            info = fuente.render('FIN DEL JUEGO',True,[255,255,255])
            pantalla.blit(info,[ANCHO//2-100,ALTO//2])      
            
            # dejar estatico el fondo:
            for fon in fondos:
                fon.velx = 0

            pass         
    
        # ----------------------------------------------------------------------------------------------------
        # Actualizaciones
        if (not Pausa) and (not finDeJuego):
            fondos.update()
            jugadores.update()
            enemigos.update()
            objetos.update()
            generadoresMama.update()
            generadoresPereza.update()
            corazones.update()
            proyectiles.update()
            modificadores.update()
            plataformas.update()
        # Llenar pantala en caso de no tener background
        pantalla.fill([0,0,0])
        # Dibujar los objetos en la pantalla
        if not InicioJuego:
            fondos.draw(pantalla)
            if not finDeJuego:
                enemigos.draw(pantalla)
                jugadores.draw(pantalla)
                objetos.draw(pantalla)
                generadoresMama.draw(pantalla)
                generadoresPereza.draw(pantalla)
                corazones.draw(pantalla)
                proyectiles.draw(pantalla)
                modificadores.draw(pantalla)
                plataformas.draw(pantalla)
            if Pausa:
                pantalla.blit(blurbackground,[0,0])
        else:
            pantalla.blit(backgroundInicio,[0,0])
        # dibujar el texto

        if (not InicioJuego) and (not Pausa) and (not finDeJuego):
            fuente = pygame.font.Font(None,24)
            infovidas = fuente.render("VIDAS",True,[0,0,0])
            pantalla.blit(infovidas,[55,20])
            pantalla.blit(tempoInfo,[ANCHO - 180,25])
            pass
        elif Pausa:
            fuente = pygame.font.Font(None,96)
            fuentePequena = pygame.font.Font(None,24)
            fuenteMediana = pygame.font.Font(None, 36)

            info = fuente.render("PAUSA",True,[255,255,255])
            infovidas = fuentePequena.render("VIDAS",True,[0,0,0])
            opcion1 = fuenteMediana.render("Reanudar (x)",True,[255,255,255])
            opcion2 = fuenteMediana.render("Salir (ESC)",True,[255,255,255])

            pantalla.blit(infovidas,[55,20])
            pantalla.blit(info,[ANCHO//2 -100,300])
            pantalla.blit(tempoInfo,[ANCHO - 180,25])
            pantalla.blit(opcion1,[ANCHO//2 -80,390])
            pantalla.blit(opcion2,[ANCHO//2 -80,450])
            pass
        elif finDeJuego:
            fuente = pygame.font.Font(None,96)
            fuenteMediana = pygame.font.Font(None, 36)

            info = fuente.render("FIN DE JUEGO",True,[255,255,255])
            opcion1 = fuenteMediana.render("Reiniciar (r)",True,[255,255,255])
            opcion2 = fuenteMediana.render("Salir (ESC)",True,[255,255,255])

            pantalla.blit(info,[ANCHO//2 -180,300])
            pantalla.blit(opcion1,[ANCHO//2 -80,450])
            pantalla.blit(opcion2,[ANCHO//2 -80,510])
            pass
        elif InicioJuego:
            fuenteMediana = pygame.font.Font(None, 36)
            opcion1 = fuenteMediana.render("Jugar (c)",True,[255,255,255])
            opcion2 = fuenteMediana.render("Salir (ESC)",True,[255,255,255])

            pantalla.blit(opcion1,[ANCHO//2 -80,390])
            pantalla.blit(opcion2,[ANCHO//2 -80,450])
            pass
        # Refrescar la pantalla
        pygame.display.flip()
        reloj.tick(FPS)
    
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()