import pygame
from constants import *

class InteractableObject:
    """La plantilla base para todos los objetos de puzle."""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_active = False

    def interact(self, projectile):
        """Cada puzle específico llenará esta función con su propia lógica."""
        pass

    def update(self):
        """Para puzles que tengan animaciones."""
        pass

    def draw(self, surface, offset_x, offset_y, zoom):
        """Cada puzle se dibujará a sí mismo."""
        pass

# --- Puzle de Antorcha (reacciona al fuego) ---
class Torch(InteractableObject):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 64) 
        
        # Carga sus imágenes únicas
        self.image_off = pygame.transform.scale(
            pygame.image.load("puzzles/antorcha_apagada.png").convert_alpha(), (self.rect.width, self.rect.height)
        )
        self.image_on_sheet = pygame.image.load("puzzles/antorcha_encendida.png").convert_alpha()
        
        # Lógica para la animación de la antorcha encendida
        self.animation_frames = []
        frame_height = self.image_on_sheet.get_height()
        # Asumimos que los cuadros de la antorcha son cuadrados
        frame_width = frame_height 
        num_frames = self.image_on_sheet.get_width() // frame_width
        for i in range(num_frames):
            frame = self.image_on_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.animation_frames.append(pygame.transform.scale(frame, (self.rect.width, self.rect.height)))
        
        self.current_frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 120

    def interact(self, projectile):
        if hasattr(projectile, 'tipo_elemental') and projectile.tipo_elemental == "fuego":
            if not self.is_active:
                # Aquí podrías reproducir un sonido de "fwoosh"
                pass
            self.is_active = True

    def update(self):
        # Si la antorcha está encendida, anima la llama
        if self.is_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.animation_cooldown:
                self.last_update = current_time
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)

    def draw(self, surface, offset_x, offset_y, zoom):
        pos_x = self.rect.x - offset_x
        pos_y = self.rect.y - offset_y
        
        if self.is_active:
            # Muestra el cuadro actual de la animación de la llama
            image_to_draw = self.animation_frames[self.current_frame_index]
        else:
            # Muestra la imagen de la antorcha apagada
            image_to_draw = self.image_off
            
        surface.blit(image_to_draw, (pos_x, pos_y))


# --- Puzle de Muro Rompible (reacciona a la tierra) ---
class BreakableWall(InteractableObject):
    def __init__(self, x, y):
        super().__init__(x, y, 64, 128)
        self.image = pygame.transform.scale(
            pygame.image.load("puzzles/muro_cayendo.png").convert_alpha(), (self.rect.width, self.rect.height)
        )
        self.is_active = False # 'is_active' aquí significa 'está roto'

    def interact(self, projectile):
        if hasattr(projectile, 'tipo_elemental') and projectile.tipo_elemental == "tierra":
            self.is_active = True
            # Aquí podríamos añadir un sonido de rocas rompiéndose

    def draw(self, surface, offset_x, offset_y, zoom):
        # Solo se dibuja si NO está roto
        if not self.is_active:
            surface.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

class FinalChest(InteractableObject):
    def __init__(self, x, y):
        self.sheet = pygame.image.load(COFRE_FINAL_PATH).convert_alpha()
        
        # --- LÓGICA DE CARGA DE FRAMES CORREGIDA ---
        # Asumimos que los frames del cofre son cuadrados (ancho = alto)
        self.frame_height = self.sheet.get_height()
        self.frame_width = self.frame_height 
        
        super().__init__(x, y, COFRE_WIDTH, COFRE_HEIGHT)
        
        self.sheet = pygame.image.load(COFRE_FINAL_PATH).convert_alpha()

        self.frames = []
        # Calcula el número de frames automáticamente para evitar errores
        if self.frame_width > 0:
            num_frames = self.sheet.get_width() // self.frame_width
            for i in range(num_frames):
                frame = self.sheet.subsurface((i * self.frame_width, 0, self.frame_width, self.frame_height))
                self.frames.append(frame)
        
        # Si no se cargan frames, usa un placeholder para evitar crasheos
        if not self.frames:
            placeholder = pygame.Surface((48, 48)); placeholder.fill(MAGIC_BLUE)
            self.frames.append(placeholder)
            
        self.current_frame = 0
        self.is_opening = False
        self.is_opened = False
        self.last_update = 0
        self.anim_speed = 80 # ms por frame

    def interact(self, projectile=None):
        if not self.is_opened and not self.is_opening:
            self.is_opening = True

    def update(self):
        if self.is_opening and not self.is_opened:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.anim_speed:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = len(self.frames) - 1
                    self.is_opening = False
                    self.is_opened = True

    def draw(self, surface, offset_x, offset_y, zoom):
        pos_x = self.rect.x - offset_x
        pos_y = self.rect.y - offset_y
        surface.blit(pygame.transform.scale(self.frames[self.current_frame], self.rect.size), (pos_x, pos_y))