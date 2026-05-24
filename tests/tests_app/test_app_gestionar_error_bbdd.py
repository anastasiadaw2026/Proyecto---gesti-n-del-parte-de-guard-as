import unittest

from app.app import App
from tests.tests_app.helpers_app import simular, reset


class TestGestionarErrorBbdd(unittest.TestCase):
    def test_imprime_mensaje_error_bd(self):
        _, salida = simular('S\n', App().gestionar_error_bbdd)
        assert 'Base de Datos' in salida

    def test_imprime_opciones_n_y_s(self):
        _, salida = simular('S\n', App().gestionar_error_bbdd)
        assert 'N' in salida and 'S' in salida

    def test_opcion_n_llama_salir(self):
        reset()
        simular('N\n', App().gestionar_error_bbdd)
        assert App.fin is True

    def test_opcion_n_minuscula_llama_salir(self):
        reset()
        simular('n\n', App().gestionar_error_bbdd)
        assert App.fin is True

    def test_opcion_s_devuelve_false(self):
        reset()
        retorno, _ = simular('S\n', App().gestionar_error_bbdd)
        assert retorno is False
        assert App.fin is False

    def test_opcion_s_minuscula_devuelve_false(self):
        retorno, _ = simular('s\n', App().gestionar_error_bbdd)
        assert retorno is False

    def test_opcion_invalida_va_a_gestionar_entrada(self):
        reset()
        simular('X\n2\n', App().gestionar_error_bbdd)
        assert App.fin is True

    def test_retorno_s_es_exactamente_false(self):
        retorno, _ = simular('S\n', App().gestionar_error_bbdd)
        assert retorno is False

    def test_no_propaga_excepciones_s(self):
        try:
            simular('S\n', App().gestionar_error_bbdd)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_n(self):
        try:
            simular('N\n', App().gestionar_error_bbdd)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
