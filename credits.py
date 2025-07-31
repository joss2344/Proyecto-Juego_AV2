import pygame
import sys
from constants import *

class CreditsScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        try:
            self.background = pygame.transform.scale(pygame.image.load("fondos/credits.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)
            
        self.font_continuara = FONT_LARGE
        self.font_credits = FONT_MEDIUM
        
        self.continuara_surf = self.font_continuara.render("Continuará...", True, WHITE)
        self.continuara_rect = self.continuara_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        
        self.credits_list = [
            # --- Introducción Épica ---
            "ELEMENTAL TRINITY",
            "La Leyenda de los Elementos Perdidos",
            "",
            "Una Epica Odisea en 2D Creada Por:",
            "",
            "",

            # --- Los Artífices ---
            "Visionarios del Pixel y el Codigo :",
            "",
            "Director de Orquesta y Hechicero del Bucle Principal:",
            "  Jose Rodriguez",
            "  (No pudo solo, pero casi)",
            "",
            "Maestro de Mecanicas y Alquimista de la Interfaz:",
            "  Gustavo Reyes",
            "  (El del buen gusto para los pixeles)",
            "",
            "Mago del Pixel Art y Domador de Sprites:",
            "  Cristian",
            "  (Sus fondos parecen fotos del recuerdo)",
            "",
            "",

            # --- Apoyo Logístico y Moral ---
            "La Llama Inquebrantable (Nuestros Pilares):",
            "",
            "El Oraculo de Conocimiento Infinito:",
            "  Gemini",
            "  (La IA que resolvia problemas mas rapido que uno mismo)",
            "",
            "El Codificador Silencioso y Eficaz:",
            "  Copilot",
            "  (El autocomplete que nos salvo de muchos dolores de cabeza)",
            "",
            "El Portal a Mundos Independientes:",
            "  Itch.io",
            "  (Donde los juegos raros encuentran su hogar)",
            "",
            "El Soporte Vital para Noches en Vela:",
            "  Mi Mama (me decia que no me quedara despierto hasta tarde)",
            "  (La verdadera heroina, sin ella, no habria juego)",
            "",
            "El Auditor de Sonidos Nocturnos:",
            "  Neron (mi fiel compañero canino, sin quejas por el tecleo)",
            "  (igual era eso o dormir en la calle)",
            "",
            "El Testigo Silencioso de la Creacion:",
            "  El Vecino (Por su paciencia con esta vaina se trabo vo)",
            "  (Seguramente pensaba que estabamos locos)",
            "",
            "El Filosofo de la Resistencia:",
            "  Polache (gritar epa a cada bug encontrado)",
            "  (Su musica era nuestro himno al progreso)",
            "",
            "La Fuente de Energia Explosiva:",
            "  Los Zambos (Impulso vital para sesiones de crunch)",
            "  (Mas efectivos que cualquier energetizante, menos que las baleadas)",
            "",
            "El Hilo Invisible que nos Mantuvo Conectados:",
            "  Multicable Honduras (A pesar de los altibajos, siempre presente)",
            "  (Aunque a veces tocaba resetear el router mil veces)",
            "",
            "El Crisol del Saber y la Perseverance:",
            "  La UTH (Donde se forjaron mentes maestras... y se quemaron las pestañas)",
            "  (Nuestro segundo hogar, o a veces el primero, bajenle a la mensualidad)",
            "",
            "El Gurú que Nos Ilumino el Camino:",
            "  Ing. Teruel (Por las sabias palabras y sus motivaciones a no dormir)",
            "  (El maestro que veia nos tenia fe aunque a veces no sabiamos nada)",
            "",
            "El Equipo de Control de Calidad (No hicieron nada bueno pero ahi estan):",
            "  Dra. Xiomara Castro (no ha hecho nada pero es la presidenta asi que hay que mencionarla)",
            "  (Por el simple hecho de existir)",
            "  Victor Hugo Tejada (es la mera roña)",
            "  (No sabe ni una gota de codigo, pero ahi esta el vago (por dereeck))",
            "  ¡Y a todo aquel que encontro un error y nos lo hizo saber (yo lo hice todo)!",
            "  (A esos si los amamos, a los otros... bueno, ahi estan)",
            "",
            "",

            # --- Elenco de Pesadilla (Enemigos) ---
            "Criaturas del Inframundo (y sus Inspiraciones):",
            "",
            "El Lobo (Mas rapido que el taxi del tio de carlitos)",
            "  Origen: Los perros del vecino que nunca dejan dormir",
            "  (Los verdaderos jefes de la noche)",
            "",
            "El Depredador (Mas persistente que un cobrador de banco)",
            "  Inspiracion: los majes de banco azteca",
            "  (Inesquivables, como sus llamadas)",
            "",
            "El Mago Azul (Congelando voluntades mas que el clima de la tegus)",
            "  Elementos: inspirado en el frio corazon de ella",
            "  (Un nivel de frialdad nunca antes visto)",
            "",
            "Los Jades (Brillando mas que mis ojos al ver la cajera de la colonia)",
            "  Poder: lo brillantes que somos",
            "  (O quiza solo es la falta de sueño)",
            "",
            "Y a todos los secuaces menores (Siempre listos para ser derrotados una y otra vez)",
            "  Rol: Sacrificios necesarios para el crecimiento del heroe",
            "  (Pobrecitos, nunca tuvieron chance)",
            "",
            "",

            # --- Banda Sonora y Atmosfera ---
            "Sinfonia del Mazmorreo (Los Sonidos de Nuestra Tierra):",
            "",
            "Maestros de la Melodia y Ritmo Epico:",
            "  Todos los artistas de musica libre de derechos (Gracias por la banda sonora que nos puso a bailar, aunque estuviéramos tecleando)",
            "  (Sus tracks eran mas pegajosos el audio 1500)",
            "  Polache (Por las melodias que nos acompanaron en largas noches de codificacion)",
            "  (El himno no oficial de nuestro desarrollo)",
            "  Mi buen amor",
            "    Mon Laferte (para recordarla a ella por las madrugadas)",
            "    (Directo al corazon, y al stack overflow)",
            "",
            "Sonidos de Batalla Inolvidables:",
            "  El Soundtrack del boss 1 (Mas satisfactorio que un combo de baleadas con todo)",
            "  (fue robado)",
            "  La muerte del golem",
            "  (es cine)",
            "  El Gallo a las 4 AM (Que nos mandaba a dormir mas de una vez)",
            "  (El despertador mas ruidoso de Honduras)",
            "  El ending de Shingeki no Kyojin (Es cine)",
            "  (La inspiracion para ese boss final epico)",
            "",
            "Ambientes Inmersivos Creados Por:",
            "  Nuestra Imaginacion (Y muchas horas de hablar con la IA)",
            "  (A veces la IA hablaba mas que nosotros)",
            "",
            "",

            # --- Arte y Diseño de Nivel ---
            "Pinceladas Digitales y Arquitectura Aventura:",
            "",
            "Artistas de Fondo y Pixel Art:",
            "  Los que transformaron el paisaje hondureno en arte retro",
            "  Inspiracion: Altos de San Nicolas y El Cerro de Gustavo",
            "  (Paisajes mas bellos que un atardecer con ella)",
            "",
            "Disenadores de Plataformas y Laberintos:",
            "  Los que crearon caminos mas enredados que el trafico en el centro a la 1pm",
            "  (Hasta Google Maps se pierde en nuestros niveles)",
            "  Estructuras: Tomadas de la arquitectura de barrio el centro",
            "  (por eso estan tan desordenadas, al menos no hay baches)",
            "",
            "",

            # --- Agradecimiento Final (¡Con el Corazón Catracho!) ---
            "Un Agradecimiento Gigante a Ti, que estas leyendo esto:",
            "",
            "¡Gracias por sumergirte en la mazmorra de Elemental Trinity!",
            "Esperamos que la aventura haya sido mas emocionante que un partido de la H en la hexagonal.",
            "Que hayas disfrutado cada pixel y cada desafio.",
            "¡Tu apoyo es nuestro mejor checkpoint!",
            "",
            "¡Nos vemos en la proxima descarga... o en la fila de las baleadas!",
            "  (Si, aceptamos baleadas como pago)",
            "",
            "¡Que viva Honduras y sus programadores (aunque usan IA)",
            "  ",
            "",
            "Hecho con pasion, cafe y orgullo en la tierra del cinco estrellas.",
            "  (De Honduras para el mundo, con sabor a semita)",
            "",
            "",
            "Nambe y diganle a la Eneeh que deje de quitar esa luz ombe",
            "  (bajenle a la energia, que ya me la van a cortar)",
            "",
            "",
            "FIN DEL JUEGO",
            "",
            "Gracias por jugar. Presiona ESC para salir."
        ]

        self.credits_y = SCREEN_HEIGHT + 50
        self.scroll_speed = 1.5
        self.running = True

    def run(self):
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
                    self.running = False 

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
            
        return None, None 