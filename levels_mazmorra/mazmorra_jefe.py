#
# Contenido para el archivo: mazmorra_jefe.py
#
import pygame
from game_scene import GameScene
from constants import *
from dialogue import DialogueBox
from aldea_scene import global_selected_character_g
from enemy import Boss1
from ui import BossHealthBar
from interactables import *

class MazmorraJefeScene(GameScene):
    def __init__(self, screen):
        self.map_width = 1920
        self.map_height = 1080
        
        ground_y = 900
        dungeon_platforms = [ pygame.Rect(0, ground_y, self.map_width, 50) ]
        dungeon_checkpoints = [ pygame.Rect(150, 800, 100, 100) ]
        dungeon_interactables = []
        player_start = (150, ground_y - PLAYER_HEIGHT)
        dungeon_enemies = []

        super().__init__(
            screen, MAP_MAZMORRA_JEFE_PATH, dungeon_platforms,
            dungeon_checkpoints,
            dungeon_interactables,
            player_start, 
            dungeon_enemies,
            self.map_width, self.map_height, 
            next_scene_name="mazmorra_p3"
        )
        
        self.boss = Boss1(self.map_width - 300, ground_y-35, "boss1")
        self.enemigos.append(self.boss)
        
        self.boss_name = "Entidad Oscura del Vacío"
        self.boss_health_bar = BossHealthBar(screen, self.boss, self.boss_name)
        
        ### NUEVO: DIÁLOGO DE INTRODUCCIÓN DEL JEFE ###
        self.intro_dialogue = DialogueBox(
            screen,
            text_lines=[
                "¡Prepárate, Guardián!",
                f"Ante ti se alza la {self.boss_name}...",
                "Es el primer gran carcelero, una abominación nacida de las sombras para proteger los secretos del Clan Umbral.",
                "En su corrupto corazón resguarda el primer fragmento de la Llave Solar.",
                "¡Libéralo de su tormento y reclama lo que es nuestro! ¡Tu verdadera prueba comienza ahora!"
            ],
            speaker_name="Eco Ancestral"
        )
        self.intro_dialogue.start() # Inicia el diálogo al cargar la escena
        ### FIN DE LA SECCIÓN NUEVA ###

        self.victory_dialogue = DialogueBox(screen, text_lines=["¡Has conseguido el primer fragmento!", "Pero tu aventura apenas comienza..."], speaker_name="Eco Ancestral")
        self.victory_dialogue_triggered = False
        self.sound_fragment_collected = self._load_sound("sounds/fragmento.wav")
        
        self.music_path = BOSS_MUSIC_PATH
        self.name = "mazmorra_jefe"

    def respawn_player(self):
        super().respawn_player()
        if self.boss not in self.enemigos:
            self.enemigos.append(self.boss)
        self.boss.salud = self.boss.salud_maxima
        self.boss.is_dying = False
        self.boss.is_dead = False
        self.boss.action = 'idle' 
        self.boss.rect.midbottom = (self.map_width - 300, 900) 

    def update(self):
        ### NUEVO: MANEJO DEL DIÁLOGO DE INTRODUCCIÓN ###
        if self.intro_dialogue.active:
            self.intro_dialogue.update()
            self.jugador.vel_x = 0 # Congela al jugador
            return # Detiene el resto de la lógica
        ### FIN DE LA SECCIÓN NUEVA ###
            
        if self.victory_dialogue.active:
            self.victory_dialogue.update()
            if self.victory_dialogue.finished:
                self.running = False 
            return 
            
        super().update()

        if self.boss in self.enemigos:
            self.boss_health_bar.update(self.boss)
        
        if not self.enemigos and not self.victory_dialogue_triggered:
            self.progreso_llave[0] = True 
            self.can_save = True 
            if self.sound_fragment_collected:
                self.sound_fragment_collected.play()
            self.victory_dialogue.start()
            self.victory_dialogue_triggered = True
            self.stop_background_music()

    def handle_input(self, evento):
        ### NUEVO: MANEJO DE INPUT DEL DIÁLOGO DE INTRO ###
        if self.intro_dialogue.active:
            self.intro_dialogue.handle_input(evento)
            return
        ### FIN DE LA SECCIÓN NUEVA ###

        if self.is_paused:
            super().handle_input(evento)
            return
        
        if self.victory_dialogue.active:
            self.victory_dialogue.handle_input(evento)
        else:
            super().handle_input(evento)
    
    def draw(self):
        super().draw()
        
        ### NUEVO: DIBUJADO DEL DIÁLOGO DE INTRO ###
        if self.intro_dialogue.active:
            self.intro_dialogue.draw()
        ### FIN DE LA SECCIÓN NUEVA ###

        if self.victory_dialogue.active:
            self.victory_dialogue.draw()
        
        if self.boss in self.enemigos:
            self.boss_health_bar.draw()