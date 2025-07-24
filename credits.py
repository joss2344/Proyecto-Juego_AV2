import pygame
import sys
from constants import *

class CreditsScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Cargar la imagen de fondo
        try:
            self.background = pygame.transform.scale(pygame.image.load("fondos/credits.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)
            
        self.font_continuara = FONT_LARGE
        self.font_credits = FONT_MEDIUM
        
        # Texto a mostrar
        self.continuara_surf = self.font_continuara.render("Continuará...", True, WHITE)
        self.continuara_rect = self.continuara_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        
        self.credits_list = [
            "Un Juego De:",
            "Jose Rodriguez",
            "Gustavo Reyes",
            "Cristian",
            "",
            "Agradecimientos Especiales:",
            "Gemini",
            "Copilot",
            "Itch.io",
            "",
            "¡Gracias por Jugar!"
        ]
        
        # Posición inicial de los créditos (debajo de la pantalla)
        self.credits_y = SCREEN_HEIGHT + 50
        self.scroll_speed = 1.5
        self.running = True

    def run(self):
        # Poner la música del final
        try:
            pygame.mixer.music.load(ENDING_MUSIC_PATH)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print(f"No se pudo cargar la música de créditos: {ENDING_MUSIC_PATH}")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):
                    self.running = False # Salir de los créditos

            # Mover los créditos hacia arriba
            self.credits_y -= self.scroll_speed
            
            # Dibujar todo
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.continuara_surf, self.continuara_rect)
            
            # Dibujar cada línea de los créditos
            for i, line in enumerate(self.credits_list):
                text_surf = self.font_credits.render(line, True, WHITE)
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, self.credits_y + i * 50))
                self.screen.blit(text_surf, text_rect)

            # Si los créditos ya salieron de la pantalla, terminar
            if self.credits_y < -len(self.credits_list) * 50:
                self.running = False

            pygame.display.flip()
            self.clock.tick(60)
            
        return None, None # No devuelve ninguna escena siguiente