# graphics.py - Elementos gráficos y dibujo del ahorcado

import pygame

from constants import (
    ANCHO, HEADER_ALTO, MAX_INTENTOS,
    PALABRA_Y, PALABRA_CASITA_ANCHO, PALABRA_CASITA_ALTO, PALABRA_SEPARACION,
    AHORCADO_CENTRO_X, AHORCADO_CENTRO_Y,
    PANEL_FALLOS_X, PANEL_FALLOS_Y, PANEL_FALLOS_ANCHO, PANEL_FALLOS_ALTO,
    COLOR_FONDO, COLOR_PANEL, COLOR_PANEL_BORDE,
    COLOR_TEXTO, COLOR_TEXTO_SUAVE,
    COLOR_AHORCADO, COLOR_CUERPO, COLOR_CUERPO_DETALLE,
    COLOR_BOTON, COLOR_HOVER, COLOR_BOTON_BORDE,
    COLOR_BOTON_USADO, COLOR_BOTON_TEXTO_USADO,
    COLOR_CASITA, COLOR_CASITA_BORDE,
    COLOR_CASITA_ACERTADA, COLOR_CASITA_ACERTADA_BORDE,
    COLOR_LETRAS_INCORRECTAS, COLOR_GANADO,
)


def dibujar_cabecera(pantalla, intentos_restantes, fuente_titulo, fuente_estado):
    """Dibuja la cabecera con el título y los intentos restantes.

    Args:
        pantalla: Superficie de pygame donde dibujar.
        intentos_restantes: Intentos que quedan.
        fuente_titulo: Fuente para el título.
        fuente_estado: Fuente para el texto de intentos.
    """
    # Línea divisoria inferior
    pygame.draw.line(pantalla, COLOR_PANEL_BORDE,
                     (0, HEADER_ALTO), (ANCHO, HEADER_ALTO), 2)

    # Título a la izquierda
    titulo = fuente_titulo.render("AHORCADO", True, COLOR_TEXTO)
    pantalla.blit(titulo, (30, HEADER_ALTO // 2 - titulo.get_height() // 2))

    # Etiqueta de intentos a la derecha
    etiqueta = fuente_estado.render("Intentos:", True, COLOR_TEXTO_SUAVE)
    pantalla.blit(etiqueta, (ANCHO - 250, 18))

    # Indicadores de vidas (puntos de colores)
    radio = 9
    separation = 30
    inicio_x = ANCHO - 180
    for i in range(MAX_INTENTOS):
        x = inicio_x + i * separation
        color = COLOR_GANADO if i < intentos_restantes else COLOR_PANEL_BORDE
        pygame.draw.circle(pantalla, color, (x, 34), radio)
        pygame.draw.circle(pantalla, COLOR_FONDO, (x, 34), radio, 1)


def dibujar_ahorcado(pantalla, intentos_restantes):
    """Dibuja el ahorcado con colores contrastantes.

    Args:
        pantalla: Superficie de pygame donde dibujar.
        intentos_restantes: Número de intentos restantes (0 a MAX_INTENTOS).
    """
    cx = AHORCADO_CENTRO_X
    cy = AHORCADO_CENTRO_Y

    # --- Panel de fondo para que resalte ---
    panel = pygame.Rect(cx - 120, cy - 165, 240, 335)
    pygame.draw.rect(pantalla, COLOR_PANEL, panel, border_radius=16)
    pygame.draw.rect(pantalla, COLOR_PANEL_BORDE, panel, width=2, border_radius=16)

    # --- Estructura (beige dorado) ---
    grosor = 7
    # Base
    pygame.draw.line(pantalla, COLOR_AHORCADO,
                     (cx - 90, cy + 150), (cx + 90, cy + 150), grosor)
    # Poste vertical
    pygame.draw.line(pantalla, COLOR_AHORCADO,
                     (cx + 70, cy + 150), (cx + 70, cy - 150), grosor)
    # Viga horizontal
    pygame.draw.line(pantalla, COLOR_AHORCADO,
                     (cx + 70, cy - 150), (cx - 40, cy - 150), grosor)
    # Soga
    pygame.draw.line(pantalla, COLOR_AHORCADO,
                     (cx - 40, cy - 150), (cx - 40, cy - 118), 4)

    fallos = MAX_INTENTOS - intentos_restantes

    # Cabeza (fallo 1)
    if fallos >= 1:
        pygame.draw.circle(pantalla, COLOR_CUERPO_DETALLE,
                           (cx - 40, cy - 88), 30, 0)
        pygame.draw.circle(pantalla, COLOR_CUERPO,
                           (cx - 40, cy - 88), 30, 4)
        # Ojos
        pygame.draw.circle(pantalla, COLOR_FONDO, (cx - 50, cy - 92), 4)
        pygame.draw.circle(pantalla, COLOR_FONDO, (cx - 30, cy - 92), 4)

    # Cuerpo (fallo 2)
    if fallos >= 2:
        pygame.draw.line(pantalla, COLOR_CUERPO,
                         (cx - 40, cy - 58), (cx - 40, cy + 40), grosor)

    # Brazo izquierdo (fallo 3)
    if fallos >= 3:
        pygame.draw.line(pantalla, COLOR_CUERPO,
                         (cx - 40, cy - 40), (cx - 90, cy + 10), grosor)

    # Brazo derecho (fallo 4)
    if fallos >= 4:
        pygame.draw.line(pantalla, COLOR_CUERPO,
                         (cx - 40, cy - 40), (cx + 10, cy + 10), grosor)

    # Pierna izquierda (fallo 5)
    if fallos >= 5:
        pygame.draw.line(pantalla, COLOR_CUERPO,
                         (cx - 40, cy + 40), (cx - 85, cy + 120), grosor)

    # Pierna derecha (fallo 6)
    if fallos >= 6:
        pygame.draw.line(pantalla, COLOR_CUERPO,
                         (cx - 40, cy + 40), (cx + 5, cy + 120), grosor)


def dibujar_palabra(pantalla, palabra_mostrar, letras_adivinadas, fuente):
    """Dibuja la palabra oculta usando casitas individuales.

    Args:
        pantalla: Superficie de pygame donde dibujar.
        palabra_mostrar: Cadena como "p _ t h o n" (con espacios).
        letras_adivinadas: Set de letras correctas para colorear las casitas.
        fuente: Fuente de pygame para las letras.

    Returns:
        Rect: Rectángulo que abarca toda la palabra.
    """
    letras = palabra_mostrar.split(" ")
    n = len(letras)
    ancho_total = n * PALABRA_CASITA_ANCHO + (n - 1) * PALABRA_SEPARACION
    x_inicio = (ANCHO - ancho_total) // 2
    y = PALABRA_Y

    for i, letra in enumerate(letras):
        x = x_inicio + i * (PALABRA_CASITA_ANCHO + PALABRA_SEPARACION)
        rect = pygame.Rect(x, y, PALABRA_CASITA_ANCHO, PALABRA_CASITA_ALTO)

        acertada = letra != "_" and letra.lower() in letras_adivinadas
        color_fondo = COLOR_CASITA_ACERTADA if acertada else COLOR_CASITA
        color_borde = COLOR_CASITA_ACERTADA_BORDE if acertada else COLOR_CASITA_BORDE

        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=8)
        pygame.draw.rect(pantalla, color_borde, rect, width=2, border_radius=8)

        if letra != "_":
            texto = fuente.render(letra.upper(), True, COLOR_TEXTO)
            texto_rect = texto.get_rect(center=rect.center)
            pantalla.blit(texto, texto_rect)

    return pygame.Rect(x_inicio, y, ancho_total, PALABRA_CASITA_ALTO)


def dibujar_boton(pantalla, x, y, ancho, alto, texto, fuente,
                  color_fondo=None, color_texto=None,
                  color_hover=None, borde_alto=2, radio_esquina=10):
    """Dibuja un botón redondeado con efecto hover.

    Args:
        pantalla: Superficie de pygame donde dibujar.
        x, y: Coordenadas del borde superior izquierdo.
        ancho, alto: Dimensiones del botón.
        texto: Texto a mostrar.
        fuente: Fuente de pygame.
        color_fondo: Color de fondo por defecto.
        color_texto: Color del texto.
        color_hover: Color al pasar el mouse.
        borde_alto: Grosor del borde.
        radio_esquina: Radio de las esquinas redondeadas.

    Returns:
        Rect: Rectángulo del botón para detección de colisiones.
    """
    if color_fondo is None:
        color_fondo = COLOR_BOTON
    if color_texto is None:
        color_texto = COLOR_TEXTO
    if color_hover is None:
        color_hover = COLOR_HOVER

    mouse_pos = pygame.mouse.get_pos()
    is_hover = (x < mouse_pos[0] < x + ancho and
                y < mouse_pos[1] < y + alto)
    color_actual = color_hover if is_hover else color_fondo

    pygame.draw.rect(pantalla, color_actual, (x, y, ancho, alto),
                     border_radius=radio_esquina)
    pygame.draw.rect(pantalla, COLOR_BOTON_BORDE, (x, y, ancho, alto),
                     border_radius=radio_esquina, width=borde_alto)

    # Auto-ajustar el tamaño de la fuente para que el texto nunca se salga
    padding = 16
    max_ancho = ancho - 2 * padding
    fuente_actual = fuente
    texto_surface = fuente_actual.render(texto, True, color_texto)

    while texto_surface.get_width() > max_ancho and fuente_actual.get_height() > 14:
        nuevo_size = max(14, fuente_actual.get_height() - 2)
        nombre = getattr(fuente_actual, "name", None) or pygame.font.get_default_font()
        es_negrita = getattr(fuente_actual, "bold", False)
        fuente_actual = pygame.font.SysFont(nombre, nuevo_size, bold=es_negrita)
        texto_surface = fuente_actual.render(texto, True, color_texto)

    texto_rect = texto_surface.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(texto_surface, texto_rect)

    return pygame.Rect(x, y, ancho, alto)


def dibujar_boton_letra(pantalla, rect, letra, fuente, usada=False, acertada=False):
    """Dibuja un botón del alfabeto con estado.

    Args:
        pantalla: Superficie de pygame donde dibujar.
        rect: Rectángulo del botón.
        letra: Letra a mostrar.
        fuente: Fuente de pygame.
        usada: Si la letra ya fue intentada.
        acertada: Si la letra intentada fue correcta.

    Returns:
        Rect: Rectángulo del botón.
    """
    mouse_pos = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse_pos) and not usada

    if usada:
        fondo = COLOR_CASITA_ACERTADA if acertada else COLOR_BOTON_USADO
        borde = COLOR_CASITA_ACERTADA_BORDE if acertada else COLOR_PANEL_BORDE
        color_texto = COLOR_TEXTO if acertada else COLOR_BOTON_TEXTO_USADO
    else:
        fondo = COLOR_HOVER if hover else COLOR_BOTON
        borde = COLOR_BOTON_BORDE
        color_texto = COLOR_TEXTO

    pygame.draw.rect(pantalla, fondo, rect, border_radius=8)
    pygame.draw.rect(pantalla, borde, rect, width=2, border_radius=8)

    texto = fuente.render(letra, True, color_texto)
    texto_rect = texto.get_rect(center=rect.center)
    pantalla.blit(texto, texto_rect)

    return rect


def dibujar_panel_fallos(pantalla, letras_incorrectas, fuente, fuente_titulo):
    """Dibuja el panel lateral con las letras falladas.

    Args:
        pantalla: Superficie de pygame donde dibujar.
        letras_incorrectas: Set o lista de letras incorrectas.
        fuente: Fuente para las letras.
        fuente_titulo: Fuente para el título del panel.
    """
    x = PANEL_FALLOS_X
    y = PANEL_FALLOS_Y
    ancho = PANEL_FALLOS_ANCHO
    alto = PANEL_FALLOS_ALTO

    # Fondo del panel
    panel = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, COLOR_PANEL, panel, border_radius=16)
    pygame.draw.rect(pantalla, COLOR_PANEL_BORDE, panel, width=2, border_radius=16)

    # Título
    titulo = fuente_titulo.render("Letras falladas", True, COLOR_TEXTO_SUAVE)
    titulo_rect = titulo.get_rect(center=(x + ancho // 2, y + 30))
    pantalla.blit(titulo, titulo_rect)

    pygame.draw.line(pantalla, COLOR_PANEL_BORDE,
                     (x + 20, y + 55), (x + ancho - 20, y + 55), 1)

    # Letras en cuadrícula de 4 columnas
    letras = sorted(letras_incorrectas)
    cols = 4
    tam = 44
    sep = 14
    inicio_x = x + (ancho - (cols * tam + (cols - 1) * sep)) // 2
    inicio_y = y + 85

    for i, letra in enumerate(letras):
        fila = i // cols
        col = i % cols
        lx = inicio_x + col * (tam + sep)
        ly = inicio_y + fila * (tam + sep)
        rect = pygame.Rect(lx, ly, tam, tam)
        pygame.draw.rect(pantalla, (60, 40, 50), rect, border_radius=8)
        pygame.draw.rect(pantalla, COLOR_LETRAS_INCORRECTAS, rect,
                         width=2, border_radius=8)
        texto = fuente.render(letra.upper(), True, COLOR_LETRAS_INCORRECTAS)
        pantalla.blit(texto, texto.get_rect(center=rect.center))

    if not letras:
        mensaje = fuente.render("¡Ninguna aún!", True, COLOR_TEXTO_SUAVE)
        pantalla.blit(mensaje, mensaje.get_rect(
            center=(x + ancho // 2, y + alto // 2 + 10)))


def dibujar_texto_central(pantalla, mensaje, fuente, color=None,
                          fondo=None, centrado=None):
    """Dibuja texto centrado en pantalla, opcionalmente con fondo.

    Args:
        pantalla: Superficie de pygame donde dibujar.
        mensaje: Texto a mostrar.
        fuente: Fuente de pygame.
        color: Color del texto.
        fondo: Color de fondo opcional.
        centrado: Tupla (x, y) para el centro del texto.

    Returns:
        Rect: Rectángulo del texto.
    """
    if color is None:
        color = COLOR_TEXTO
    if centrado is None:
        centrado = (ANCHO // 2, ALTO // 2)

    texto_surface = fuente.render(mensaje, True, color)
    texto_rect = texto_surface.get_rect(center=centrado)

    if fondo:
        padding = 20
        rect_fondo = texto_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(pantalla, fondo, rect_fondo, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_PANEL_BORDE, rect_fondo,
                         width=2, border_radius=10)

    pantalla.blit(texto_surface, texto_rect)
    return texto_rect

