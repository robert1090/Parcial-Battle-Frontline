#Nombre: Robert Avila Betancour
#Matricula: 23-SISN-2-001

import pygame
import sys

#Inicializacion de Pygame
pygame.init()
#Dimensiones de la pantalla
altura = 900
anchura = 1500
pantalla = pygame.display.set_mode((anchura, altura))
pygame.mixer.init()
pygame.display.set_caption("Battle Frontline")
pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))
clock = pygame.time.Clock()

#Menu de Inicio
def Menu():
    background_menu = pygame.transform.scale(pygame.image.load("assets/images/background_menu.png"), (anchura, altura))
    font = pygame.font.SysFont(None, 45)
    menu = True
    clock = pygame.time.Clock()
    selector = None

    #Boton de Inicio y Salir
    iniciar_btn = pygame.Rect(anchura // 2 - 100, 450, 200, 60)
    salir_btn = pygame.Rect(anchura // 2 - 100, 550, 200, 60)

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
        pantalla.blit(text_iniciar, (iniciar_btn.x + 50, iniciar_btn.y + 15))
        pantalla.blit(text_salir, (salir_btn.x + 60, salir_btn.y + 15))

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

        if selector:
            pygame.mixer.Sound("assets/sounds/choice.ogg").play()
            pygame.display.flip()
            pygame.time.delay(300)
            if selector == "jugar":
                menu = False 
            elif selector == "salir":
                pygame.quit()
                sys.exit()

#Llamada al Menu
Menu()