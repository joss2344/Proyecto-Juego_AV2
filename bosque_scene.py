
import pygame
import sys
from game_scene import GameScene
from constants import *
from interactables import *
from dialogue import DialogueBox

class BosqueScene(GameScene):
    def __init__(self, screen):
        self.map_width = 2500
        self.map_height = 830
        
        ground_y = 780
        bosque_platforms = [
            pygame.Rect(0, ground_y, self.map_width, 50),
        ]
        
        bosque_checkpoints = []
        bosque_interactables = []

        player_start = (100, ground_y - PLAYER_HEIGHT+10)
        
        bosque_enemies = [
            (600, ground_y-50, 0, "lobo"),
            (1100, ground_y-50, 600, "lobo"),
            (900, ground_y-50, 600, "lobo"),
        ]

        super().__init__(
            screen, MAP_BOSQUE_PATH, bosque_platforms, 
            bosque_checkpoints,
            bosque_interactables,
            player_start, 
            bosque_enemies, 
            self.map_width, 
            self.map_height, 
            next_scene_name="aldea"
        )
        
        self.name = "bosque"

        self.music_path = "Soundtracks/soundtrack1.mp3"

        self.intro_dialogue = DialogueBox(
            screen,
            text_lines=[
                "El silencio se acerca... y tú eres el único eco que responde.",
                "Una herida sangra en el tejido de la existencia: el Clan Umbral, devoradores de realidades.",
                "No fuiste 'elegido'... fuiste la única chispa de voluntad que se negó a extinguirse en este crepúsculo.",
                "Sobre tus hombros no descansa un reino, sino el destino de toda memoria. Si tu luz cae, todo se desvanecerá en la nada.",
                "La corrupción ya ha manchado este bosque. ¡Mira adelante!",
                "¡Ahí! Una de sus viles criaturas. ¡Demuestra que la existencia aún merece luchar! ¡Atácalo con tus habilidades!"
            ],
            speaker_name="Eco de la Creación"
        )
        self.intro_dialogue.start()
        
        self.dialogo_terminado = False

    def run(self, selected_character_for_this_scene=None):
        if selected_character_for_this_scene:
            self.jugador.cambiar_personaje(selected_character_for_this_scene)

        try:
            pygame.mixer.music.load("Soundtracks/misteriosa.mp3")
            pygame.mixer.music.play(-1)
            GameScene._current_music_path = "Soundtracks/misteriosa.mp3"
        except pygame.error as e:
            print(f"No se pudo cargar 'Soundtracks/misteriosa.mp3': {e}")

            self.play_background_music()

        self.cambio_escena_activo = False
        
        while self.running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                self.handle_input(evento)
            
            if not self.is_paused:
                self.update()
                
            self.draw()
            pygame.display.flip()
            self.reloj.tick(60)
            
        return self.next_scene_name, self.jugador.personaje



    def update(self):
        if self.intro_dialogue.active:
            self.intro_dialogue.update()
            self.jugador.vel_x = 0
            self.jugador.vel_y = 0
            return

        # Esta condición se cumplirá UNA SOLA VEZ, justo después de que el diálogo termine.
        if not self.dialogo_terminado:
            self.dialogo_terminado = True
            print("Diálogo finalizado. Iniciando soundtrack principal.")
            # Llama a la función de la clase base para reproducir la música principal de la escena.
            self.play_background_music()

        super().update()

  
    def handle_input(self, evento):
        if self.intro_dialogue.active:
            self.intro_dialogue.handle_input(evento)
        else:
            super().handle_input(evento)

    def draw(self):
        super().draw()
        
        if self.intro_dialogue.active:
            self.intro_dialogue.draw()