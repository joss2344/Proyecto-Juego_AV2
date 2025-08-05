import pygame
from game_scene import GameScene
from constants import *
from interactables import *

class MazmorraP5Scene(GameScene):
    def __init__(self, screen):
        self.map_width = 3000
        self.map_height = 830
        
        # Ajustamos la altura base del suelo para que coincida con el fondo
        ground_y = 815

        # --- PLATAFORMAS AJUSTADAS EN ALTURA Y SEPARACIÓN ---
        suelo_y = ground_y 
        platforms = [
            pygame.Rect(0, suelo_y+20, self.map_width, 50),

        ]
        
        checkpoints = [pygame.Rect(1700, ground_y - 250, 100, 100)]
        interactables = []
        player_start = (100, ground_y+5 - PLAYER_HEIGHT)

        # --- ENEMIGOS REUBICADOS Y NUEVO GOLEM AÑADIDO ---
        enemies_data = [
            (500, ground_y - 45, 0, "jades"),              
            (1750, ground_y - 240, 300, "wizzardblue"),     
            (1200, ground_y-35, 400, "depredator"),            
            (2600, ground_y-35, 200, "fire"),                  
            (1050, ground_y-35, 300, "golem_2"),               
        ]
        
        super().__init__(
            screen, MAP_MAZMORRA_P5_PATH, platforms,
            checkpoints, interactables, player_start, 
            enemies_data, self.map_width, self.map_height, 
            next_scene_name="mazmorra_p6"
        )
        
        self.music_path = "Soundtracks/soundtrack2.mp3"
        self.name = "mazmorra_p5"