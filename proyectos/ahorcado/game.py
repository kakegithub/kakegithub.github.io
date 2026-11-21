# game.py - Lógica del juego del ahorcado

import random
from constants import MAX_INTENTOS


class Ahorcado:
    """Clase que gestiona la lógica del juego del ahorcado."""

    def __init__(self, palabras=None):
        """Inicializa un nuevo juego.

        Args:
            palabras: Lista de palabras opcional. Si None, usa una lista por defecto.

        Raises:
            ValueError: Si la lista de palabras está vacía.
        """
        if palabras is None:
            palabras = [
                "python", "pygame", "programacion", "ahorcado",
                "computadora", "desarrollo", "algoritmo", "archivo",
                "variable", "funcion", "bucles", "condicionales",
                "interfaz", "grafico", "animacion", "teclado",
                "mouse", "ventana", "render", "sistema"
            ]

        self.palabras = [
            str(palabra).strip().lower()
            for palabra in palabras
            if str(palabra).strip()
        ]
        if not self.palabras:
            raise ValueError("La lista de palabras no puede estar vacía")

        self.ultima_palabra = None
        self.nuevo_juego()

    def nuevo_juego(self):
        """Reinicia el estado del juego para una nueva partida."""
        candidatas = self.palabras
        if self.ultima_palabra is not None and len(self.palabras) > 1:
            candidatas = [p for p in self.palabras if p != self.ultima_palabra]

        self.palabra_objetivo = random.choice(candidatas)
        self.ultima_palabra = self.palabra_objetivo
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos_restantes = MAX_INTENTOS
        self.juego_activo = True

    def adivinar_letra(self, letra):
        """Intenta adivinar una letra.

        Args:
            letra: Carácter único (string de longitud 1).

        Returns:
            bool or None: True si acertó, False si falló, None si la entrada es
            inválida, la letra ya fue intentada o la partida terminó.
        """
        if not isinstance(letra, str) or len(letra) != 1 or not letra.isalpha():
            return None

        if not self.juego_activo:
            return None

        letra = letra.lower()

        # Ignorar si ya fue adivinada
        if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
            return None

        if letra in self.palabra_objetivo:
            self.letras_adivinadas.add(letra)
            if self.todas_letras_adivinadas():
                self.juego_activo = False
            return True
        else:
            self.letras_incorrectas.add(letra)
            self.intentos_restantes -= 1
            if self.intentos_restantes <= 0:
                self.juego_activo = False
            return False

    def todas_letras_adivinadas(self):
        """Verifica si todas las letras de la palabra han sido adivinadas.

        Returns:
            bool: True si la palabra completa ha sido adivinada.
        """
        for letra in self.palabra_objetivo:
            if letra not in self.letras_adivinadas:
                return False
        return True

    def palabra_mostrar(self):
        """Devuelve la palabra con letras adivinadas reveladas y guiones para las demás.

        Returns:
            str: Cadena con la palabra mostrando letras adivinadas y '_' para las desconocidas.
        """
        resultado = []
        for letra in self.palabra_objetivo:
            if letra in self.letras_adivinadas:
                resultado.append(letra)
            else:
                resultado.append("_")
        return " ".join(resultado)