import datetime
import unittest

from app.app import App
from tests.tests_app.helpers_app import simular, reset
from recursos_externos.bbdd.base_datos import BaseDatos
from claves import claves_admin as ad


def _cargar_bd():
    if not BaseDatos.vaciar_bbdd():
        return False
    return BaseDatos.cargar_tablas()


def _primer_prof():
    datos = BaseDatos.recoger_info_ficheros()
    if not datos:
        return None
    _, _, _, profs = datos
    return (profs[0].id, profs[0].clave) if profs else None


class TestGestionarLector(unittest.TestCase):
    def test_imprime_menu_lector(self):
        _, salida = simular('2\n', App().gestionar_lector)
        assert 'guardia' in salida.lower() or 'Salir' in salida or 'opciones' in salida.lower()

    def test_opcion_2_llama_salir(self):
        reset()
        simular('2\n', App().gestionar_lector)
        assert App.fin is True

    def test_opcion_invalida_luego_salir(self):
        reset()
        simular('X\n2\n', App().gestionar_lector)
        assert App.fin is True

    def test_no_propaga_excepciones(self):
        try:
            simular('2\n', App().gestionar_lector)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_imprime_separador(self):
        _, salida = simular('2\n', App().gestionar_lector)
        assert '·' in salida


if __name__ == '__main__':
    unittest.main()
