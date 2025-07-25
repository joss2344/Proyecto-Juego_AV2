import pygame
import sys
from game_scene import GameScene
from constants import *
from enemy import Boss2
from ui import BossHealthBar
from dialogue import DialogueBox
from game_state import save_game 

class MazmorraBoss2Scene(GameScene):
    def __init__(self, screen):
        self.map_width = 1920
        self.map_height = 1080
        ground_y = 900
        platforms = [pygame.Rect(0, ground_y, self.map_width, 50)]
        player_start = (200, ground_y - PLAYER_HEIGHT)
        
        super().__init__(
            screen, MAP_MAZMORRA_BOSS2_PATH, platforms,
            [], [], player_start, [], 
            self.map_width, self.map_height, 
            next_scene_name="mazmorrap5" 
        )
        self.name = "mazmorra_boss2"
        self.music_path = BOSS_MUSIC_PATH

        # --- CREACIÓN DEL JEFE NIGHTBORNE ---
        boss_start_x = self.map_width - 400
        boss_start_y = ground_y
        self.boss = Boss2(boss_start_x, boss_start_y, "nightborne")
        self.enemigos.append(self.boss)
        
        self.boss_health_bar = BossHealthBar(screen, self.boss, "NightBorne")

        # --- LÓGICA DE VICTORIA AÑADIDA ---
        self.victory_dialogue = DialogueBox(screen, text_lines=["El segundo fragmento es tuyo.", "El poder ancestral casi está completo..."], speaker_name="Eco Ancestral")
        self.victory_triggered = False
        self.sound_fragment_collected = self._load_sound("sounds/fragmento.wav")

    def respawn_player(self):
        super().respawn_player()
        
        if self.boss not in self.enemigos:
            self.enemigos.append(self.boss)
        
        self.boss.salud = self.boss.salud_maxima
        self.boss.is_dying = False
        self.boss.is_dead = False
        self.boss.action = 'idle'
        self.boss.rect.midbottom = (self.map_width - 400, 900)

    def update(self):
        if self.victory_dialogue.active:
            self.victory_dialogue.update()
            if self.victory_dialogue.finished:
                self.running = False
            return

        super().update()
        
        if self.boss in self.enemigos:
            self.boss_health_bar.update(self.boss)
        
        elif not self.enemigos and not self.victory_triggered:
            self.victory_triggered = True
            
            self.progreso_llave[1] = True 
            
            game_data = {
                "last_scene": "aldea",
                "progreso_llave": self.progreso_llave,
                "personaje": self.jugador.personaje
            }
            save_game(game_data)
            
            if self.sound_fragment_collected:
                self.sound_fragment_collected.play()
            
            self.victory_dialogue.start()
            self.stop_background_music()

    def handle_input(self, evento):
        if self.victory_dialogue.active:
            self.victory_dialogue.handle_input(evento)
        else:
            super().handle_input(evento)

    def draw(self):
        super().draw()
        if self.boss in self.enemigos:
            self.boss_health_bar.draw()
        if self.victory_dialogue.active:
            self.victory_dialogue.draw()