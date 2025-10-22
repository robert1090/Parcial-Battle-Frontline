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

    def update(self): #Actualizador de direccion a la que ira la bala segun donde mire
        
        if self.direction == "arriba":
            self.rect.y -= self.velocidad
        elif self.direction == "abajo":
            self.rect.y += self.velocidad
        elif self.direction == "izquierda":
            self.rect.x -= self.velocidad
        elif self.direction == "derecha":
            self.rect.x += self.velocidad

        if self.rect.x < 80 or self.rect.x > 1420 or self.rect.y < 150 or self.rect.y > 700:
            self.kill() #Limite hasta donde llega la bala

class BalaCooldown: #Cooldown entre disparo para las balas
    def __init__(self, bala_sprite=None, cooldown=300, tipo="player"):
        
        self.balas = pygame.sprite.Group()
        self.bala_sprite = bala_sprite #Llama el Sprite de Bala, permitiendo tambien ser modificado
        self.cooldown = cooldown #Tiempo de Cooldown
        self.ultimo_shoot = 0 #Contador de Cooldown
        self.tipo = tipo #Identificador de si es de Player o Enemy

    def shoot(self, x, y, direction):
        time = pygame.time.get_ticks()
        
        #Funcion de disparo, comprueba si el cooldown ya termino y permite disparar, para luego reiniciar el cooldown
        if time - self.ultimo_shoot >= self.cooldown:
            bala = Bala(x, y, direction, self.bala_sprite)
            self.balas.add(bala)
            self.ultimo_shoot = time

    def update(self, player=None, enemies=None, bloques=None):
        self.balas.update() #Actualizador

        #Deteccion si la bala de Enemy golpea a Player, o al reves, le resta una vida
        if self.tipo == "enemy" and player is not None:
            for bala in self.balas:
                if bala.rect.colliderect(player.rect):
                    player.vida -= 1
                    bala.kill()
        
        elif self.tipo == "player" and enemies is not None:
            for bala in self.balas:
                for enemy in enemies:
                    if bala.rect.colliderect(enemy.rect):
                        enemy.vida -= 1
                        bala.kill()
        
        #Deteccion de Bloques
        if bloques is not None:
            for bala in self.balas:
                for bloque in bloques:
                    if bala.rect.colliderect(bloque.rect):
                        bloque.hit()
                        bala.kill()

    def draw(self, screen):
        self.balas.draw(screen) #Permite dibujar las balas en pantalla