import pygame
from game_scene import GameScene
from constants import *
from interactables import *

class MazmorraP5Scene(GameScene):
    def __init__(self, screen):
        self.map_width = 3000
        self.map_height = 830
        
        # Ajustamos la altura base del suelo para que coincida con el fondo
        ground_y = 805

        # --- PLATAFORMAS AJUSTADAS EN ALTURA Y SEPARACIÓN ---
        suelo_y = ground_y +20
        platforms = [
            pygame.Rect(0, suelo_y, self.map_width, 50),

        ]
        
        checkpoints = [pygame.Rect(1700, ground_y - 250, 100, 100)]
        interactables = []
        player_start = (100, ground_y - PLAYER_HEIGHT)

        # --- ENEMIGOS REUBICADOS Y NUEVO GOLEM AÑADIDO ---
        enemies_data = [
            (500, ground_y - 30, 0, "jades"),              
            (1750, ground_y - 250, 300, "wizzardblue"),     
            (1200, ground_y, 400, "depredator"),            
            (2600, ground_y-20, 200, "fire"),                  
            (1050, ground_y, 300-25, "golem_2"),               
        ]
        
        super().__init__(
            screen, MAP_MAZMORRA_P5_PATH, platforms,
            checkpoints, interactables, player_start, 
            enemies_data, self.map_width, self.map_height, 
            next_scene_name="mazmorra_p6"
        )
        
        self.music_path = "Soundtracks/soundtrack2.mp3"
        self.name = "mazmorra_p5"