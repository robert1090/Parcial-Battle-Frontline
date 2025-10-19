#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import pygame
import os

#Clase Bala que permite crear el sprite de bala y hacerla mover en una direccion
class Bala(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction, bala=None):
        super().__init__()
        #Verifica si Bala no tiene textura cambiada, si se cambia el sprite, por ejemplo para jugador, no carga la textura original
        if bala is None:
            bala = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "bala_enemy.png")
        
        bala = os.path.normpath(bala)
        self.image = pygame.image.load(bala).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 12 #Velocidad del proyectil
        self.direction = direction

    def update(self):
        
        if self.direction == "arriba":
            self.rect.y -= self.velocidad
        elif self.direction == "abajo":
            self.rect.y += self.velocidad
        elif self.direction == "izquierda":
            self.rect.x -= self.velocidad
        elif self.direction == "derecha":
            self.rect.x += self.velocidad

        if self.rect.x < 80 or self.rect.x > 1420 or self.rect.y < 150 or self.rect.y > 700:
            self.kill()

class BalaCooldown:
    def __init__(self, bala_sprite=None, cooldown=300):
        
        self.balas = pygame.sprite.Group()
        self.bala_sprite = bala_sprite
        self.cooldown = cooldown
        self.ultimo_shoot = 0

    def shoot(self, x, y, direction):
        time = pygame.time.get_ticks()
        
        if time - self.ultimo_shoot >= self.cooldown:
            bala = Bala(x, y, direction, self.bala_sprite)
            self.balas.add(bala)
            self.ultimo_shoot = time

    def update(self):
        self.balas.update()

    def draw(self, screen):
        self.balas.draw(screen)