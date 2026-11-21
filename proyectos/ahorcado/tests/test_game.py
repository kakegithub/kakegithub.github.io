"""Tests de la lógica del juego del ahorcado.

Ejecutar con: pytest tests/ -v
"""

import pytest

from game import Ahorcado


class TestValidacionDeEntrada:
    """Validación de datos en los límites de la API."""

    def test_rechaza_lista_de_palabras_vacia(self):
        with pytest.raises(ValueError, match="palabras"):
            Ahorcado(palabras=[])

    def test_rechaza_letra_vacia(self):
        juego = Ahorcado(palabras=["python"])
        resultado = juego.adivinar_letra("")

        assert resultado is None
        assert juego.letras_adivinadas == set()
        assert juego.letras_incorrectas == set()
        assert juego.intentos_restantes == 6

    def test_rechaza_multiple_caracter(self):
        juego = Ahorcado(palabras=["python"])
        resultado = juego.adivinar_letra("ab")

        assert resultado is None
        assert juego.intentos_restantes == 6


class TestEstadoDelJuego:
    """Comportamiento una vez terminada la partida."""

    def test_no_acepta_adivinanzas_despues_de_perder(self):
        juego = Ahorcado(palabras=["python"])
        for letra in "zxqwvb":
            juego.adivinar_letra(letra)

        assert juego.juego_activo is False
        assert juego.intentos_restantes == 0

        juego.adivinar_letra("k")

        assert juego.intentos_restantes == 0
        assert "k" not in juego.letras_incorrectas

    def test_no_acepta_adivinanzas_despues_de_ganar(self):
        juego = Ahorcado(palabras=["sol"])
        for letra in "sol":
            juego.adivinar_letra(letra)

        assert juego.todas_letras_adivinadas() is True
        juego.adivinar_letra("x")

        assert juego.intentos_restantes == 6
        assert "x" not in juego.letras_incorrectas


class TestReglasBasicas:
    """Regresión de la lógica original."""

    def test_letra_correcta_revela_y_no_consume_intento(self):
        juego = Ahorcado(palabras=["test"])
        assert juego.adivinar_letra("t") is True
        assert juego.palabra_mostrar() == "t _ _ t"
        assert juego.intentos_restantes == 6

    def test_letra_incorrecta_consume_intento(self):
        juego = Ahorcado(palabras=["test"])
        assert juego.adivinar_letra("x") is False
        assert juego.intentos_restantes == 5
        assert "x" in juego.letras_incorrectas

    def test_letra_repetida_no_consume_intento(self):
        juego = Ahorcado(palabras=["test"])
        juego.adivinar_letra("t")
        assert juego.adivinar_letra("t") is None
        assert juego.intentos_restantes == 6

    def test_ganar_despues_de_ultima_letra(self):
        juego = Ahorcado(palabras=["test"])
        for letra in "test":
            juego.adivinar_letra(letra)
        assert juego.juego_activo is False
        assert juego.todas_letras_adivinadas() is True

    def test_nuevo_juego_reinicia_estado(self):
        juego = Ahorcado(palabras=["test"])
        juego.adivinar_letra("x")
        juego.nuevo_juego()
        assert juego.intentos_restantes == 6
        assert juego.letras_adivinadas == set()
        assert juego.letras_incorrectas == set()
        assert juego.juego_activo is True


class TestSeleccionDePalabra:
    """Evitar repeticiones consecutivas."""

    def test_no_repite_palabra_consecutiva(self):
        juego = Ahorcado(palabras=["sol", "mar"])
        palabras = []
        for _ in range(20):
            juego.nuevo_juego()
            palabras.append(juego.palabra_objetivo)

        for anterior, actual in zip(palabras, palabras[1:]):
            assert anterior != actual
