# main.py - Punto de entrada principal del juego del ahorcado

import pygame
import sys
import os

# Agregar el directorio del proyecto al path para importar módulos
sys.path.insert(0, os.path.dirname(__file__))

from constants import (
    ANCHO, ALTO, FPS, TITULO_JUEGO,
    ALFABETO_COLUMNAS, ALFABETO_BOTON_ANCHO, ALFABETO_BOTON_ALTO,
    ALFABETO_SEPARACION, ALFABETO_Y,
    FUENTE_TITULO, FUENTE_DEFAULT,
    COLOR_FONDO, COLOR_PANEL, COLOR_PANEL_BORDE, COLOR_TEXTO_SUAVE,
    COLOR_GANADO, COLOR_PERDISTE,
)
from game import Ahorcado
from graphics import (
    dibujar_ahorcado, dibujar_palabra, dibujar_boton, dibujar_boton_letra,
    dibujar_texto_central, dibujar_cabecera, dibujar_panel_fallos,
)

# Botones del alfabeto (compartidos entre funciones)
botones_alfabeto = []


def iniciar_pygame():
    """Inicializa pygame y configura la ventana principal."""
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO_JUEGO)

    reloj = pygame.time.Clock()
    return pantalla, reloj


def crear_botones_alfabeto():
    """Crea los botones del alfabeto centrados en la zona inferior."""
    botones_alfabeto.clear()

    ancho_total = (ALFABETO_COLUMNAS * ALFABETO_BOTON_ANCHO +
                   (ALFABETO_COLUMNAS - 1) * ALFABETO_SEPARACION)
    x_inicio = (ANCHO - ancho_total) // 2

    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, letra in enumerate(letras):
        fila = i // ALFABETO_COLUMNAS
        col = i % ALFABETO_COLUMNAS
        x = x_inicio + col * (ALFABETO_BOTON_ANCHO + ALFABETO_SEPARACION)
        y = ALFABETO_Y + fila * (ALFABETO_BOTON_ALTO + ALFABETO_SEPARACION)
        rect = pygame.Rect(x, y, ALFABETO_BOTON_ANCHO, ALFABETO_BOTON_ALTO)
        botones_alfabeto.append({
            "rect": rect,
            "letra": letra,
            "usada": False,
            "acertada": False,
        })


def reset_botones_alfabeto():
    """Reinicia el estado de los botones del alfabeto."""
    for btn in botones_alfabeto:
        btn["usada"] = False
        btn["acertada"] = False


def manejar_eventos_juego(ahorcado):
    """Maneja los eventos durante la partida activa.

    Args:
        ahorcado: Instancia de Ahorcado.

    Returns:
        str or None: Estado al que cambiar, o None para continuar.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "salir"

        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for btn in botones_alfabeto:
                if not btn["usada"] and btn["rect"].collidepoint(mouse_pos):
                    letra = btn["letra"]
                    btn["usada"] = True
                    resultado = ahorcado.adivinar_letra(letra)
                    btn["acertada"] = (resultado is True)
                    break  # Solo un botón por clic

        if evento.type == pygame.KEYDOWN:
            # Permitir adivinar letras usando el teclado
            if evento.unicode.isalpha() and len(evento.unicode) == 1:
                letra = evento.unicode.upper()
                for btn in botones_alfabeto:
                    if btn["letra"] == letra and not btn["usada"]:
                        btn["usada"] = True
                        resultado = ahorcado.adivinar_letra(letra)
                        btn["acertada"] = (resultado is True)
                        break

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "menu"

    # Verificar fin de juego después de procesar eventos
    if not ahorcado.juego_activo:
        if ahorcado.todas_letras_adivinadas():
            return "victoria"
        return "derrota"

    return None


def dibujar_pantalla_juego(pantalla, ahorcado, fuentes):
    """Dibuja todos los elementos de la pantalla de juego.

    Args:
        pantalla: Superficie de pygame.
        ahorcado: Instancia de Ahorcado.
        fuentes: Dict con las fuentes cargadas.
    """
    pantalla.fill(COLOR_FONDO)

    # Cabecera con título e indicadores de vidas
    dibujar_cabecera(pantalla, ahorcado.intentos_restantes,
                     fuentes["titulo"], fuentes["estado"])

    # Palabra con casitas
    dibujar_palabra(pantalla, ahorcado.palabra_mostrar(),
                    ahorcado.letras_adivinadas, fuentes["palabra"])

    # Ahorcado y panel de fallos
    dibujar_ahorcado(pantalla, ahorcado.intentos_restantes)
    dibujar_panel_fallos(pantalla, ahorcado.letras_incorrectas,
                         fuentes["letras"], fuentes["estado"])

    # Etiqueta del alfabeto y pista de teclado
    etiqueta = fuentes["estado"].render("Alfabeto", True, COLOR_TEXTO_SUAVE)
    pantalla.blit(etiqueta, (60, ALFABETO_Y - 35))

    pista = fuentes["estado"].render("ESC = menú", True, COLOR_TEXTO_SUAVE)
    pantalla.blit(pista, (ANCHO - pista.get_width() - 60, ALFABETO_Y - 35))

    # Botones del alfabeto
    for btn in botones_alfabeto:
        dibujar_boton_letra(pantalla, btn["rect"], btn["letra"],
                            fuentes["boton"], btn["usada"], btn["acertada"])


def pantalla_inicio(pantalla, reloj, fuentes):
    """Muestra la pantalla de inicio.

    Returns:
        str: Estado al que regresar ("jugando" o "salir").
    """
    esperando = True
    while esperando:
        reloj.tick(FPS)
        pantalla.fill(COLOR_FONDO)

        # Panel central decorativo
        panel = pygame.Rect(ANCHO // 2 - 340, ALTO // 2 - 220, 680, 440)
        pygame.draw.rect(pantalla, COLOR_PANEL, panel, border_radius=24)
        pygame.draw.rect(pantalla, COLOR_PANEL_BORDE, panel,
                         width=2, border_radius=24)

        dibujar_texto_central(pantalla, "AHORCADO", fuentes["titulo"],
                              centrado=(ANCHO // 2, ALTO // 2 - 110))

        dibujar_texto_central(pantalla, "Adivina la palabra antes de que sea tarde",
                              fuentes["estado"], color=COLOR_TEXTO_SUAVE,
                              centrado=(ANCHO // 2, ALTO // 2 - 20))

        ancho_jugar = 200
        ancho_salir = 160
        separacion = 20
        x_inicio = ANCHO // 2 - ancho_jugar - separacion // 2

        btn_jugar = dibujar_boton(pantalla, x_inicio, ALTO // 2 + 50,
                                  ancho_jugar, 60, "JUGAR", fuentes["boton"])
        btn_salir = dibujar_boton(pantalla,
                                  x_inicio + ancho_jugar + separacion,
                                  ALTO // 2 + 50, ancho_salir, 60,
                                  "SALIR", fuentes["boton_pequeno"])

        dibujar_texto_central(pantalla,
                              "Haz clic en las letras o usa tu teclado  |  ESC = salir",
                              fuentes["estado"], color=COLOR_TEXTO_SUAVE,
                              centrado=(ANCHO // 2, ALTO // 2 + 155))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_jugar.collidepoint(evento.pos):
                    return "jugando"
                if btn_salir.collidepoint(evento.pos):
                    return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return "jugando"
                if evento.key == pygame.K_ESCAPE:
                    return "salir"

    return "jugando"


def pantalla_resultado(pantalla, reloj, ahorcado, fuentes, gano):
    """Muestra la pantalla de victoria o derrota.

    Args:
        gano: True para victoria, False para derrota.

    Returns:
        str: Estado al que regresar.
    """
    mensaje = "¡HAS GANADO!" if gano else "HAS PERDIDO"
    color = COLOR_GANADO if gano else COLOR_PERDISTE

    esperando = True
    while esperando:
        reloj.tick(FPS)
        pantalla.fill(COLOR_FONDO)

        panel = pygame.Rect(ANCHO // 2 - 320, ALTO // 2 - 230, 640, 460)
        pygame.draw.rect(pantalla, COLOR_PANEL, panel, border_radius=24)
        pygame.draw.rect(pantalla, color, panel, width=3, border_radius=24)

        dibujar_texto_central(pantalla, mensaje, fuentes["grande"], color=color,
                              centrado=(ANCHO // 2, ALTO // 2 - 130))

        palabra_texto = f"La palabra era: {ahorcado.palabra_objetivo.upper()}"
        dibujar_texto_central(pantalla, palabra_texto, fuentes["estado"],
                              centrado=(ANCHO // 2, ALTO // 2 - 40))

        ancho_btn = 280
        alto_btn = 52
        separacion_btn = 30
        x_inicio = ANCHO // 2 - ancho_btn - separacion_btn // 2

        btn_repetir = dibujar_boton(
            pantalla, x_inicio, ALTO // 2 + 40,
            ancho_btn, alto_btn, "JUGAR DE NUEVO", fuentes["boton_pequeno"])
        btn_menu = dibujar_boton(
            pantalla, x_inicio + ancho_btn + separacion_btn, ALTO // 2 + 40,
            ancho_btn, alto_btn, "MENÚ PRINCIPAL", fuentes["boton_pequeno"])

        btn_salir = dibujar_boton(
            pantalla, ANCHO // 2 - 100, ALTO // 2 + 110,
            200, 44, "SALIR", fuentes["boton_pequeno"])

        dibujar_texto_central(
            pantalla, "N = nueva partida   |   M = menú   |   ESC = salir",
            fuentes["estado"], color=COLOR_TEXTO_SUAVE,
            centrado=(ANCHO // 2, ALTO // 2 + 185))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_repetir.collidepoint(evento.pos):
                    return "nuevo"
                if btn_menu.collidepoint(evento.pos):
                    return "menu"
                if btn_salir.collidepoint(evento.pos):
                    return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_n:
                    return "nuevo"
                if evento.key == pygame.K_m:
                    return "menu"
                if evento.key == pygame.K_ESCAPE:
                    return "salir"

    return "menu"


def cargar_fuentes():
    """Carga y devuelve todas las fuentes usadas en el juego."""
    return {
        "titulo": pygame.font.SysFont(FUENTE_TITULO, 52, bold=True),
        "grande": pygame.font.SysFont(FUENTE_TITULO, 64, bold=True),
        "palabra": pygame.font.SysFont(FUENTE_DEFAULT, 40, bold=True),
        "boton": pygame.font.SysFont(FUENTE_DEFAULT, 28, bold=True),
        "boton_pequeno": pygame.font.SysFont(FUENTE_DEFAULT, 24, bold=True),
        "letras": pygame.font.SysFont(FUENTE_DEFAULT, 28, bold=True),
        "estado": pygame.font.SysFont(FUENTE_DEFAULT, 24),
    }


def bucle_principal():
    """Bucle principal que controla el flujo entre pantallas."""
    pantalla, reloj = iniciar_pygame()
    fuentes = cargar_fuentes()

    crear_botones_alfabeto()

    estado_actual = "inicio"
    ahorcado = Ahorcado()

    ejecutando = True
    while ejecutando:
        if estado_actual == "inicio":
            estado_actual = pantalla_inicio(pantalla, reloj, fuentes)

        elif estado_actual == "jugando":
            estado = manejar_eventos_juego(ahorcado)
            if estado:
                estado_actual = estado
            dibujar_pantalla_juego(pantalla, ahorcado, fuentes)
            pygame.display.flip()

        elif estado_actual == "victoria":
            estado_actual = pantalla_resultado(pantalla, reloj, ahorcado,
                                               fuentes, gano=True)

        elif estado_actual == "derrota":
            estado_actual = pantalla_resultado(pantalla, reloj, ahorcado,
                                               fuentes, gano=False)

        elif estado_actual in ("nuevo", "menu"):
            ahorcado.nuevo_juego()
            reset_botones_alfabeto()
            estado_actual = "jugando" if estado_actual == "nuevo" else "inicio"

        elif estado_actual == "salir":
            ejecutando = False

        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    bucle_principal()
