# 🎮 Ahorcado Profesional con Pygame

Un juego del ahorcado con interfaz gráfica profesional, desarrollado en Python usando
la biblioteca **pygame**.

## 📁 Estructura del proyecto

```
ahorcado/
├── main.py              # Punto de entrada principal y manejo de pantallas
├── game.py              # Lógica del juego (palabra, intentos, victoria/derrota)
├── graphics.py          # Funciones de dibujo (ahorcado, botones, textos)
├── constants.py         # Constantes de colores, fuentes y dimensiones
├── requirements.txt     # Dependencias de producción
├── requirements-dev.txt # Dependencias de desarrollo (pytest)
├── run.sh               # Script lanzador portable
├── tests/
│   └── test_game.py     # Tests de la lógica del juego
├── assets/              # Recursos opcionales (imágenes/sonidos)
└── README.md            # Este archivo
```

## 🔧 Instalación

Se recomienda un entorno virtual para no afectar otras instalaciones de Python:

```bash
python3 -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Para development + tests:

```bash
pip install -r requirements-dev.txt
```

## 🚀 Cómo ejecutar

### Opción 1: Script lanzador (recomendada)
```bash
./run.sh
```

El script detecta automáticamente el entorno virtual activo, un `.venv` local o el
`python3` del sistema, y muestra un mensaje claro si falta pygame.

### Opción 2: Ejecución directa
```bash
python3 main.py
```

## ✅ Tests

```bash
python3 -m pytest tests/ -v
```

Cubren validación de entrada, estado post-partida, reglas básicas y selección
de palabras sin repeticiones consecutivas.

## 🎯 Cómo jugar

- Haz clic en **"Jugar"** en la pantalla de inicio.
- Adivina la palabra haciendo clic en los botones del alfabeto o usando el teclado.
- Tienes **6 intentos** antes de que el ahorcado se complete.
- Si adivinas todas las letras, ¡ganas! Si se agotan los intentos, pierdes.

## ✨ Características

- Ventana 1000×700 con título y paleta de colores profesional.
- **Ahorcado con colores contrastantes** (beige dorado y coral) sobre panel azul,
  fácil de distinguir.
- **Layout organizado en zonas sin solapes**: cabecera, palabra, ahorcado,
  panel de fallos y alfabeto.
- Palabra mostrada en **casitas individuales** que se iluminan en verde al acertar.
- Botones del alfabeto con efecto hover y estados visuales (sin usar / acertado / fallado).
- Panel lateral con las letras falladas en cuadrícula.
- Indicadores de vidas como puntos de colores en la cabecera.
- Pantallas de inicio, victoria y derrota con paneles centrados.
- **Opción para salir** en el menú y en las pantallas de resultado (botón "SALIR" o tecla `Esc`).
- Soporte para mouse y teclado (`Enter` juega, `N` nueva partida, `M` menú, `Esc` menú/salir).
- **Validación de entrada**: se ignoran letras vacías, multi-carácter y adivinanzas
  posteriores al fin de la partida.
- **Sin repeticiones consecutivas** de palabra entre partidas.
- Bucle principal a 60 FPS.

## 🎨 Paleta de colores

| Elemento | Color |
|----------|-------|
| Fondo | Azul noche `(18, 28, 48)` |
| Paneles | Azul `(30, 45, 70)` |
| Texto | Blanco suave `(235, 242, 250)` |
| Horca | Beige dorado `(215, 195, 150)` |
| Prisionero | Coral `(235, 140, 90)` |
| Botones | Azul `(55, 110, 175)` |
| Hover | Azul claro `(85, 155, 235)` |
| Acertado | Verde `(100, 200, 140)` |
| Fallado | Rojo coral `(235, 110, 110)` |
