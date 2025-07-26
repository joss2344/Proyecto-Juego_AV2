import pygame
import sys
from game_scene import GameScene
from constants import *
from enemy import Boss3
from ui import BossHealthBar, CreditsScreen
from dialogue import DialogueBox
from interactables import FinalChest
from game_state import save_game

class MazmorraBoss3Scene(GameScene):
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
            next_scene_name=None
        )
        self.name = "mazmorra_boss3"
        self.music_path = BOSS_MUSIC_PATH

        self.boss_start_x = self.map_width - 200
        self.boss_start_y = ground_y-60
        self.boss = Boss3(self.boss_start_x, self.boss_start_y, "agis")
        self.enemigos.append(self.boss)
        self.boss_health_bar = BossHealthBar(screen, self.boss, "Agis, Heraldo del Fin")

        self.chest = FinalChest(self.boss_start_x-270, self.boss_start_y - COFRE_HEIGHT-5 )
        
        self.dialogue_final = DialogueBox(screen, text_lines=[
            "Así que lo has logrado, mortal...",
            "Has reunido los fragmentos que ni yo, el Heraldo de la Eternidad, podía tocar durante siglos...",
            "Mi castigo fue la inmortalidad, observar sin actuar.",
            "Pero tú... tú has sido mi instrumento, y si que has actuado.",
            "Ahora, con el poder de la Llave Solar, mi plan se pone en marcha.",
            "Este universo conocerá la verdadera eternidad... la del silencio.",
            "No intentes detenerme, ya es tarde, el mundo conocera mi verdadera forma...."
        ], speaker_name="¿Anciano Sabio?")
        
        self.sound_fragment_collected = self._load_sound("sounds/fragmento.wav")
        self.game_state = "BATTLE"

    def respawn_player(self):
        super().respawn_player()
        if self.boss not in self.enemigos: self.enemigos.append(self.boss)
        self.boss.salud = self.boss.salud_maxima
        self.boss.is_dying = False; self.boss.is_dead = False
        self.boss.action = 'idle'
        self.boss.rect.midbottom = (self.boss_start_x, self.boss_start_y)
        self.interactables = []
        self.game_state = "BATTLE"

    def update(self):
        # --- MÁQUINA DE ESTADOS DE LA ESCENA FINAL (CORREGIDA) ---

        # ESTADO 4: Diálogo Final
        if self.game_state == "DIALOGUE":
            self.dialogue_final.update()
            if self.dialogue_final.finished:
                self.game_state = "CREDITS"
                self.running = False
                self.next_scene_name = "credits"
            return # Detiene todo lo demás

        # Si no estamos en el diálogo, la lógica normal del juego corre
        super().update()
        
        # ESTADO 1: Batalla
        if self.game_state == "BATTLE":
            if self.boss in self.enemigos:
                self.boss_health_bar.update(self.boss)
                if self.boss.salud <= 0:
                    self.game_state = "BOSS_DEAD"
        
        # ESTADO 2: Jefe Muerto (esperando que termine la animación de muerte)
        elif self.game_state == "BOSS_DEAD":
            if not self.enemigos: # Cuando el enemigo se elimina de la lista
                self.game_state = "CHEST_APPEARS"
                self.interactables.append(self.chest)
                self.progreso_llave[2] = True
                game_data = {"last_scene": "mazmorra_boss3", "progreso_llave": self.progreso_llave, "personaje": self.jugador.personaje, self.game_state=="BOOS_DEAD": True}
                save_game(game_data)
        
        # ESTADO 3: Cofre en Escena
        elif self.game_state == "CHEST_APPEARS":
            # Si el jugador se acerca al cofre, se activa el diálogo
            if self.jugador.rect.colliderect(self.chest.rect.inflate(40, 40)):
                if self.sound_fragment_collected: self.sound_fragment_collected.play()
                self.dialogue_final.start()
                self.game_state = "DIALOGUE" 

    def handle_input(self, evento):
        # El input solo lo maneja el diálogo si está activo
        if self.dialogue_final.active:
            self.dialogue_final.handle_input(evento)
            return
        super().handle_input(evento)

    def draw(self):
        super().draw()
        if self.boss in self.enemigos:
            self.boss_health_bar.draw()
        if self.dialogue_final.active:
            self.dialogue_final.draw()