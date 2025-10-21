#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import pygame
import math
import heapq
from scripts.bala import BalaCooldown

#Nodos necesarios para el Arbol de Comportamiento
class Nodo:
    def __init__(self):
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def ejecutar(self):
        pass

class Selector(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False

class Secuencia(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True

class Accion(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        return self.accion()

class Invertir(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):
        return not self.hijos[0].ejecutar()

#Creacion de la clase de Enemigos
class Enemy:
    def __init__(self, sprite_data, spritesheet, player, mapa, posiciones, scale=2):
        self.X, self.Y = posiciones
        self.velocidad = 4 #Velocidad de movimiento de Enemy
        self.radio = 20
        self.scale = scale
        self.sprite_data = sprite_data["Entidad"] #Carga las coordenadas del Sprite
        self.spritesheet = spritesheet
        self.direction = "abajo" #Direccion incial a la que mira
        self.shoot_direction = "abajo"
        self.rect = pygame.Rect(self.X - 15, self.Y - 15, 60, 60) #Hitbox
        self.player = player
        self.mapa = mapa
        self.tile_size = 32
        self.distancia_disparo = 400 #Distancia a la que comenzara a disparar del Player
        self.cooldown = 900 #Cooldown del Disparo
        self.ultimo_shoot = 0
        self.balas = BalaCooldown(cooldown=self.cooldown, tipo="enemy")
        self.camino = [] #Pathfinding
        self.ultima_busqueda = 0
        self.intervalo_busqueda = 500  #Tiempo de recarculando la busqueda
        self.comportamiento = self.arbol()
        self.frame_index = 0
        self.frame_delay = 10
        self.frame_counter = 0
        self.vida = 1 #Cantidad de Vidas de Enemy

    def crear(self, screen):

        self.draw(screen)

    #Funcion para dibujar a los Enemy
    def draw(self, screen):
        frame = self.sprite_data[self.direction][self.frame_index]
        sprite = self.spritesheet.get_sprite(frame["x"], frame["y"], frame["i"], frame["j"])

        if self.scale != 1:
            sprite = pygame.transform.scale_by(sprite, self.scale)

        screen.blit(sprite, (self.rect.left, self.rect.top))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) #Funcion solo para ver la Hitbox

    #Funcion para animar el sprite en movimiento
    def animar(self, moviendo):
        if moviendo:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_index = (self.frame_index + 1) % len(self.sprite_data[self.direction])
                self.frame_counter = 0
        else:
            self.frame_index = 0 

    #Utiliza A_Star para encontrar a Player
    def buscar_player(self):
        tiempo = pygame.time.get_ticks()
        moviendo = False  

        #Recalcula el camino
        if tiempo - self.ultima_busqueda > self.intervalo_busqueda:
            inicio = self.pixel_a_tile(self.rect.center)
            destino = self.pixel_a_tile(self.player.rect.center)
            self.camino = self.a_star(inicio, destino)
            self.ultima_busqueda = tiempo

        if self.camino:
            siguiente_tile = self.camino[0]
            siguiente_px = self.tile_a_pixel(siguiente_tile)
            dx = siguiente_px[0] - self.rect.centerx
            dy = siguiente_px[1] - self.rect.centery
            distancia_al_tile = math.hypot(dx, dy)
            distancia_al_player = math.hypot(self.player.rect.centerx - self.rect.centerx,
                                            self.player.rect.centery - self.rect.centery)

            alineado = self.player_alineado()

            #Evita que se mueva al menos que este lejos o no este alineado
            if distancia_al_tile > 4 and (distancia_al_player > self.distancia_disparo or not alineado):
                self.rect.x += int(self.velocidad * dx / distancia_al_tile)
                self.rect.y += int(self.velocidad * dy / distancia_al_tile)
                moviendo = True  

                # Actualizar dirección según vector de movimiento
                if abs(dx) > abs(dy):
                    self.direction = "izquierda" if dx > 0 else "derecha"
                else:
                    self.direction = "abajo" if dy > 0 else "arriba"
            else:
                self.camino.pop(0)

        #Anima el sprite
        self.animar(moviendo)

        return True

    #Verifica si el Player esta alineado
    def player_alineado(self):
        dx = abs(self.player.rect.centerx - self.rect.centerx)
        dy = abs(self.player.rect.centery - self.rect.centery)
        return dx < 20 or dy < 20
    
    #Verifica si esta a la distancia correcta
    def player_distancia(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        return distancia <= self.distancia_disparo
    
    #Funcion de Disparo
    def shoot(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_shoot >= self.cooldown:
            self.ultimo_shoot = tiempo_actual

            # Calcular dirección de disparo correcta
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery

            if abs(dx) > abs(dy):
                self.shoot_direction = "derecha" if dx > 0 else "izquierda"
            else:
                self.shoot_direction = "abajo" if dy > 0 else "arriba"

            self.balas.shoot(self.rect.centerx, self.rect.centery, self.shoot_direction)
            return True
        return False
    
    #Arbol de Comportamiento
    def arbol(self):
        secuencia_atacar = Secuencia()
        secuencia_atacar.agregar_hijo(Accion(self.buscar_player))
        secuencia_atacar.agregar_hijo(Accion(self.player_alineado))
        secuencia_atacar.agregar_hijo(Accion(self.player_distancia))
        secuencia_atacar.agregar_hijo(Accion(self.shoot))

        raiz = Selector()
        raiz.agregar_hijo(secuencia_atacar)

        return raiz
    
    #Actualizador
    def update(self, screen):
        self.comportamiento.ejecutar()
        self.balas.update(player=self.player)
        self.balas.draw(screen)

    #Implementacion de A* para buscar al player
    def a_star(self, inicio, destino):
        def heuristica(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        direcciones = [(0,1),(1,0),(0,-1),(-1,0)]
        frontera = []
        heapq.heappush(frontera, (0, inicio))
        de_donde_viene = {inicio: None}
        costo_hasta_ahora = {inicio: 0}

        while frontera:
            _, actual = heapq.heappop(frontera)
            if actual == destino:
                break

            for dx, dy in direcciones:
                vecino = (actual[0] + dx, actual[1] + dy)
                if not self.camino_valido(vecino):
                    continue

                nuevo_costo = costo_hasta_ahora[actual] + 1
                if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:
                    costo_hasta_ahora[vecino] = nuevo_costo
                    prioridad = nuevo_costo + heuristica(destino, vecino)
                    heapq.heappush(frontera, (prioridad, vecino))
                    de_donde_viene[vecino] = actual

        actual = destino
        camino = []
        while actual in de_donde_viene and de_donde_viene[actual] is not None:
            camino.append(actual)
            actual = de_donde_viene[actual]
        camino.reverse()
        return camino

    #Convertidor de Coordenadas Pixeles a Coordenadas de Tile
    def pixel_a_tile(self, pos):
        return (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

    #Convertidor de Coordenadas de Tile a Coordenadas de Pixeles
    def tile_a_pixel(self, tile):
        return (tile[0] * self.tile_size + self.tile_size // 2,
                tile[1] * self.tile_size + self.tile_size // 2)

    #Verifica que es valido el camino
    def camino_valido(self, tile):
        x, y = tile
        if x < 0 or y < 0 or y >= len(self.mapa) or x >= len(self.mapa[0]):
            return False
        return self.mapa[y][x] == 0 