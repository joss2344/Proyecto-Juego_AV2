import pygame
import sys
import os
from constants import *
from game_state import save_game, load_game, get_saved_games
from bosque_scene import BosqueScene
from aldea_scene import AldeaScene
from mazmorra_scene import MazmorraScene
from levels_mazmorra.mazmorrap1 import MazmorraP1Scene
from levels_mazmorra.mazmorrap2 import MazmorraP2Scene
from levels_mazmorra.mazmorrap3 import MazmorraP3Scene
from levels_mazmorra.mazmorrap4 import MazmorraP4Scene
from levels_mazmorra.mazmorrap5 import MazmorraP5Scene
from levels_mazmorra.mazmorra_jefe import MazmorraJefeScene
from levels_mazmorra.mazmorrap6 import MazmorraP6Scene
from levels_mazmorra.mazmorra_boss2 import MazmorraBoss2Scene
from ui import LoadGameScreen
from levels_mazmorra.mazmorra_boss3 import MazmorraBoss3Scene
from ui import LoadGameScreen
from credits import CreditsScene


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Elemental Trinity")

# ---MAPA DE ESCENAS   ---
scene_map = {
    "bosque": BosqueScene,
    "aldea": AldeaScene,
    "mazmorra": MazmorraScene,
    "mazmorra_p1": MazmorraP1Scene,
    "mazmorra_p2": MazmorraP2Scene,
    "mazmorra_p3": MazmorraP3Scene,
    "mazmorra_p4": MazmorraP4Scene,
    "mazmorra_p5": MazmorraP5Scene, 
    "mazmorra_p6": MazmorraP6Scene,
    "mazmorra_jefe": MazmorraJefeScene,
    "mazmorra_boss2": MazmorraBoss2Scene,
    "mazmorra_boss3": MazmorraBoss3Scene,
    "credits": CreditsScene, 
}

def show_credits():
    stop_menu_music() 
    credits_scene = CreditsScene(screen)
    credits_scene.run()
    play_menu_music() 

progreso_llave = [False, False, False]
global_selected_character_g = "Prota"

def run_game_loop(start_scene_name, character, key_progress):
    global progreso_llave, global_selected_character_g
    
    progreso_llave = key_progress
    selected_character_for_next_scene = character
    global_selected_character_g = character
    
    stop_menu_music()
    next_scene_name = start_scene_name

    while next_scene_name:
        # --- LÓGICA  PARA MANEJAR LA ESCENA DE CRÉDITOS ---
        if next_scene_name == "credits":
            credits_scene = CreditsScene(screen)
            credits_scene.run()
            break 
            
        current_scene_class = scene_map.get(next_scene_name)
        if not current_scene_class:
            print(f"ADVERTENCIA: Escena '{next_scene_name}' no encontrada en scene_map. Volviendo al menú.")
            break
        
        current_scene = current_scene_class(screen)
        current_scene.set_key_progress(progreso_llave)
        current_scene.name = next_scene_name
        
        next_scene_name, returned_character = current_scene.run(
            selected_character_for_this_scene=selected_character_for_next_scene
        )
        
        progreso_llave = current_scene.progreso_llave
        if returned_character:
            selected_character_for_next_scene = returned_character
            global_selected_character_g = returned_character

    play_menu_music()

def start_new_game():
    run_game_loop("bosque", "Prota", [False, False, False])

def load_and_start_game():
    load_screen = LoadGameScreen(screen)
    selected_file = load_screen.run()
    
    if selected_file:
        saved_data = load_game(selected_file)
        if saved_data:
            start_scene = saved_data.get("last_scene", "bosque")
            character = saved_data.get("personaje", "Prota")
            keys = saved_data.get("progreso_llave", [False, False, False])
            run_game_loop(start_scene, character, keys)

def stop_menu_music():
    if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()

def play_menu_music():
    try:
        if getattr(play_menu_music, 'current_song', None) != MENU_MUSIC_PATH:
            pygame.mixer.music.load(MENU_MUSIC_PATH)
            pygame.mixer.music.play(-1)
            play_menu_music.current_song = MENU_MUSIC_PATH
    except pygame.error as e: print(f"Error al reproducir música del menú: {e}")

def quit_game():
    stop_menu_music(); pygame.quit(); sys.exit()

def main_menu():
    fondo_menu = pygame.transform.scale(pygame.image.load(MENU_BACKGROUND_PATH).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # --- LÓGICA PARA CARGAR Y ESCALAR BOTONES DE IMAGEN ---
    try:
        button_images_original = {
            "Nueva Partida": pygame.image.load("interfaz/play.png").convert_alpha(),
            "Cargar Partida": pygame.image.load("interfaz/load.png").convert_alpha(),
            "Créditos": pygame.image.load("interfaz/credits.png").convert_alpha(),
            "Salir": pygame.image.load("interfaz/exit.png").convert_alpha()
        }
        button_images_scaled = {
            name: pygame.transform.scale(img, (BUTTON_WIDTH, BUTTON_HEIGHT))
            for name, img in button_images_original.items()
        }
    except pygame.error as e:
        print(f"Error al cargar las imágenes de los botones: {e}")
        return

    botones = {
        "Nueva Partida":  {"accion": start_new_game},
        "Cargar Partida": {"accion": load_and_start_game},
        "Créditos":       {"accion": show_credits}, 
        "Salir":          {"accion": quit_game}
    }
    
    # --- POSICIONAMIENTO CON TU AJUSTE DE ALTURA +230 ---
    spacing = 40
    total_area_height = (len(botones) * BUTTON_HEIGHT) + ((len(botones) - 1) * spacing)
    y_pos = (SCREEN_HEIGHT - total_area_height) // 2 + 230

    for nombre, data in botones.items():
        image = button_images_scaled.get(nombre)
        data["image"] = image
        data["rect"] = image.get_rect(centerx=SCREEN_WIDTH // 2, top=y_pos)
        y_pos += BUTTON_HEIGHT + spacing

    clock = pygame.time.Clock()

    while True:
        screen.blit(fondo_menu, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        
        # Dibuja los botones de imagen en lugar de texto
        for nombre, data in botones.items():
            if data["rect"].collidepoint(mouse_pos):
                scaled_img = pygame.transform.scale(data["image"], (int(data["rect"].width * 1.05), int(data["rect"].height * 1.05)))
                scaled_rect = scaled_img.get_rect(center=data["rect"].center)
                screen.blit(scaled_img, scaled_rect)
            else:
                screen.blit(data["image"], data["rect"])

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                quit_game()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botones["Nueva Partida"]["rect"].collidepoint(evento.pos): start_new_game()
                if botones["Cargar Partida"]["rect"].collidepoint(evento.pos):
                    if get_saved_games(): load_and_start_game()
                if botones["Créditos"]["rect"].collidepoint(evento.pos): show_credits()
                if botones["Salir"]["rect"].collidepoint(evento.pos): quit_game()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    play_menu_music()
    main_menu()