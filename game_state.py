import json
import os
from datetime import datetime

SAVES_DIR = "saves" # El nombre de nuestra carpeta de guardado

# --- MODIFICAR LA FUNCIÓN save_game ---
def save_game(data, custom_name=None): # Añadir custom_name con valor por defecto None
    """Guarda el estado del juego en un nuevo archivo con fecha y hora, o un nombre personalizado."""
    # 1. Asegura que la carpeta 'saves' exista
    if not os.path.exists(SAVES_DIR): #
        os.makedirs(SAVES_DIR) #

    # 2. Crea un nombre de archivo único
    if custom_name: #
        # Asegurarse de que el nombre sea seguro para el sistema de archivos
        # y añadir la extensión .json si no la tiene
        safe_name = "".join(c for c in custom_name if c.isalnum() or c in (' ', '_', '-')).strip() #
        if not safe_name: # Si el nombre resulta vacío después de limpiar
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") #
            filename = f"save_{timestamp}.json" #
        else:
            filename = f"{safe_name}.json" # Usar el nombre personalizado
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") #
        filename = f"save_{timestamp}.json" #
        
    filepath = os.path.join(SAVES_DIR, filename) #

    # 3. Guarda los datos en el nuevo archivo
    try:
        with open(filepath, 'w') as f: #
            json.dump(data, f, indent=4) #
        print(f"Partida guardada en: {filepath}") #
    except Exception as e:
        print(f"Error al guardar la partida: {e}") #

def load_game(filename):
    """Carga una partida específica desde la carpeta 'saves'."""
    filepath = os.path.join(SAVES_DIR, filename) #
    if not os.path.exists(filepath): #
        print(f"Error: No se encontró el archivo de guardado {filename}") #
        return None #
    try:
        with open(filepath, 'r') as f: #
            print(f"Cargando partida: {filename}") #
            return json.load(f) #
    except Exception as e:
        print(f"Error al cargar la partida: {e}") #
        return None #

def get_saved_games():
    """Devuelve una lista de todas las partidas guardadas, ordenadas por la más reciente."""
    if not os.path.exists(SAVES_DIR): #
        return [] # Devuelve una lista vacía si no hay carpeta

    try:
        # Obtiene todos los archivos .json de la carpeta de guardado
        files = [f for f in os.listdir(SAVES_DIR) if f.endswith(".json")] #
        # Ordena los archivos por fecha de modificación (el más nuevo primero)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(SAVES_DIR, x)), reverse=True) #
        return files #
    except Exception as e:
        print(f"Error al obtener partidas guardadas: {e}") #
        return [] #