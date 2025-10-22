#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import pygame

#Clase de Bloques que seran obstaculos destruibles en el mapa
class Bloque(pygame.sprite.Sprite):
    def __init__(self, X, Y, imagen):
        super().__init__()

        self.X = X
        self.Y = Y
        self.imagen = imagen
        self.bloque = pygame.image.load(imagen).convert_alpha()
        self.rect = pygame.Rect(self.X - 15, self.Y - 15, 60, 60) #Hitbox
        self.vida = 2 #Vida del Bloque antes de ser destruido

    def hit(self): #funcion para que cuando la vida llegue a 0 sea eliminado
        self.vida -= 1
        if self.vida == 0:
            self.kill()

    def draw(self, screen): #Funcion para dibujar el bloque en pantalla
        screen.blit(self.bloque, (self.rect.left, self.rect.top))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) #Funcion solo para ver la Hitbox