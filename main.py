#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import pygame
import sys
from scripts.player import Player
from scripts.spritesheet import Spritesheet
from scripts.enemy import Enemy
from scripts.bloque import Bloque
import json
import random
import os

#Inicializacion de Pygame
pygame.init()
#Dimensiones de la pantalla
os.environ['SDL_VIDEO_CENTERED'] = '1'
altura = 900
anchura = 1500
pantalla = pygame.display.set_mode((anchura, altura), pygame.RESIZABLE)
pygame.mixer.init()
pygame.display.set_caption("Battle Frontline")
pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))
background = pygame.transform.scale(pygame.image.load("assets/images/background.png"), (anchura, altura))
clock = pygame.time.Clock()
score = 0

with open("scripts/coordenadas_sprite.json") as f:
    sprite_data = json.load(f)

with open("scripts/posiciones_bloques.json", "r") as f:
    posiciones_bloques = json.load(f)

#Menu de Inicio
def Menu():
    global pantalla, anchura, altura
    background_menu = pygame.transform.scale(pygame.image.load("assets/images/background_menu.png"), (anchura, altura))
    font = pygame.font.Font("assets/fonts/DeltaForce.ttf", 40)
    menu = True
    clock = pygame.time.Clock()
    splash = pygame.transform.scale(pygame.image.load("assets/images/Battle-Frontline-Logo.png").convert_alpha(), (400, 200))
    selector = None

    #Cargamos la musica
    pygame.mixer.music.load("assets/music/save-as.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #Boton de Inicio y Salir
    iniciar_btn = pygame.Rect(100, 450, 200, 60)
    salir_btn = pygame.Rect(100, 550, 200, 60)

    #While del Menu
    while menu:
        clock.tick(60)
        pantalla.fill((0, 0, 0))
        pantalla.blit(background_menu, (0, 0))

        #Dibujar Botones
        boton_a = pygame.transform.scale(pygame.image.load("assets/images/boton_a.png").convert_alpha(), (40, 40))
        boton_b = pygame.transform.scale(pygame.image.load("assets/images/boton_b.png").convert_alpha(), (40, 40))
        pygame.draw.rect(pantalla, (255, 0, 0), iniciar_btn)
        pygame.draw.rect(pantalla, (255, 0, 0), salir_btn)
        text_iniciar = font.render("Iniciar", True, (255, 255, 255))
        text_salir = font.render("Salir", True, (255, 255, 255))
        pantalla.blit(text_iniciar, (iniciar_btn.x + 40, iniciar_btn.y + 15))
        pantalla.blit(text_salir, (salir_btn.x + 50, salir_btn.y + 15))

        #Dibujar el Titulo
        splash_rect = splash.get_rect(center=(250, 150))
        pantalla.blit(splash, splash_rect)

        pygame.display.flip()

        #Captura de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if iniciar_btn.collidepoint(event.pos):
                    selector = "jugar" 
                elif salir_btn.collidepoint(event.pos):
                    selector = "salir"

            elif event.type == pygame.VIDEORESIZE:
                anchura, altura = event.w, event.h
                pantalla = pygame.display.set_mode((anchura, altura), pygame.RESIZABLE)
                background_menu = pygame.transform.scale(pygame.image.load("assets/images/background_menu.png"), (anchura, altura))

        if selector:
            pygame.mixer.Sound("assets/sounds/choice.ogg").play()
            pygame.display.flip()
            pygame.mixer.music.stop()
            pygame.time.delay(300)
            if selector == "jugar":
                menu = False
                Play()
            elif selector == "salir":
                pygame.quit()
                sys.exit()

#Funcion de Juego
def Play():
    
    run = True #Varibale que dara a entender que el bucle siga ejecutandose
    global pantalla, background

    #Cargamos la musica
    pygame.mixer.music.load("assets/music/battle-woods.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    player = Player(sprite_data, Spritesheet("assets/images/player.png")) #Carga la clase Player y carga los Sprite
    player.crear(pantalla) #Se dibuja en pantalla al Player

    vida = pygame.image.load("assets/images/corazones.png").convert_alpha()
    vida = pygame.transform.scale(vida, (40, 40))

    #Creacion de Bloques en el Mapa
    bloques = pygame.sprite.Group()
    for x, y in posiciones_bloques:
        bloque = Bloque(x, y, "assets/images/bloque.png")
        bloques.add(bloque)

    mapa = [[0]*50 for _ in range(30)]  #Grid Libre para mapa

    #Marca la posicion de los bloques en el mapa
    for bloque in bloques:
        tile_x = bloque.rect.left // 32
        tile_y = bloque.rect.top // 32
        ancho_tiles = bloque.rect.width // 32
        alto_tiles = bloque.rect.height // 32
        for x in range(tile_x, tile_x + ancho_tiles):
            for y in range(tile_y, tile_y + alto_tiles):
                mapa[y][x] = 1

    max_enemy = 6 #Maximo de Enemys
    enemys = [] #Array donde se almacenaran los Enemys
    spawn_enemy = 1500 #Tiempo de Spawn de cada Enemy
    ultimo_spawn = 0 #Contador de Tiempo desde el ultimo Spawn

    #Posicion Aleatoria de Spawn para Enemy
    posiciones = [(200, 400), (1300, 400), (250, 700), (1250, 700), (200, 200), (1300, 200)]

    #Puntaje
    global score
    score = 0

    #Bucle del Juego
    while run:
        tiempo = pygame.time.get_ticks()
        for event in pygame.event.get(): #Captura de Eventos del Juego
            if event.type == pygame.QUIT:
                #Funcion para cerrar la ventana y matar la ejecucion
                run = False
                break

        if event.type == pygame.VIDEORESIZE:
            anchura, altura = event.w, event.h
            pantalla = pygame.display.set_mode((anchura, altura), pygame.RESIZABLE)
            background = pygame.transform.scale(pygame.image.load("assets/images/background.png"), (anchura, altura))

        pantalla.fill((0,0,0)) #Imprimimos un Fondo Negro
        clock.tick(60) #Limite de FPS
        pantalla.blit(background, (0,0)) #Imprime el Escenario

        player.mover(pygame.key.get_pressed(), pantalla, bloques) #Captura los botones precionados para mover a Player

        if tiempo - ultimo_spawn >= spawn_enemy and len(enemys) < max_enemy: #Crea un Enemy cada vez que el tiempo de Spawn se cumple
            posicion = random.choice(posiciones)
            enemy = Enemy(sprite_data, Spritesheet("assets/images/enemy.png"), player, mapa, posicion)
            enemys.append(enemy)
            player.enemy = enemy #Pasa referencia de Enemy a Player
            ultimo_spawn = tiempo
    
        #Actualizador de Enemys
        for enemigo in enemys[:]:
            enemigo.update(pantalla, bloques)
            if enemigo.vida <= 0:
                enemys.remove(enemigo)
                score += 10 #Aumenta el puntaje al eliminar un Enemy


        #Muestra en pantalla a los Enemys cada vez que se crean
        for enemigo in enemys:
            enemigo.crear(pantalla)

        for bloque in bloques:
            bloque.draw(pantalla)

        player.BalaCooldown.update(enemies=enemys, bloques=bloques) #Actualizador de las Balas de Player

        #Dibuja Vidas en Pantalla
        for i in range(player.vida):
            pantalla.blit(vida, (20 + i*50, 20))

        pygame.display.flip()#Actualizador de Pantalla

        #Condicion para que ocurra el Gameover
        if player.vida == 0:
            pygame.mixer.music.stop()
            Gameover()
            return
        
def Gameover(): #Menu de Gameover
    
    run = True #Varibale que dara a entender que el bucle siga ejecutandose
    gameover = pygame.transform.scale(pygame.image.load("assets/images/gameover.png").convert_alpha(), (400, 200))
    font = pygame.font.Font("assets/fonts/DeltaForce.ttf", 40)
    reiniciar_btn = pygame.Rect(anchura/2 - 110, 450, 220, 60)
    salir_btn = pygame.Rect(anchura/2 - 100, 550, 200, 60)
    selector = None

    #Cargamos la musica
    gameover_sound = pygame.mixer.Sound("assets/music/game-over.ogg")
    gameover_sound.set_volume(0.5)
    gameover_sound.play()

    #Bucle del Menu de Gameover
    while run:
        pantalla.fill((0,0,0)) #Imprimimos un Fondo Negro
        clock.tick(60) #Limite de FPS
        gameover_rect = gameover.get_rect(center=(anchura/2, 150))
        pantalla.blit(gameover, gameover_rect)

        pygame.draw.rect(pantalla, (255, 0, 0), reiniciar_btn)
        pygame.draw.rect(pantalla, (255, 0, 0), salir_btn)
        text_reiniciar = font.render("Reintentar", True, (255, 255, 255))
        text_salir = font.render("Salir", True, (255, 255, 255))
        pantalla.blit(text_reiniciar, (reiniciar_btn.x, reiniciar_btn.y + 15))
        pantalla.blit(text_salir, (salir_btn.x + 50, salir_btn.y + 15))

        text_score = font.render("Puntuaje: " + str(score), True, (255, 255, 255))
        pantalla.blit(text_score, (anchura/2 - 120, 350))

        pygame.display.flip()

        #Captura de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reiniciar_btn.collidepoint(event.pos):
                    selector = "reiniciar" 
                elif salir_btn.collidepoint(event.pos):
                    selector = "salir"

        if selector:
            pygame.mixer.Sound("assets/sounds/choice.ogg").play()
            pygame.display.flip()
            pygame.time.delay(300)
            if selector == "reiniciar":
                run = False
                Play()
                return
            elif selector == "salir":
                pygame.quit()
                sys.exit()

#Llamada al Menu
Menu()