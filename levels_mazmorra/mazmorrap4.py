import pygame
from game_scene import GameScene
from constants import *
from interactables import *

class MazmorraP4Scene(GameScene):
    def __init__(self, screen):
        self.map_width = 2500
        self.map_height = 830
        ground_y = 750

        # --- PLATAFORMAS AJUSTADAS EN ALTURA Y SEPARACIÓN ---
        suelo_y = ground_y - 20
        platforms = [
            # Plataforma principal del suelo
            pygame.Rect(0, suelo_y, self.map_width, 50),

        ]

        checkpoints = [
             pygame.Rect(1500, suelo_y - PLAYER_HEIGHT - 20, 100, 100) 
        ]

        interactables = []
        player_start = (100, suelo_y - PLAYER_HEIGHT)

        # --- ENEMIGOS CON ALTURA REAJUSTADA ---
        enemy_offset = -45

        enemies_data = [
            (500, suelo_y + enemy_offset, 300, "depredator"),
            (1150, suelo_y - 275, 100, "wizzardblue"),
            (1700, suelo_y + enemy_offset, 200, "fire"),
            (1950, suelo_y + enemy_offset, 200, "wind"),
            (2300, suelo_y + enemy_offset, 0, "jades"),
        ]

        super().__init__(
            screen, MAP_MAZMORRA_P4_PATH, platforms,
            checkpoints,
            interactables,
            player_start,
            enemies_data,
            self.map_width, self.map_height,
            next_scene_name="mazmorra_boss2"
        )

        self.name = "mazmorra_p4"