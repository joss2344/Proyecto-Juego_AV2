import pygame
from constants import *
import pygame
import os # <-- AÑADE ESTA LÍNEA
from constants import *
from game_state import get_saved_games, save_game
from game_state import get_saved_games, save_game

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = FONT_LARGE
        self.opciones = ["Continuar", "Guardar Partida", "Salir al Menú"] #
        self.botones_rect = [] #
        y_inicial = SCREEN_HEIGHT // 2 - 80 #
        for i, opcion in enumerate(self.opciones): #
            texto_surf = self.font.render(opcion, True, WHITE) #
            texto_rect = texto_surf.get_rect(center=(SCREEN_WIDTH // 2, y_inicial + i * 80)) #
            self.botones_rect.append(texto_rect) #
        
        # ---  ATRIBUTOS PARA EL INPUT DE GUARDADO ---
        self.saving_state = False 
        self.save_name_input = "" 
        self.input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50, 400, 50) #
        self.input_active = False 
        self.font_small = FONT_SMALL 

    def handle_event(self, event, can_save, game_data_to_save): 
        if self.saving_state: #
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN: 
                    if self.save_name_input.strip(): 
                        # Llamar a la función de guardado con el nombre personalizado
                        save_game(game_data_to_save, self.save_name_input.strip()) 
                        self.saving_state = False 
                        self.save_name_input = "" 
                        self.input_active = False 
                        return "Guardado Exitoso" 
                    else:
                        print("El nombre de la partida no puede estar vacío.") 
                elif event.key == pygame.K_BACKSPACE: 
                    self.save_name_input = self.save_name_input[:-1] #
                elif event.key == pygame.K_ESCAPE: 
                    self.saving_state = False 
                    self.save_name_input = "" 
                    self.input_active = False 
                else:
                    self.save_name_input += event.unicode 
            return None 
        else:
            if event.type == pygame.MOUSEBUTTONDOWN: 
                for i, rect in enumerate(self.botones_rect): 
                    if rect.collidepoint(event.pos): 
                        if self.opciones[i] == "Guardar Partida": 
                            if can_save: 
                                self.saving_state = True 
                                self.input_active = True 
                                return None 
                            else:
                                return None
                        return self.opciones[i] 
            return None 

    def draw(self, can_save):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) #
        overlay.fill((0, 0, 0, 150)) 
        self.screen.blit(overlay, (0, 0)) 
        mouse_pos = pygame.mouse.get_pos() 

        if self.saving_state: #
            # Dibujar el cuadro de entrada de texto
            prompt_text = self.font_small.render("Introduce un nombre para la partida:", True, WHITE) #
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)) #
            self.screen.blit(prompt_text, prompt_rect) #

            pygame.draw.rect(self.screen, WHITE, self.input_rect, 2) 
            if self.input_active: #
                pygame.draw.rect(self.screen, LIGHT_GREY, self.input_rect) 
            else:
                pygame.draw.rect(self.screen, DARK_GREY, self.input_rect) 
            
            text_surface = self.font_small.render(self.save_name_input, True, WHITE) #
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 10)) #
            
            # Dibujar el cursor parpadeante
            if self.input_active and pygame.time.get_ticks() % 1000 < 500: #
                cursor_pos_x = self.input_rect.x + 5 + text_surface.get_width() 
                pygame.draw.line(self.screen, WHITE, (cursor_pos_x, self.input_rect.y + 10), (cursor_pos_x, self.input_rect.y + self.input_rect.height - 10), 2) 
        else:
            for i, opcion in enumerate(self.opciones): 
                rect = self.botones_rect[i] #
                color = MAGIC_BLUE if rect.collidepoint(mouse_pos) else WHITE 
                if opcion == "Guardar Partida" and not can_save: 
                    color = (100, 100, 100) 
                
                texto_surf = self.font.render(opcion, True, color) 
                self.screen.blit(texto_surf, rect) 

class DeathScreenQuote:
    def __init__(self, screen, quote, author):
        self.screen = screen 
        self.font_quote = FONT_MEDIUM 
        self.font_author = FONT_SMALL 
        self.quote_surf = self.font_quote.render(f'"{quote}"', True, (180, 180, 180)) #
        self.author_surf = self.font_author.render(f"- {author}", True, (150, 150, 150)) #
        self.quote_rect = self.quote_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) #
        self.author_rect = self.author_surf.get_rect(center=(SCREEN_WIDTH / 2, self.quote_rect.bottom + 30)) #

    def draw(self):
        self.screen.fill(BLACK) 
        self.screen.blit(self.quote_surf, self.quote_rect) #
        self.screen.blit(self.author_surf, self.author_rect) #

class LoadGameScreen:
    def __init__(self, screen):
        self.screen = screen #
        self.font_title = FONT_LARGE #
        self.font_item = FONT_MEDIUM #
        self.saved_games_files = get_saved_games() 
        self.opciones_ui = [] 
        
        self.scroll_y = 0 
        self.item_height = 60 #
        self.visible_items_count = 6 
        self.display_area_start_y = 150 
        self.display_area_height = self.item_height * self.visible_items_count 
        
        self._prepare_options() 

    def _prepare_options(self):
        self.opciones_ui = [] 
        for game_file in self.saved_games_files: 
            try:
                # Intentar extraer el nombre personalizado o la fecha/hora
                base_name = os.path.splitext(game_file)[0] 
                if base_name.startswith("save_"): #
                    # Si es un guardado automático, formatea la fecha y hora
                    raw_datetime = base_name.replace("save_", "") 
                    date_part, time_part = raw_datetime.split('_') 
                    formatted_time = time_part.replace("-", ":") 
                    display_text = f"Guardado {date_part} {formatted_time}" 
                else:
                    display_text = base_name #
            except ValueError:
                display_text = game_file 
            
            # El rect se calculará en draw() para aplicar el scroll
            self.opciones_ui.append({"file": game_file, "text": display_text}) #
            
        self.total_content_height = len(self.opciones_ui) * self.item_height #
        self.max_scroll = max(0, self.total_content_height - self.display_area_height) #

    def run(self):
        import sys
        running = True 
        while running: 
            self.screen.fill(DARK_GREY) 
            mouse_pos = pygame.mouse.get_pos() 

            titulo_surf = self.font_title.render("Cargar Partida", True, WHITE) 
            self.screen.blit(titulo_surf, titulo_surf.get_rect(center=(SCREEN_WIDTH / 2, 80))) 

            # Dibujar las opciones de guardado
            for i, opcion_data in enumerate(self.opciones_ui): #
                item_y = self.display_area_start_y + i * self.item_height - self.scroll_y #
                
                # Solo dibuja si está dentro del área visible
                if item_y + self.item_height > self.display_area_start_y and \
                   item_y < self.display_area_start_y + self.display_area_height: #
                    
                    # Crear un rect temporal para la colisión del mouse
                    temp_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, item_y, 500, self.item_height) #
                    
                    color = MAGIC_BLUE if temp_rect.collidepoint(mouse_pos) else WHITE #
                    texto_surf = self.font_item.render(opcion_data["text"], True, color) #
                    # Elblit usa la posición absoluta
                    self.screen.blit(texto_surf, texto_surf.get_rect(center=(SCREEN_WIDTH // 2, item_y + self.item_height // 2))) #

            # Dibujar scrollbar si es necesario
            if self.max_scroll > 0: 
                scrollbar_x = SCREEN_WIDTH - 50 # Posición X de la barra
                scrollbar_y = self.display_area_start_y 
                scrollbar_height = self.display_area_height 
                scrollbar_width = 10 
                
                # Fondo de la barra
                pygame.draw.rect(self.screen, (100, 100, 100), (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height), border_radius=5) 
                
                # El "pulgar" de la barra de desplazamiento
                thumb_height = (self.display_area_height / self.total_content_height) * self.display_area_height 
                thumb_y = scrollbar_y + (self.scroll_y / self.max_scroll) * (scrollbar_height - thumb_height) 
                pygame.draw.rect(self.screen, (200, 200, 200), (scrollbar_x, thumb_y, scrollbar_width, thumb_height), border_radius=5) 


            for evento in pygame.event.get(): 
                if evento.type == pygame.QUIT: 
                    pygame.quit() 
                    sys.exit() 
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: 
                    return None 
                
                # Manejar scroll con la rueda del ratón
                if evento.type == pygame.MOUSEBUTTONDOWN: 
                    if evento.button == 4: # Scroll up
                        self.scroll_y = max(0, self.scroll_y - self.item_height) #
                    elif evento.button == 5: # Scroll down
                        self.scroll_y = min(self.max_scroll, self.scroll_y + self.item_height) 
                    
                    # Manejar clics en las opciones
                    if evento.button == 1: # Botón izquierdo del ratón
                        mouse_x, mouse_y = evento.pos 
                        
                        # Verificar si el clic fue dentro del área de visualización
                        if mouse_y > self.display_area_start_y and \
                           mouse_y < self.display_area_start_y + self.display_area_height: #
                            
                            clicked_item_index = (mouse_y - self.display_area_start_y + self.scroll_y) // self.item_height #
                            if 0 <= clicked_item_index < len(self.opciones_ui): 
                                # Re-crear el rect para verificar el clic preciso
                                item_y_on_screen = self.display_area_start_y + clicked_item_index * self.item_height - self.scroll_y #
                                clickable_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, item_y_on_screen, 500, self.item_height) #
                                if clickable_rect.collidepoint(mouse_x, mouse_y): 
                                    return self.opciones_ui[clicked_item_index]["file"] 

            pygame.display.flip() 
# --- CLASE AÑADIDA PARA LA BARRA DE VIDA DEL JEFE ---
class BossHealthBar:
    def __init__(self, screen, boss, boss_name):
        self.screen = screen 
        self.boss = boss 
        self.boss_name = boss_name 
        self.width = SCREEN_WIDTH * 0.6 
        self.height = 25 
        self.x = (SCREEN_WIDTH - self.width) // 2 
        self.y = 40 
        self.font = FONT_SMALL 

    def update(self, boss):
        self.boss = boss 

    def draw(self):
        if self.boss.salud <= 0: 
            return 
            
        bg_rect = pygame.Rect(self.x - 4, self.y - 4, self.width + 8, self.height + 8) 
        pygame.draw.rect(self.screen, (0,0,0,150), bg_rect, border_radius=5) 
        
        health_percentage = max(0, self.boss.salud / self.boss.salud_maxima) 
        health_width = int(self.width * health_percentage) 
        
        pygame.draw.rect(self.screen, (180, 0, 0), (self.x, self.y, self.width, self.height)) 
        if health_width > 0: #
            pygame.draw.rect(self.screen, GREEN_HEALTH, (self.x, self.y, health_width, self.height)) 
        
        pygame.draw.rect(self.screen, WHITE, (self.x, self.y, self.width, self.height), 2, border_radius=5) 
        
        text_surface = self.font.render(self.boss_name, True, WHITE) 
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, self.y - 15)) 
        self.screen.blit(text_surface, text_rect) 

class CreditsScreen:
    def __init__(self, screen):
        self.screen = screen 
        self.font_title = FONT_LARGE 
        self.font_credits = FONT_MEDIUM 
        self.credits_list = [
            # --- Introducción ---
            "ELEMENTAL TRINITY",
            "",
            "Una Aventura Épica Creada Por:",
            "",

            # --- Equipo Principal ---
            "Mentes Maestras del Pixel:",
            "  Jose Rodriguez",
            "  Gustavo Reyes",
            "  Cristian",
            "",

            # --- Agradecimientos Especiales ---
            "Inspiracion Divina y Apoyo Indispensable:",
            "  Gemini",
            "  Copilot",
            "  Itch.io",
            "  Multicable",
            "  Xiomara Castro",
            "  Mel Zelaya",
            "  Mi Mama",
            "  Neron",
            "  El Vecino",
            "",

            # --- Contribuciones Invisibles (y con humor) ---
            "Fuerza Bruta y Cafeina Ilimitada:",
            "  Los que sacrificaron sus horas de sueno",
            "  La Cafeteria de la esquina",
            "  El internet hondureno",
            "  Los generadores electricos",
            "",

            # --- Elenco de Pesadilla (Enemigos) ---
            "Los Titanes que te Desafiaron:",
            "  El Lobo",
            "  El Depredador",
            "  El Mago Azul",
            "  Los Jades",
            "  Y todos los demas secuaces",
            "",

            # --- Banda Sonora y Atmosfera ---
            "Sinfonia del Mazmorreo:",
            "  Musicos y creadores de efectos sonoros",
            "  El sonido de las chicharras en verano",
            "",

            # --- Agradecimiento Final ---
            "Un Agradecimiento Gigante a TI:",
            "  ¡Gracias por Jugar a Elemental Trinity!",
            "  ¡Esperamos que hayas disfrutado la aventura!",
            "",
            "FIN DEL JUEGO"
        ]
        self.alpha = 0 #
        self.state = "FADE_IN_CONTINUARA" 
        self.continuara_surf = self.font_title.render("Continuará...", True, WHITE) #
        self.continuara_rect = self.continuara_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) #
        self.credits_y = SCREEN_HEIGHT + 50 
        self.credits_speed = 1.5 

    def run(self):
        clock = pygame.time.Clock() 
        running = True #
        while running: #
            self.screen.fill(BLACK) #
            
            if self.state == "FADE_IN_CONTINUARA": #
                self.alpha += 2 #
                if self.alpha >= 255: #
                    self.alpha = 255 #
                    self.state = "SHOW_CONTINUARA" #
                    pygame.time.wait(2000) # Espera 2 segundos
                self.continuara_surf.set_alpha(self.alpha) #
                self.screen.blit(self.continuara_surf, self.continuara_rect) #

            elif self.state == "SHOW_CONTINUARA": #
                self.state = "FADE_OUT_CONTINUARA" #
            
            elif self.state == "FADE_OUT_CONTINUARA": #
                self.alpha -= 2 #
                if self.alpha <= 0: #
                    self.alpha = 0 #
                    self.state = "CREDITS_ROLL" #
                    pygame.time.wait(1000) #
                self.continuara_surf.set_alpha(self.alpha) #
                self.screen.blit(self.continuara_surf, self.continuara_rect) #

            elif self.state == "CREDITS_ROLL": #
                self.credits_y -= self.credits_speed #
                y = self.credits_y #
                for i, line in enumerate(self.credits_list): #
                    text_surf = self.font_credits.render(line, True, WHITE) #
                    text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, y + i * 50)) #
                    self.screen.blit(text_surf, text_rect) #
                if y < -len(self.credits_list) * 50: #
                    running = False # Terminan los créditos

            for event in pygame.event.get(): #
                if event.type == pygame.QUIT: #
                    running = False #
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #
                    running = False # Permite saltar los créditos

            pygame.display.flip() #
            clock.tick(60) #