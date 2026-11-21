#!/bin/bash
# Lanzador portable del juego del ahorcado con pygame.
set -euo pipefail

cd "$(dirname "$0")"

# Resolver el intérprete: entorno virtual activo > venv local > python3 del sistema.
if [ -n "${VIRTUAL_ENV:-}" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
    PYTHON="$VIRTUAL_ENV/bin/python"
elif [ -x ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
else
    PYTHON="python3"
fi

# Verificar dependencia antes de lanzar, con un mensaje accionable.
if ! "$PYTHON" -c "import pygame" >/dev/null 2>&1; then
    echo "Error: pygame no está disponible en $PYTHON" >&2
    echo "Instálalo con:" >&2
    echo "  $PYTHON -m pip install -r requirements.txt" >&2
    exit 1
fi

exec "$PYTHON" main.py
