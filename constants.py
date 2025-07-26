import pygame

pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# --- Colors --- #
WHITE = (255, 255, 255); DARK_GREY = (50, 50, 50); MAGIC_BLUE = (80, 160, 255)
RED_HEALTH = (255, 0, 0); GREEN_HEALTH = (0, 255, 0); BLACK = (0, 0, 0)
LIGHT_GREY = (180, 180, 180)

# --- Fonts --- #
FONT_LARGE = pygame.font.SysFont("arial", 38); FONT_MEDIUM = pygame.font.SysFont("arial", 30)
FONT_SMALL = pygame.font.SysFont("arial", 24)

# --- Game Physics --- #
PLAYER_SPEED = 5; ENEMY_SPEED = 2; DETECTION_RADIUS = 350
GRAVITY = 0.6; JUMP_STRENGTH = -9

# --- Player and Enemy Sizes --- #
PLAYER_WIDTH = 100; PLAYER_HEIGHT = 100
ENEMY_WIDTH = 100; ENEMY_HEIGHT = 75 
BOSS_WIDTH = 500; BOSS_HEIGHT = 500
BOSS_HEALTH = 2000
COFRE_WIDTH = 100; COFRE_HEIGHT = 100

# --- Projectile Properties --- #
ELEMENTAL_COOLDOWN = 500; SPECIAL_COOLDOWN = 2000
COFRE_FINAL_PATH = "interactables/cofre_final.png"

# --- Asset Paths --- #
MENU_BACKGROUND_PATH = "interfaz/fondo.png"
PLAYER_SPRITE_PATHS = {
    "Prota": "Characters/prota.png", "Lia": "Characters/lia.png",
    "Kael": "Characters/kael.png", "Aria": "Characters/aria.png",
    
}
PLAYER_ANIMATION_DATA = {
    "Prota": {"idle": {"frames": 4}, "run": {"frames": 4}},
    "Lia":   {"idle": {"frames": 3}, "run": {"frames": 3}},
    "Kael":  {"idle": {"frames": 3}, "run": {"frames": 3}},
    "Aria":  {"idle": {"frames": 3}, "run": {"frames": 3}}
}

SKILL_ICON_PATHS = {
    "rock": "Skills/rock.png", "sarten": "Skills/sarten.png",
    "fire": "Skills/fire_projectile.png", "ice": "Skills/ice_projectile.png",
    "mixed": "Skills/mixed_projectile.png", "root": "Skills/root.png",
    "earth_spike": "Skills/earth_spike.png", "lightning_bolt": "Skills/lightning_bolt.png",
    "storm": "Skills/storm.png", "boss_fireball": "Skills/boss_fireball.png",
    "boss_groundwave": "Skills/boss_groundwave.png", "lightning_strike": "Skills/lightning_strike.png",
    "skeleton_sword": "Skills/skeleton_sword.png",
    "hongo_proyectil": "Skills/hongo_proyectil.png",
    "boss3_proyectil": "Skills/boss3_proyectil.png",
}


## --- DICCIONARIO CENTRAL DE ENEMIGOS ---
ENEMY_INFO = {
    "lobo":       {"health": 30, "speed": 2.5, "contact_damage": 0.2, "scale": 0.3, "width": 45, "height": 30, "y_offset": 0, "hitbox_scale": (1.5, 1.5), "hitbox_offset": (0, 0), "sprite_path": "Enemies/lobos.png","detection_radius": 300, "death_sound": "sounds/lobodeath.mp3"},
    "depredator": {"health": 50, "speed": 2,   "contact_damage": 1, "scale": 0.3, "width": 45, "height": 35, "y_offset": 0, "hitbox_scale": (1.3, 1.8), "hitbox_offset": (0, 0), "sprite_path": "Enemies/depredator.png","detection_radius": 300, "death_sound": "sounds/lobodeath.mp3"},
    "fire":       {"health": 40, "speed": 1.8, "contact_damage": 1, "scale": 0.3, "width": 45, "height": 35, "y_offset": 0, "hitbox_scale": (1.3, 1.8), "hitbox_offset": (0, 0), "sprite_path": "Enemies/fire.png","detection_radius": 300, "death_sound": "sounds/lobodeath.mp3"},
    "jades":      {"health": 80, "speed": 1.5, "contact_damage": 1, "scale": 0.3, "width": 45, "height": 35, "y_offset": 0, "hitbox_scale": (1.3, 1.8), "hitbox_offset": (0, 0), "sprite_path": "Enemies/jades.png","detection_radius": 300, "death_sound": "sounds/lobodeath.mp3"},
    "wind":       {"health": 35, "speed": 2.2, "contact_damage": 1, "scale": 0.3, "width": 45, "height": 35, "y_offset": 0, "hitbox_scale": (1.3, 1.8), "hitbox_offset": (0, 0), "sprite_path": "Enemies/wind.png","detection_radius": 300, "death_sound": "sounds/lobodeath.mp3"},
    
    "esqueleto": {
        "health": 60, "speed": 1.5, "death_sound": "sounds/muerte_esqueleto.wav", "scale": 2.0, "width": 60, "height": 90, "y_offset": 0, "hitbox_scale": (0.8, 0.9), "hitbox_offset": (0, 0),
        "attack_damage": 15, "attack_range": 120, "attack_cooldown": 1500, "attack_damage_frame": 4, "detection_radius": 400,
        "anim_data": { "attack": {"path": "Enemies/Skeleton/skeleton_atk.png", "frames": 6} }
    },
    "golem": {
        "health": 150, "speed": 1, "death_sound": "sounds/muerte_golem.wav", "scale": 4.5, "width": 140, "height": 130, "y_offset": 0, "hitbox_scale": (1.8, 2.0), "hitbox_offset": (0, 0),
        "attack_damage": 25, "attack_range": 220, "attack_cooldown": 2200, "attack_damage_frame": 5, "detection_radius": 350,
        "anim_data": {
            "idle":   {"path": "Enemies/golem/Golem_1_idle.png",   "frames": 8},
            "walk":   {"path": "Enemies/golem/Golem_1_walk.png",   "frames": 10},
            "attack": {"path": "Enemies/golem/Golem_1_attack.png", "frames": 11},
            "die":    {"path": "Enemies/golem/Golem_1_die.png",    "frames": 13}
        }
    },
    "wizzardblue": {
        "health": 70, "speed": 1.8, "death_sound": "sounds/lobodeath.mp3",
        "scale": 0.4, "width": 40, "height": 55, "y_offset": 0, "hitbox_scale": (1.4,2.0), "hitbox_offset": (0,0),
        "contact_damage": 0, 
        "attack_range": 400, "attack_cooldown": 2500, "detection_radius": 2500,
        "is_flying": True, "is_ranged": True, 
        "sprite_path": "Enemies/wizzardblue.png"
    },

    "golem_2": {
        "health": 180, "speed": 1.2, "death_sound": "sounds/muerte_golem.wav", "scale": 4, "width": 130, "height": 120, "y_offset": 5, "hitbox_scale": (1.3,2.0), "hitbox_offset": (0, 0),
        "attack_damage": 30, "attack_range": 200, "attack_cooldown": 2500, "attack_damage_frame": 6, "detection_radius": 400,
        "anim_data": {
            "idle":   {"path": "Enemies/golemcito/Golem_2_idle.png",   "frames": 8},
            "walk":   {"path": "Enemies/golemcito/Golem_2_walk.png",   "frames": 10},
            "attack": {"path": "Enemies/golemcito/Golem_2_attack.png", "frames": 11},
            "die":    {"path": "Enemies/golemcito/Golem_2_die.png",    "frames": 13}
        }
        },

    "boss1": {
        "health": BOSS_HEALTH, "speed": 0, "death_sound": "sounds/muerte_jefe.wav", "scale": 1.0, "width": 250, "height": 250, "y_offset": 50, "hitbox_scale": (1.3, 4.0), "hitbox_offset": (0,0),
        "sprite_path": "Enemies/boss1.png",
        "is_boss": True
    },

        "nightborne": {
        "health": 500, "speed": 2.6, "death_sound": "sounds/muerte_jefe.wav", # <-- VELOCIDAD AÑADIDA
        "scale": 4.0, "width": 200, "height": 180, "y_offset": 5, "hitbox_scale": (0.5, 0.9), "hitbox_offset": (0,0),
        "is_boss": True,
        "attack_damage": 40, "attack_range": 150, "attack_damage_frame": 5, "detection_radius": 600, # <-- RANGOS AJUSTADOS
        "anim_data": {
            "idle":   {"path": "Enemies/NightBorne/nightborne_idle.png",   "frames": 9},
            "walk":   {"path": "Enemies/NightBorne/nightborne_walk.png",   "frames": 6},
            "attack": {"path": "Enemies/NightBorne/nightborne_attack.png", "frames": 12},
            "die":    {"path": "Enemies/NightBorne/nightborne_die.png",    "frames": 21}
        }
    },

    "agis": {
        "health": 400, "speed": 0, "death_sound": "sounds/muerte_jefe.wav",
        "scale": 4.0, "width": 100, "height": 180, "y_offset": 0, "hitbox_scale": (0.8, 2.0), "hitbox_offset": (0,0),
        "is_boss": True,
        "anim_data": {
            "idle": {"path": "Enemies/Agis.png", "frames": 15},
            "die": {"path": "Enemies/agis_die.png", "frames": 8}
        }
    }

}

# --- Map and Sound Paths ---
MAP_BOSQUE_PATH = "fondos/mapa_bosque.png"; 
MAP_ALDEA_PATH = "fondos/mapa_aldea.png"
MAP_MAZMORRA_PATH = "fondos/mapa_mazmorra.png"; 
MAP_MAZMORRA_P1_PATH = "fondos/mazmorra_p1.png"
MAP_MAZMORRA_P2_PATH = "fondos/mazmorra_p2.png"; 
MAP_MAZMORRA_P3_PATH = "fondos/mazmorra_p3.png"
MAP_MAZMORRA_P4_PATH = "fondos/mazmorra_p4.png"; 
MAP_MAZMORRA_P5_PATH = "fondos/mazmorra_p5.png"
MAP_MAZMORRA_JEFE_PATH = "fondos/mapa_boss1.png"
MAP_MAZMORRA_P6_PATH = "fondos/mazmorra_p6.png"
MAP_MAZMORRA_BOSS2_PATH = "fondos/mazmorra_boss2.png"

MENU_MUSIC_PATH = "Soundtracks/menu.mp3"
BOSS_MUSIC_PATH = "Soundtracks/soundtrackboss1.mp3"
ENDING_MUSIC_PATH = "Soundtracks/ending.mp3"

INITIAL_ZOOM = 0.85
DEATH_QUOTES = [
    ("Alguien lee esto??", "El que paga el internet"),
    ("Por cada taza de arroz, dos de agua. Y para cada boss, paciencia.", "Madre de Prota"),
    ("Se te acabo la carga, mi rey.", "Eneeh"),
    ("El 'Game Over' es solo una sugerencia.", "Guru del Grind"),
    ("Menos vida que el internet de Multicable en la tormenta.", "Un Hondureño Frustrado"),
    ("Otra vez a empezar. Como lunes despues de feriado.", "Eduardo Maldonado"),
    ("Creiste que era facil, ¿verdad? Como conseguir una baleada con todo en hora pico.", "El Maje de la Baleada"),
    ("Tu ego fue mas grande que tu barra de vida.", "La Espada Vengativa"),
    ("No te preocupes, la venganza es un plato que se come con consomé.", "La Abuela de Cristian"),
    ("Ni con el poder de la Monja Blanca lograste esto.", "El Espectro Olvidado"),
    ("50% de descuento en linea blanca.", "El Gallo mas Gallo"),
    ("Casi lo logras. Casi. Como la H en el ultimo mundial.", "El Comentarista Deportivo"),
    ("Te mato el lag, no el enemigo.", "El Server Caido"),
    ("La proxima vez, no te confies como cuando dejaste el arroz en la estufa.", "El Vecino Preocupado"),
    ("Hasta aqui te trajo la corriente. Y tu mala decision.", "El Rio Ulua"),
    ("Ni todas las baleadas del mundo te van a revivir.", "Doña Susy"),
    ("Eso te pasa por andar de vivo.", "El Espejo de la Realidad"),
    ("Un valiente menos. Un dolor de cabeza mas para el programador.", "Gemini"),
    ("La oscuridad siempre te espera. Especialmente cuando se va la luz.", "La ENEE"),
    ("No te moriste, solo te tomaste un descanso eterno.", "El Entrenador Espiritual"),
]