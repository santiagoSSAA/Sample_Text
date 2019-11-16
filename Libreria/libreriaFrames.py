import pygame
from pygame.locals import *
# -------------------------------------------------------------------------------
# DEVOLVER UNA LISTA CON CADA SPRITE DE LA IMAGEN
def recortarSprite(pantalla,imagen, numeroColumnas, numeroFilas):
    # Aqui se almacenarán todos los sprites recortados de la imagen
    listaSprites = []
    
    # Aquí se calcula el tamaño individual de cada frame
    anchoSprite = imagen.get_rect()[2] // numeroColumnas
    altoSprite = imagen.get_rect()[3] // numeroFilas

    # Aquí se recorta cada sprite de la imagen
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
# -------------------------------------------------------------------------------
# GENERAR LA ANIMACION DE UN SPRITE
def animarSprite(pantalla, lista, numeroFrames, fila, posicion, numeroTicks):
    reloj = pygame.time.Clock()
    for i in range(numeroFrames):
        #print(i," ",fila)
        pantalla.fill([0,0,0])
        pantalla.blit(lista[fila][i],posicion)
        pygame.display.flip()
        reloj.tick(numeroTicks)
# -------------------------------------------------------------------------------