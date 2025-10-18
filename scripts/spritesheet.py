#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import pygame

#Clase para animar los Sprites
class Spritesheet:
    #Funcion para inicializar y cargar el sprite
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()
    
    #Funcion que localizar los Sprite
    def get_sprite(self, x, y, i ,j):
        
        sprite = pygame.Surface((i, j), pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, i, j))

        return sprite