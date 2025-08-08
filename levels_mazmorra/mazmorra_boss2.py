import pygame
import sys
from game_scene import GameScene
from constants import *
from enemy import Boss2
from ui import BossHealthBar
from dialogue import DialogueBox
from game_state import save_game 

class MazmorraBoss2Scene(GameScene):
    def __init__(self, screen): # Asumo que ahora recibe 'joystick'
        self.map_width = 1920
        self.map_height = 1080
        ground_y = 900
        platforms = [pygame.Rect(0, ground_y, self.map_width, 50)]
        player_start = (200, ground_y - PLAYER_HEIGHT)
        
        super().__init__(
            screen, # Pasando el joystick
            MAP_MAZMORRA_BOSS2_PATH, platforms,
            [], [], player_start, [], 
            self.map_width, self.map_height, 
            next_scene_name="mazmorra_p5" 
        )
        self.name = "mazmorra_boss2"
        self.music_path =  BOSS_2_MUSIC_PATH

        self.boss = Boss2(self.map_width - 400, ground_y, "nightborne")
        self.enemigos.append(self.boss)
        
        self.boss_health_bar = BossHealthBar(screen, self.boss, "NightBorne")
        
        self.intro_dialogue = DialogueBox(
            screen,
            text_lines=[
                "El corazón de la mazmorra late con un rencor antiguo... ¡Puedes sentirlo!",
                "He ahí el NightBorne, un caballero caído, consumido por la eternidad y guardián de este santuario oscuro.",
                "El segundo fragmento de la Llave Solar arde en su pecho, encadenado a su alma torturada.",
                "Su colosal espada es lenta, una reliquia de un tiempo olvidado. Anticipa su arco y la evasión será tu aliada.",
                "Pero no te confíes, pues un solo golpe de esa hoja maldita puede quebrar la voluntad del alma más fuerte.",
                "¡Acaba con su vigilia eterna y reclama el segundo fragmento!"
            ],
            speaker_name="Eco Ancestral"
        )
        self.intro_dialogue.start()

        self.victory_dialogue = DialogueBox(screen, text_lines=["El segundo fragmento es tuyo.", "El poder ancestral casi está completo..."], speaker_name="Eco Ancestral")
        self.victory_triggered = False
        self.sound_fragment_collected = self._load_sound("sounds/fragmento.wav")

        # La transición está bloqueada por defecto, esto está bien.
        self.transition_conditions_met = False

    def respawn_player(self):
        super().respawn_player()
        
        if self.boss not in self.enemigos:
            self.enemigos.append(self.boss)
        
        self.boss.salud = self.boss.salud_maxima
        self.boss.is_dying = False
        self.boss.is_dead = False
        self.boss.action = 'idle'
        self.boss.rect.midbottom = (self.map_width - 400, 900)

        # Re-bloqueamos la transición al reaparecer, esto está bien.
        self.transition_conditions_met = False
        self.victory_triggered = False

    def update(self):
        # Manejo de diálogos que pausan el juego
        if self.intro_dialogue.active:
            self.intro_dialogue.update()
            self.jugador.vel_x = 0
            return

        if self.victory_dialogue.active:
            self.victory_dialogue.update()
            if self.victory_dialogue.finished:
                # La transición ahora se maneja al llegar al borde del mapa,
                # por lo que no es necesario forzar el cambio de escena aquí.
                # self.running = False 
                pass
            return

        # 1. Ejecutamos la lógica de la clase base PRIMERO.
        # Esto mueve todo, pero también comete el error de poner transition_conditions_met = True
        super().update()
        
        # Actualizamos la barra de vida del jefe si está vivo
        if self.boss in self.enemigos:
            self.boss_health_bar.update(self.boss)
        
        # Verificamos si el jefe ha sido derrotado
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

        # <<<<<<< INICIO DE LA CORRECCIÓN DE EMERGENCIA >>>>>>>>
        # 2. Imponemos la regla CORRECTA al final de cada fotograma.
        # Esto anula el error de la clase base.
        if not self.victory_triggered:
            # Si la secuencia de victoria NO ha comenzado, la salida está BLOQUEADA.

            if BOSS_HEALTH>0:
                self.transition_conditions_met = False
        else:
            # Si la secuencia de victoria SÍ ha comenzado, la salida está PERMITIDA.
            self.transition_conditions_met = True
        # <<<<<<< FIN DE LA CORRECCIÓN DE EMERGENCIA >>>>>>>>

    def handle_input(self, evento):
        if self.intro_dialogue.active:
            self.intro_dialogue.handle_input(evento)
            return

        if self.victory_dialogue.active:
            self.victory_dialogue.handle_input(evento)
        else:
            super().handle_input(evento)

    def draw(self):
        super().draw()

        if self.intro_dialogue.active:
            self.intro_dialogue.draw()
            
        if self.boss in self.enemigos:
            self.boss_health_bar.draw()
            
        if self.victory_dialogue.active:
            self.victory_dialogue.draw()