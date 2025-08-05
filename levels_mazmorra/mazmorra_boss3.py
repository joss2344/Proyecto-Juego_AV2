#
# Contenido FINAL, COMPLETO Y CORREGIDO para el archivo: mazmorra_boss3.py
#
import pygame
import sys
from game_scene import GameScene
from constants import *
from enemy import Boss3
from ui import BossHealthBar
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
            next_scene_name="credits"
        )
        self.music_path = None
        self.name = "mazmorra_boss3"
        
        self.boss_start_x = self.map_width - 200
        self.boss_start_y = ground_y - 50
        self.boss = Boss3(self.boss_start_x, self.boss_start_y, "agis")
        self.enemigos.append(self.boss)
        self.boss_health_bar = BossHealthBar(screen, self.boss, "Agis, Heraldo del Fin")

        self.chest = FinalChest(self.boss_start_x - 270, self.boss_start_y - COFRE_HEIGHT - 50)
        
        self.intro_dialogue = DialogueBox(screen, text_lines=[
            "Así que has llegado, insecto... Justo como lo planeé.", "Has sido un instrumento obediente...",
            "Tu utilidad, sin embargo, ha llegado a su fin.", "Contempla al Heraldo del Fin y desespera."
        ], speaker_name="Agis, Heraldo del Fin")
        self.intro_dialogue.start()

        self.fake_victory_dialogue = DialogueBox(screen, text_lines=[
            "¡Increíble! ¡Lo has logrado, Guardián! ¡El Heraldo ha caído!", "El último fragmento es nuestro...",
            "...Espera. ¿Qué es esta energía?", "¡No puede ser! El fragmento... ¡No está siendo purificado, está siendo CONSUMIDO!",
            "¡CUIDADO! ¡ES UNA TRAMPA!"
        ], speaker_name="Eco Ancestral")

        self.final_dialogue = DialogueBox(screen, text_lines=[
            "Así que lo has logrado, mortal... Has reunido los fragmentos que ni yo... podía tocar.",
            "Mi castigo fue la inmortalidad... Pero tú... tú has sido mi instrumento.",
            "Ahora, con el poder de la Llave Solar, mi verdadero plan se pone en marcha.",
            "Este universo conocerá la verdadera eternidad... la del silencio.",
            "No intentes detenerme. Ya es tarde... el mundo conocerá mi verdadera forma."
        ], speaker_name="¿Anciano Sabio?")
        
        self.sound_victory_sting = self._load_sound("Soundtracks/victory_sting.mp3")
        self.sound_suspense = self._load_sound("sounds/suspense.mp3")
        self.sound_boss_revive = self._load_sound("sounds/revive.mp3")
        self.sound_betrayal = self._load_sound("Soundtracks/traicion.mp3") # --- NUEVO: Carga del audio de traición ---
        self.suspense_sound_played = False
        self.opening_music_played = False

        self.game_state = "INTRO_DIALOGUE"
        
        self.revival_anim_frames = self.boss.animations.get('die', [])
        self.revival_frame_index = 0
        self.last_revival_update = 0
        self.revival_anim_speed = 80
        
        pygame.mixer.music.stop()

    def respawn_player(self):
        super().respawn_player()
        pygame.mixer.music.stop()
        self.game_state = "INTRO_DIALOGUE"
        if self.boss not in self.enemigos: self.enemigos.append(self.boss)
        self.boss.is_dying = False; self.boss.is_dead = False; self.boss.action = 'idle'
        self.boss.rect.midbottom = (self.boss_start_x, self.boss_start_y)
        self.interactables = []
        self.suspense_sound_played = False
        self.opening_music_played = False
        self.intro_dialogue.start()

    def update(self):
        if self.game_state == "INTRO_DIALOGUE":
            self.intro_dialogue.update()
            self.jugador.vel_x = 0
            
            if not self.opening_music_played:
                pygame.mixer.music.load("Soundtracks/opening.mp3")
                pygame.mixer.music.play(-1)
                self.opening_music_played = True

            if self.intro_dialogue.finished:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(BOSS_3_MUSIC_PATH)
                pygame.mixer.music.play(-1)
                self.game_state = "BATTLE_PHASE_1"
                self.boss.salud = 600
                self.boss.salud_maxima = 600
            return

        elif self.game_state == "BATTLE_PHASE_1":
            super().update()
            self.boss_health_bar.update(self.boss)
            if self.boss.salud <= 0:
                pygame.mixer.music.stop()
                self.game_state = "BOSS_DYING_PHASE_1"
            return

        elif self.game_state == "BOSS_DYING_PHASE_1":
            super().update()
            self.jugador.vel_x = 0

            if not self.enemigos:
                if self.sound_victory_sting: self.sound_victory_sting.play()
                self.fake_victory_dialogue.start()
                self.game_state = "FAKE_VICTORY_DIALOGUE"
            return

        elif self.game_state == "FAKE_VICTORY_DIALOGUE":
            self.jugador.vel_x = 0
            self.fake_victory_dialogue.update()
            if self.fake_victory_dialogue.current_line_index == 3 and not self.suspense_sound_played:
                if self.sound_victory_sting: self.sound_victory_sting.stop()
                if self.sound_suspense: self.sound_suspense.play(-1)
                self.suspense_sound_played = True

            if self.fake_victory_dialogue.finished:
                if self.sound_suspense: self.sound_suspense.stop()
                if self.sound_boss_revive: self.sound_boss_revive.play()
                self.game_state = "REVIVAL_ANIMATION"
                self.trigger_shake(120, 8)
                self.revival_frame_index = len(self.revival_anim_frames) - 1 if self.revival_anim_frames else 0
                self.last_revival_update = pygame.time.get_ticks()
            return
            
        elif self.game_state == "REVIVAL_ANIMATION":
            self.jugador.vel_x = 0
            now = pygame.time.get_ticks()
            if now - self.last_revival_update > self.revival_anim_speed:
                self.last_revival_update = now
                self.revival_frame_index -= 1
                if self.revival_frame_index < 0:
                    pygame.mixer.music.load(BOSS_3_MUSIC_PATH)
                    pygame.mixer.music.play(-1, fade_ms=1000)
                    self.game_state = "BATTLE_PHASE_2"
                    self.enemigos.append(self.boss)
                    self.boss.salud = 2000
                    self.boss.salud_maxima = 2000
                    self.boss.action = 'idle'
                    self.boss.is_dying = False
                    self.boss.is_dead = False
                    self.boss_health_bar.boss_name = "Agis, DIOS de la Falsa Trinidad"
            return

        elif self.game_state == "BATTLE_PHASE_2":
            super().update()
            self.boss_health_bar.update(self.boss)
            if self.boss.salud <= 0:
                pygame.mixer.music.stop()
                self.game_state = "BOSS_DEAD"
            return
        
        elif self.game_state == "BOSS_DEAD":
            super().update()
            if not self.enemigos:
                self.game_state = "CHEST_APPEARS"
                self.interactables.append(self.chest)
                self.progreso_llave[2] = True
        
        elif self.game_state == "CHEST_APPEARS":
            super().update()
            if self.jugador.rect.colliderect(self.chest.rect.inflate(40, 40)):
                # --- NUEVO: Se reproduce la música de traición al iniciar el diálogo final ---
                if self.sound_betrayal:
                    pygame.mixer.music.load("Soundtracks/traicion.mp3")
                    pygame.mixer.music.play(-1)
                self.final_dialogue.start()
                self.game_state = "FINAL_DIALOGUE" 

        elif self.game_state == "FINAL_DIALOGUE":
            self.final_dialogue.update()
            if self.final_dialogue.finished:
                self.game_state = "CREDITS"
                self.running = False

    def handle_input(self, evento):
        if self.intro_dialogue.active: self.intro_dialogue.handle_input(evento)
        elif self.fake_victory_dialogue.active: self.fake_victory_dialogue.handle_input(evento)
        elif self.final_dialogue.active: self.final_dialogue.handle_input(evento)
        else: super().handle_input(evento)

    def draw(self):
        super().draw()
        
        if self.boss in self.enemigos:
            self.boss.draw_telegraphs(self.screen, self.offset_x, self.offset_y, self.zoom)

        if self.game_state in ["BATTLE_PHASE_1", "BATTLE_PHASE_2"]:
             if self.boss in self.enemigos: self.boss_health_bar.draw()
        
        if self.game_state == "REVIVAL_ANIMATION":
            if self.revival_frame_index >= 0 and self.revival_anim_frames:
                revival_image = self.revival_anim_frames[self.revival_frame_index]
                img_rect = revival_image.get_rect(center=self.boss.rect.center)
                render_pos_x = (img_rect.x - self.offset_x) * self.zoom
                render_pos_y = (img_rect.y - self.offset_y) * self.zoom
                self.screen.blit(revival_image, (render_pos_x, render_pos_y))
        
        if self.intro_dialogue.active: self.intro_dialogue.draw()
        elif self.fake_victory_dialogue.active: self.fake_victory_dialogue.draw()
        elif self.final_dialogue.active: self.final_dialogue.draw()
