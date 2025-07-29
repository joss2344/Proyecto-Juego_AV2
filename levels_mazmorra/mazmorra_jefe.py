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
        
        ground_y = 900 # <-- Altura del suelo
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
        
        # --- CREACIÓN DEL JEFE CORREGIDA ---
        boss_start_x = self.map_width - 300
        boss_start_y = ground_y # <-- AHORA APARECE SOBRE EL SUELO
        self.boss = Boss1(boss_start_x, boss_start_y, "boss1")
        self.enemigos.append(self.boss)
        
        self.boss_name = "Entidad Oscura del Vacío"
        self.boss_health_bar = BossHealthBar(screen, self.boss, self.boss_name)
        
        self.victory_dialogue = DialogueBox(screen, text_lines=["¡Has conseguido el primer fragmento!", "Pero tu aventura apenas comienza..."], speaker_name="Eco Ancestral")
        self.victory_dialogue_triggered = False
        self.sound_fragment_collected = self._load_sound("sounds/fragmento.wav")
        
        self.music_path = BOSS_MUSIC_PATH
        self.name = "mazmorra_jefe"

    def respawn_player(self):
        # Llama a la lógica de la pantalla de muerte de la clase base
        super().respawn_player()
        
        # Si el jefe no está en la lista de enemigos (porque fue derrotado), lo vuelve a añadir
        if self.boss not in self.enemigos:
            self.enemigos.append(self.boss)
        
        # Le restaura la vida
        self.boss.salud = self.boss.salud_maxima
        # También asegúrate de resetear cualquier estado de muerte del jefe si los tiene
        self.boss.is_dying = False
        self.boss.is_dead = False
        self.boss.action = 'idle' 
        self.boss.rect.midbottom = (self.map_width - 300, 900) 

    def update(self):
        if self.victory_dialogue.active:
            self.victory_dialogue.update()
            if self.victory_dialogue.finished:
                self.running = False # Finaliza la escena para la transición
            return 
            
        super().update() # Llama al update de GameScene para lógica general

        # Actualiza la barra de vida del jefe si está presente
        if self.boss in self.enemigos:
            self.boss_health_bar.update(self.boss)
        
        # Lógica de victoria cuando el jefe es derrotado
        if not self.enemigos and not self.victory_dialogue_triggered:
            self.progreso_llave[0] = True # Marca el primer fragmento de llave como conseguido
            
  
            
            self.can_save = True # <--- ¡CAMBIO CRUCIAL! Habilita el guardado manual después de la victoria
            
            if self.sound_fragment_collected:
                self.sound_fragment_collected.play() # Reproduce sonido de fragmento
            
            self.victory_dialogue.start() # Inicia el diálogo de victoria
            self.victory_dialogue_triggered = True # Marca que el diálogo ya se activó
            self.stop_background_music() # Detiene la música del jefe

    def handle_input(self, evento):
        # Si el juego está en pausa, la clase base GameScene maneja el input
        if self.is_paused:
            super().handle_input(evento)
            return
        
        # Si el diálogo de victoria está activo, solo el diálogo maneja el input
        if self.victory_dialogue.active:
            self.victory_dialogue.handle_input(evento)
        else:
            # De lo contrario, la clase base GameScene maneja el input del jugador
            super().handle_input(evento)
    
    def draw(self):
        super().draw() # Dibuja el fondo, jugador, enemigos, etc.
        
        # Dibuja el diálogo de victoria si está activo
        if self.victory_dialogue.active:
            self.victory_dialogue.draw()
        
        # Dibuja la barra de vida del jefe si el jefe aún está en la lista de enemigos
        if self.boss in self.enemigos:
            self.boss_health_bar.draw()