# constants.py - Constantes del juego del ahorcado

# Dimensiones de la ventana
ANCHO = 1000
ALTO = 700
FPS = 60

# Título del juego
TITULO_JUEGO = "Ahorcado Profesional"

# --- Paleta de colores ---
# Fondo
COLOR_FONDO = (18, 28, 48)          # Azul noche profundo
COLOR_PANEL = (30, 45, 70)          # Azul más claro para paneles
COLOR_PANEL_BORDE = (70, 100, 145)  # Borde de paneles

# Texto
COLOR_TEXTO = (235, 242, 250)       # Blanco suave (alto contraste)
COLOR_TEXTO_SUAVE = (150, 170, 200) # Gris azulado para etiquetas

# Estructura del ahorcado (colores claros que resaltan sobre el fondo)
COLOR_AHORCADO = (215, 195, 150)    # Beige dorado para la horca
COLOR_CUERPO = (235, 140, 90)       # Coral/naranja para el prisionero
COLOR_CUERPO_DETALLE = (255, 210, 160)  # Piel clara para la cabeza

# Botones
COLOR_BOTON = (55, 110, 175)        # Azul medio
COLOR_HOVER = (85, 155, 235)        # Azul claro al pasar el mouse
COLOR_BOTON_BORDE = (120, 175, 230) # Borde claro de botones
COLOR_BOTON_USADO = (40, 55, 80)    # Gris oscuro para letras ya usadas
COLOR_BOTON_TEXTO_USADO = (110, 125, 150)

# Casitas de la palabra
COLOR_CASITA = (38, 58, 88)         # Fondo de cada casita
COLOR_CASITA_BORDE = (90, 130, 180) # Borde de cada casita
COLOR_CASITA_ACERTADA = (45, 90, 70)      # Verde suave si se adivinó
COLOR_CASITA_ACERTADA_BORDE = (100, 200, 140)

# Estados
COLOR_LETRAS_INCORRECTAS = (235, 110, 110)  # Rojo coral
COLOR_GANADO = (100, 220, 150)      # Verde brillante
COLOR_PERDISTE = (235, 110, 110)    # Rojo

# Configuración de fuentes
FUENTE_TITULO = "Arial"
FUENTE_DEFAULT = "Arial"

# Configuración del ahorcado
MAX_INTENTOS = 6

# --- Layout de la pantalla de juego ---
# Cabecera
HEADER_ALTO = 70

# Palabra (zona superior)
PALABRA_Y = 105
PALABRA_CASITA_ANCHO = 56
PALABRA_CASITA_ALTO = 60
PALABRA_SEPARACION = 10

# Ahorcado (zona media izquierda)
AHORCADO_CENTRO_X = 330
AHORCADO_CENTRO_Y = 345

# Panel de letras falladas (zona media derecha)
PANEL_FALLOS_X = 590
PANEL_FALLOS_Y = 205
PANEL_FALLOS_ANCHO = 320
PANEL_FALLOS_ALTO = 230

# Alfabeto (zona inferior)
ALFABETO_Y = 530
ALFABETO_COLUMNAS = 13
ALFABETO_BOTON_ANCHO = 48
ALFABETO_BOTON_ALTO = 48
ALFABETO_SEPARACION = 12
