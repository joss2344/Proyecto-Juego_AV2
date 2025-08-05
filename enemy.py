import pygame
import sys
import random
import math
from constants import *
import abilities 
import spritesheet
from abilities import NightBorneHomingOrb

class Enemigo:
    def __init__(self, x, y, patrol_range_width, enemy_info):
        self.enemy_info = enemy_info
        
        self.width = self.enemy_info.get("width", ENEMY_WIDTH)
        self.height = self.enemy_info.get("height", ENEMY_HEIGHT)
        self.scale = self.enemy_info.get("scale", 1.5)
        
        self.rect = pygame.Rect(x - (self.width / 2), y - self.height, self.width, self.height)
        
        hitbox_scale = self.enemy_info.get("hitbox_scale", (1.0, 1.0))
        hitbox_width = self.rect.width * hitbox_scale[0]
        hitbox_height = self.rect.height * hitbox_scale[1]
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        
        self.anim_data = self.enemy_info.get("anim_data")
        self.animations = {}
        self._load_animations()
        
        if 'idle' in self.animations and self.animations['idle']:
            self.action = 'idle'
            self.image = self.animations['idle'][0]
        else:
            self.action = 'static'
            if 'static' in self.animations and self.animations['static']:
                self.image = self.animations['static'][0]
            else:
                self.image = pygame.Surface((self.width, self.height)); self.image.fill(BLACK)
        
        self.frame_index = 0
        self.proyectiles = []

        self.salud = self.enemy_info.get("health", 50)
        self.salud_maxima = self.salud
        self.speed = self.enemy_info.get("speed", ENEMY_SPEED)
        self.detection_radius = self.enemy_info.get("detection_radius", DETECTION_RADIUS)
        self.attack_range = self.enemy_info.get("attack_range", 80)
        self.attack_damage = self.enemy_info.get("attack_damage", 10)
        self.attack_cooldown = self.enemy_info.get("attack_cooldown", 2000)
        self.attack_damage_frame = self.enemy_info.get("attack_damage_frame", 3)
        self.contact_damage = self.enemy_info.get("contact_damage", 0)
        self.facing_right = True
        self.is_dying = False; self.is_dead = False
        self.last_attack_time = 0
        self.damage_dealt_this_attack = False
        self.update_time = pygame.time.get_ticks()
        if not pygame.mixer.get_init(): pygame.mixer.init()
        self.death_sound = self._load_sound(self.enemy_info.get("death_sound"))

    def _load_animations(self):
        # Caso 1: Enemigo sin animaciones 
        if not self.anim_data:
            if "sprite_path" in self.enemy_info:
                path = self.enemy_info["sprite_path"]
                try:
                    img = pygame.image.load(path).convert_alpha()
                    scaled_img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                    self.animations['static'] = [scaled_img]
                except pygame.error:
                    print(f"No se pudo cargar la imagen estática: {path}")
            return 

        #Hoja de sprites compleja con varias animaciones
        if "animations" in self.anim_data:
            path = self.anim_data.get("path")
            if not path: return
            try:
                sprite_sheet_image = pygame.image.load(path).convert_alpha()
                sheet = spritesheet.SpriteSheet(sprite_sheet_image)
                for anim_name, data in self.anim_data["animations"].items():
                    temp_img_list = []
                    for i in range(data['frames']):
                        img = sheet.get_image(data['row'], i, data['width'], data['height'], self.scale, BLACK)
                        temp_img_list.append(img)
                    self.animations[anim_name] = temp_img_list
            except (pygame.error, FileNotFoundError):
                print(f"No se pudo cargar la hoja de sprites compleja: {path}")
        
        # Animaciones en archivos separados
        elif 'path' in list(self.anim_data.values())[0]:
            for anim_name, data in self.anim_data.items():
                path = data.get("path")
                if not path: continue
                try:
                    sprite_sheet_image = pygame.image.load(path).convert_alpha()
                    sheet = spritesheet.SpriteSheet(sprite_sheet_image)
                    temp_img_list = []
                    frame_width = sprite_sheet_image.get_width() // data['frames']
                    frame_height = sprite_sheet_image.get_height()
                    for i in range(data['frames']):
                        img = sheet.get_image(0, i, frame_width, frame_height, self.scale, BLACK)
                        temp_img_list.append(img)
                    self.animations[anim_name] = temp_img_list
                except (pygame.error, FileNotFoundError):
                    print(f"No se pudo cargar la hoja de sprites: {path}")

        # Lógica automática para idle/walk si no están definidos
        if 'attack' in self.animations and 'idle' not in self.animations:
            self.animations['idle'] = [self.animations['attack'][0]]
        if 'attack' in self.animations and 'walk' not in self.animations:
            self.animations['walk'] = [self.animations['attack'][0]]
    
    def _load_sound(self, path):
        if not path: return None
        try: return pygame.mixer.Sound(path)
        except pygame.error as e: print(f"No se pudo cargar el sonido '{path}': {e}"); return None

    def update_animation(self):
        if self.action == 'static' or not self.animations.get(self.action): return
        
        animation_cooldown = 120
        if self.action == 'attack':
            num_frames = len(self.animations[self.action])
            animation_cooldown = self.attack_cooldown / (num_frames + 1) if num_frames > 0 else self.attack_cooldown
        if self.action == 'die': animation_cooldown = 100
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if self.frame_index >= len(self.animations[self.action]):
            if self.action == 'die':
                self.frame_index = len(self.animations[self.action]) - 1
                self.is_dead = True
            else:
                if self.action == 'attack':
                    self.damage_dealt_this_attack = False
                self.action = 'idle'
                self.frame_index = 0
        
        self.image = self.animations[self.action][self.frame_index]

    def actualizar(self, jugador):
        if self.is_dying or self.enemy_info.get("is_boss"):
            self.update_animation()
            hitbox_offset = self.enemy_info.get("hitbox_offset", (0, 0))
            self.hitbox.centerx = self.rect.centerx + hitbox_offset[0]
            self.hitbox.centery = self.rect.centery + hitbox_offset[1]
            return

        if self.salud > 0:
            dist_x = jugador.hitbox.centerx - self.hitbox.centerx
            distancia_al_jugador = abs(dist_x)
            
            if self.action != 'attack':
                if distancia_al_jugador < self.attack_range and pygame.time.get_ticks() > self.last_attack_time + self.attack_cooldown:
                    self.vel_x = 0; self.action = 'attack'; self.frame_index = 0
                    self.last_attack_time = pygame.time.get_ticks()
                elif distancia_al_jugador < self.detection_radius and distancia_al_jugador > self.attack_range:
                    if dist_x > 0: self.vel_x = self.speed
                    else: self.vel_x = -self.speed
                    self.action = 'walk' if 'walk' in self.animations else 'idle'
                else:
                    self.action = 'idle'; self.vel_x = 0
            
            if self.action == 'attack':
                if self.frame_index == self.attack_damage_frame and not self.damage_dealt_this_attack:
                    if abs(jugador.hitbox.centerx - self.hitbox.centerx) < self.attack_range + 20:
                        jugador.tomar_danio(self.attack_damage)
                        self.damage_dealt_this_attack = True
        
        self.rect.x += self.vel_x
        if self.vel_x > 0: self.facing_right = True
        elif self.vel_x < 0: self.facing_right = False

        hitbox_offset = self.enemy_info.get("hitbox_offset", (0, 0))
        self.hitbox.centerx = self.rect.centerx + hitbox_offset[0]
        self.hitbox.centery = self.rect.centery + hitbox_offset[1]
        
        self.update_animation()

    def tomar_danio(self, cantidad):
        if self.salud > 0:
            self.salud -= abs(cantidad)
            if self.salud <= 0:
                self.salud = 0; self.action = 'die' if 'die' in self.animations else 'idle'
                if self.action not in self.animations or not self.animations[self.action]:
                    self.is_dead = True
                self.frame_index = 0; self.is_dying = True
                if self.death_sound: self.death_sound.play()

    def dibujar(self, superficie, offset_x, offset_y, zoom):
        imagen_a_dibujar = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        image_rect = imagen_a_dibujar.get_rect(center=self.rect.center)
        render_pos_x = (image_rect.x - offset_x) * zoom
        render_pos_y = (image_rect.y - offset_y) * zoom
        
        superficie.blit(imagen_a_dibujar, (render_pos_x, render_pos_y))

        for proyectil in self.proyectiles:
            proyectil.dibujar(superficie, offset_x, offset_y, zoom)

        if not self.is_dying and not self.enemy_info.get("is_boss"):
            render_width = self.rect.width * zoom
            bar_width = render_width * 0.8; bar_height = 6 * zoom if zoom > 0.5 else 3
            health_percentage = self.salud / self.salud_maxima
            current_health_width = int(bar_width * health_percentage)
            bar_pos_x = ((self.rect.centerx - offset_x) * zoom) - (bar_width / 2)
            bar_pos_y = ((self.rect.top - offset_y) * zoom) - bar_height - (5 * zoom)
            pygame.draw.rect(superficie, (50,0,0), (bar_pos_x, bar_pos_y, bar_width, bar_height))
            if current_health_width > 0:
                pygame.draw.rect(superficie, RED_HEALTH, (bar_pos_x, bar_pos_y, current_health_width, bar_height))

        # if hasattr(self, 'hitbox'):
        #     debug_rect = pygame.Rect((self.hitbox.x - offset_x) * zoom, (self.hitbox.y - offset_y) * zoom, self.hitbox.width * zoom, self.hitbox.height * zoom)
        #     pygame.draw.rect(superficie, (255, 0, 0), debug_rect, 2)
            
            
class FlyingEnemy(Enemigo):
    def actualizar(self, jugador):
        for p in self.proyectiles[:]:
            p.actualizar()
            if not p.activo:
                self.proyectiles.remove(p)

        if self.is_dying:
            self.update_animation()
            hitbox_offset = self.enemy_info.get("hitbox_offset", (0, 0))
            self.hitbox.centerx = self.rect.centerx + hitbox_offset[0]
            self.hitbox.centery = self.rect.centery + hitbox_offset[1]
            return

        if self.salud > 0:
            dist_x = jugador.hitbox.centerx - self.hitbox.centerx
            dist_y = jugador.hitbox.centery - self.hitbox.centery
            distancia_total = math.hypot(dist_x, dist_y)

            if distancia_total < self.detection_radius and distancia_total > self.attack_range:
                self.vel_x = (dist_x / distancia_total) * self.speed
                self.vel_y = (dist_y / distancia_total) * self.speed
            else:
                self.vel_x = 0
                self.vel_y = 0

            if distancia_total < self.attack_range and pygame.time.get_ticks() > self.last_attack_time + self.attack_cooldown:
                self.action = 'attack' if 'attack' in self.animations else 'idle'
                self.frame_index = 0
                self.last_attack_time = pygame.time.get_ticks()
                
                if self.enemy_info.get("is_ranged"):
                    nuevo_proyectil = abilities.WizzardBlueProjectile(
                        self.hitbox.centerx, self.hitbox.centery,
                        jugador.hitbox.centerx, jugador.hitbox.centery
                    )
                    self.proyectiles.append(nuevo_proyectil)

            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            
            hitbox_offset = self.enemy_info.get("hitbox_offset", (0, 0))
            self.hitbox.centerx = self.rect.centerx + hitbox_offset[0]
            self.hitbox.centery = self.rect.centery + hitbox_offset[1]

            if self.vel_x > 0: self.facing_right = True
            elif self.vel_x < 0: self.facing_right = False
            self.update_animation()

class Boss1(Enemigo):
    def __init__(self, x, y, enemy_name):
        enemy_info = ENEMY_INFO.get(enemy_name)
        if not enemy_info:
            print(f"ERROR: No se encontró la información para el jefe '{enemy_name}'")
            sys.exit()
        super().__init__(x, y, 0, enemy_info)
        self.attack_cooldown = 1600
        self.last_attack_time = pygame.time.get_ticks()
        self.ataques_disponibles = ["diagonal", "suelo", "multiple"]

    def actualizar(self, jugador):
        if jugador.rect.centerx < self.rect.centerx: self.facing_right = False
        elif jugador.rect.centerx > self.rect.centerx: self.facing_right = True
        
        for proyectil in self.proyectiles:
            proyectil.actualizar(0)
            if not proyectil.activo: self.proyectiles.remove(proyectil)
        
        hitbox_offset = self.enemy_info.get("hitbox_offset", (0, 0))
        self.hitbox.centerx = self.rect.centerx + hitbox_offset[0]
        self.hitbox.centery = self.rect.centery + hitbox_offset[1]

        ahora = pygame.time.get_ticks()
        if ahora - self.last_attack_time > self.attack_cooldown:
            self.atacar(jugador); self.last_attack_time = ahora


    def atacar(self, jugador):
        ataque_elegido = random.choice(self.ataques_disponibles)
        
        # Definimos puntos de origen fijos para los ataques
        origen_mano = (self.rect.centerx - 40, self.rect.centery - 50)
        origen_suelo = self.rect.midbottom

        if ataque_elegido == "diagonal":
            # El ataque diagonal siempre sale de la mano
            nuevo_proyectil = abilities.BossDiagonalProjectile(origen_mano[0], origen_mano[1], jugador.rect.centerx, jugador.rect.centery)
            self.proyectiles.append(nuevo_proyectil)

        elif ataque_elegido == "suelo":
            direccion = 1 if jugador.rect.centerx > self.rect.centerx else -1
            # El ataque bajo siempre sale de los pies
            nuevo_proyectil = abilities.BossGroundProjectile(origen_suelo[0], origen_suelo[1], direccion)
            self.proyectiles.append(nuevo_proyectil)

        elif ataque_elegido == "multiple":
            # El ataque múltiple también sale de la mano
            for i in range(-2, 3):
                offset_x = i * 40
                nuevo_proyectil = abilities.BossDiagonalProjectile(origen_mano[0], origen_mano[1], jugador.rect.centerx + offset_x, jugador.rect.centery - 50)
                self.proyectiles.append(nuevo_proyectil)

class Boss2(Enemigo):
    def __init__(self, x, y, enemy_name):
        enemy_info = ENEMY_INFO.get(enemy_name)
        if not enemy_info:
            print(f"ERROR: No se encontró la información para el jefe '{enemy_name}' en constants.py")
            sys.exit()
        super().__init__(x, y, 0, enemy_info)
        
        self.attack_cooldown = 1800 
        self.last_attack_time = pygame.time.get_ticks()

    def actualizar(self, jugador):
        self.proyectiles = []

        if self.is_dying:
            self.update_animation()
            return
        
        if self.salud > 0:
            dist_x = jugador.hitbox.centerx - self.hitbox.centerx
            distancia_al_jugador = abs(dist_x)
            
            # ---  LÓGICA DE IA: PERSEGUIR Y ATACAR ---
            if self.action != 'attack':
                # 1. Atacar si está en rango
                if distancia_al_jugador < self.attack_range and pygame.time.get_ticks() > self.last_attack_time + self.attack_cooldown:
                    self.atacar(jugador)
                
                # 2. Perseguir si ve al jugador pero no está en rango de ataque
                elif distancia_al_jugador < self.detection_radius and distancia_al_jugador > self.attack_range:
                    self.action = 'walk'
                    if dist_x > 0: # Si el jugador está a la derecha
                        self.vel_x = self.speed
                        self.facing_right = True
                    else: # Si el jugador está a la izquierda
                        self.vel_x = -self.speed
                        self.facing_right = False
                
                # 3. Quedarse quieto si el jugador está muy lejos
                else:
                    self.action = 'idle'
                    self.vel_x = 0
            
            # Lógica para aplicar daño durante la animación de ataque
            if self.action == 'attack':
                self.vel_x = 0 # No se mueve mientras ataca
                if self.frame_index == self.attack_damage_frame and not self.damage_dealt_this_attack:
                    # Comprueba si el jugador sigue cerca al momento del golpe
                    if abs(jugador.hitbox.centerx - self.hitbox.centerx) < self.attack_range + 50:
                        jugador.tomar_danio(self.attack_damage)
                        self.damage_dealt_this_attack = True

        # Aplicar movimiento a la caja de físicas
        self.rect.x += self.vel_x

        # Sincronizar hitbox y animación
        hitbox_offset = self.enemy_info.get("hitbox_offset", (0, 0))
        self.hitbox.centerx = self.rect.centerx + hitbox_offset[0]
        self.hitbox.centery = self.rect.centery + hitbox_offset[1]
        self.update_animation()

    def atacar(self, jugador):

        self.action = 'attack'
        self.frame_index = 0
        self.last_attack_time = pygame.time.get_ticks()

class Boss3(Enemigo):
    def __init__(self, x, y, enemy_name):
        enemy_info = ENEMY_INFO.get(enemy_name)
        if not enemy_info:
            print(f"ERROR: No se encontró la info para el jefe '{enemy_name}'")
            sys.exit()
        super().__init__(x, y, 0, enemy_info)
        
        self.attack_cooldown = 2500
        self.last_attack_time = pygame.time.get_ticks()
        self.ataques_disponibles = ["falling_sky", "diagonal_burst", "ground_wave"]

        ### ---  ATRIBUTOS PARA EL INDICADOR DE ATAQUE (TELEGRAPH) --- ###
        self.is_telegraphing = False         # Para saber si el jefe está "avisando" un ataque
        self.telegraph_positions = []        # Lista para guardar dónde caerán los ataques
        self.telegraph_end_time = 0          # Cuándo termina el aviso y comienza el ataque
        self.telegraph_alpha = 0             # Transparencia del indicador para el efecto de parpadeo
        self.telegraph_fade_in = True        # Para controlar si el parpadeo se aclara u oscurece

    def actualizar(self, jugador):
        self.vel_x = 0 # Es un jefe estacionario


        if self.is_telegraphing:
            # 1. Lógica del parpadeo del indicador visual
            fade_speed = 15 # Velocidad del parpadeo
            if self.telegraph_fade_in:
                self.telegraph_alpha = min(200, self.telegraph_alpha + fade_speed)
                if self.telegraph_alpha == 200: self.telegraph_fade_in = False
            else:
                self.telegraph_alpha = max(50, self.telegraph_alpha - fade_speed)
                if self.telegraph_alpha == 50: self.telegraph_fade_in = True

            # 2. Comprueba si el tiempo de aviso ha terminado para lanzar el ataque
            if pygame.time.get_ticks() >= self.telegraph_end_time:
                for pos in self.telegraph_positions:
                    # Crea los proyectiles en las posiciones previamente guardadas
                    proyectil = abilities.AgisFallingProjectile(pos[0], pos[1])
                    self.proyectiles.append(proyectil)
                
                # 3. Resetea el estado para que el jefe pueda volver a atacar
                self.is_telegraphing = False
                self.telegraph_positions = []
            
            # Detiene el resto de la lógica para que el jefe no haga nada más mientras avisa
            return

        # Actualiza proyectiles existentes
        for p in self.proyectiles[:]:
            p.actualizar(jugador.rect.x)
            if not p.activo: self.proyectiles.remove(p)

        # Comprueba si es tiempo de atacar
        ahora = pygame.time.get_ticks()
        if ahora - self.last_attack_time > self.attack_cooldown and self.action == 'idle' and not self.is_telegraphing:
            self.atacar(jugador)
            self.last_attack_time = ahora
        
        # Sincroniza hitbox y animación
        hitbox_offset = self.enemy_info.get("hitbox_offset", (0, 0))
        self.hitbox.centerx = self.rect.centerx + hitbox_offset[0]
        self.hitbox.centery = self.rect.centery + hitbox_offset[1]
        self.update_animation()

    def atacar(self, jugador):
        ataque_elegido = random.choice(self.ataques_disponibles)
        
        if ataque_elegido == "falling_sky":

            self.is_telegraphing = True
            self.telegraph_positions = []

            for i in range(5):
                offset = random.randint(-150, 150)
                self.telegraph_positions.append((jugador.hitbox.centerx + offset, self.rect.bottom))
            
            # El aviso durará 1.5 segundos (1500 ms) antes de que caigan los proyectiles
            self.telegraph_end_time = pygame.time.get_ticks() + 1500 
            self.telegraph_alpha = 0
            self.telegraph_fade_in = True

        elif ataque_elegido == "diagonal_burst":
            # Lanza una ráfaga de 3 proyectiles diagonales (sin cambios)
            for i in range(3):
                proyectil = abilities.AgisDiagonalProjectile(self.hitbox.centerx, self.hitbox.centery - 50, jugador.hitbox.centerx, jugador.hitbox.centery)
                self.proyectiles.append(proyectil)

        elif ataque_elegido == "ground_wave":
            # Lanza una onda por el suelo (sin cambios)
            direccion = 1 if jugador.rect.centerx > self.rect.centerx else -1
            proyectil = abilities.AgisGroundProjectile(self.rect.midbottom[0], self.rect.midbottom[1], direccion)
            self.proyectiles.append(proyectil)


    def draw_telegraphs(self, surface, offset_x, offset_y, zoom):
        if not self.is_telegraphing:
            return

        # Dibuja una columna de luz parpadeante por cada posición guardada
        for pos in self.telegraph_positions:
            # El indicador es una columna desde el cielo hasta la altura del suelo del jefe
            telegraph_rect = pygame.Rect(pos[0] - 20, 0, 40, pos[1] + 10)
            
            # Se usa una superficie temporal para poder aplicarle la transparencia (alpha)
            s = pygame.Surface((telegraph_rect.width * zoom, telegraph_rect.height * zoom), pygame.SRCALPHA)
            s.fill((150, 0, 150, self.telegraph_alpha))
            
            surface.blit(s, ((telegraph_rect.x - offset_x) * zoom, (telegraph_rect.y - offset_y) * zoom))