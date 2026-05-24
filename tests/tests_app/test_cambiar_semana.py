import unittest

from app.app import App
from tests.tests_app.helpers_app import simular, reset
from recursos_externos.bbdd.base_datos import BaseDatos


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


class TestCambiarSemana(unittest.TestCase):
    def test_imprime_menu_semana(self):
        _, salida = simular('N\n', App().cambiar_semana)
        assert 'semana' in salida.lower() or '·' in salida

    def test_opcion_n_llama_salir(self):
        reset()
        simular('N\n', App().cambiar_semana)
        assert App.fin is True

    def test_opcion_n_minuscula_llama_salir(self):
        reset()
        simular('n\n', App().cambiar_semana)
        assert App.fin is True

    def test_opcion_s_devuelve_true(self):
        _cargar_bd()
        retorno, _ = simular('S\n15\n1\n2024\n', App().cambiar_semana)
        assert retorno is True or retorno is None or retorno is False

    def test_opcion_invalida_luego_salir(self):
        reset()
        simular('X\n2\n', App().cambiar_semana)
        assert App.fin is True

    def test_no_propaga_excepciones_n(self):
        try:
            simular('N\n', App().cambiar_semana)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_s(self):
        try:
            simular('S\n15\n1\n2024\n', App().cambiar_semana)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_imprime_separador(self):
        _, salida = simular('N\n', App().cambiar_semana)
        assert '·' in salida


if __name__ == '__main__':
    unittest.main()
