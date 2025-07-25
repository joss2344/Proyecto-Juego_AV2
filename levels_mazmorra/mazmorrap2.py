import pygame
from game_scene import GameScene
from constants import *
from interactables import *

class MazmorraP2Scene(GameScene):
    def __init__(self, screen):
        self.map_width = 3000
        self.map_height = 830
        
        ground_y = 780
        dungeon_platforms = [ pygame.Rect(0, ground_y, self.map_width, 50) ]
        dungeon_checkpoints = []
        dungeon_interactables = []
        
        player_start = (100, ground_y - PLAYER_HEIGHT)
        
        # --- LISTA SIMPLIFICADA ---
        dungeon_enemies = [
            (500, ground_y-55, 250, "golem"),
            (1000, ground_y-50, 300, "lobo"),
            (1500, ground_y-55, 200, "esqueleto"),
            (2000, ground_y-55, 250, "golem"),
            (2500, ground_y-55, 150, "esqueleto"),
        ]
        
        super().__init__(
            screen, MAP_MAZMORRA_P2_PATH, dungeon_platforms, dungeon_checkpoints,
            dungeon_interactables, player_start, dungeon_enemies,
            self.map_width, self.map_height, next_scene_name="mazmorra_jefe"
        )
        
        self.music_path = "Soundtracks/soundtrack2.mp3"
        self.name = "mazmorra_p2"