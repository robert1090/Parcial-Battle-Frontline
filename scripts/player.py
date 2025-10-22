#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import pygame
import os
from scripts.bala import BalaCooldown

#Clase Player que contiene las funciones de inicializacion, movimiento, animacion de sprite y limites
class Player:
    def __init__(self, sprite_data, spritesheet, scale=2):

        self.X = 715 #Posicion Inicial de Player
        self.Y = 690
        self.velocidad = 6 #Velocidad de movimiento
        self.radio = 20
        self.rect = pygame.Rect(self.X - 15, self.Y - 15, 60, 60) #Hitbox
        self.scale = scale #Variable para escalar el Sprite
        self.sprite_data = sprite_data["Entidad"] #Carga las coordenadas del Sprite
        self.spritesheet = spritesheet
        self.direction = "abajo" #Direccion a la que mira Player inicialmente
        self.frame_index = 0
        self.frame_delay = 10
        self.frame_counter = 0
        self.sonido = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "shot-effect.ogg") #Busca la ruta del sonido de Shoot
        self.sonido = os.path.normpath(self.sonido)
        self.bala_sprite = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "bala_player.png") #Busca el sprite de bala_player
        self.BalaCooldown = BalaCooldown(self.bala_sprite)
        self.cooldown = 300
        self.ultimo_shoot = 0
        self.vida = 3 #Cantidad de Vidas de Player
    
    def crear(self, screen):

        self.draw(screen)
    
    def mover(self, keys, screen, bloques):

        #Se asigna el valor False para identificar que no este en movimiento
        movio = False
        posicion_anterior = (self.X, self.Y) #En caso de chocar con un bloque

        #Verificamos si se preciona una tecla y pasa movido a True para animar el Sprite
        if keys[pygame.K_w]:
            self.Y -= self.velocidad
            self.direction = "arriba"
            movio = True
        elif keys[pygame.K_s]:
            self.Y += self.velocidad
            self.direction = "abajo"
            movio = True
        elif keys[pygame.K_a]:
            self.X -= self.velocidad
            self.direction = "izquierda"
            movio = True
        elif keys[pygame.K_d]:
            self.X += self.velocidad
            self.direction = "derecha"
            movio = True
                
        self.rect.left = self.X - 15
        self.rect.top = self.Y - 15

        for bloque in bloques: #Verifica colision con bloques
            if self.rect.colliderect(bloque.rect):
                self.X, self.Y = posicion_anterior
                self.rect.left = self.X - 15
                self.rect.top = self.Y - 15
        
        #Verifica si se preciona la tecla "J" para disparar
        if keys[pygame.K_j]:
            self.shoot()

        #Se mueve la Hitbox junto al Player
        self.rect.left = self.X - 15
        self.rect.top = self.Y - 15
        
        #Llama la funcion de animar si esta en movimiento y de lo contrario se queda estatico
        if movio:
            self.animar()
        else:
            self.frame_index = 1

        #dibujo del Player en pantalla
        self.draw(screen)
        self.limit() #Verifica los Limites
        self.BalaCooldown.update(enemies=[self.enemy] if hasattr(self, "enemy") else None)
        self.BalaCooldown.draw(screen)

    def shoot(self):
        tiempo = pygame.time.get_ticks()

        if tiempo - self.ultimo_shoot >= self.cooldown:
            self.ultimo_shoot = tiempo
            #Reproduce el sonido de disparo
            sonido_shoot = pygame.mixer.Sound(self.sonido)
            sonido_shoot.play()
            #Llama a la funcion para disparar en bala.py
            self.BalaCooldown.shoot(self.rect.centerx, self.rect.centery, self.direction)

    #Funcion para dibujar al Player
    def draw(self, screen):

        frame = self.sprite_data[self.direction][self.frame_index]
        sprite = self.spritesheet.get_sprite(frame["x"], frame["y"], frame["i"], frame["j"])
        
        if self.scale != 1:
            sprite = pygame.transform.scale_by(sprite, self.scale) #Permite aumentar la escala del Sprite

        screen.blit(sprite, (self.rect.left, self.rect.top))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) #Funcion solo para ver la Hitbox

    #Funcion para animar el sprite en movimiento
    def animar(self):

        self.frame_counter += 1

        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.sprite_data[self.direction])
            self.frame_counter = 0

    #Limites en Pantalla
    def limit(self):

        self.X = max(80, min(self.X, 1420))
        self.Y = max(150, min(self.Y, 700))