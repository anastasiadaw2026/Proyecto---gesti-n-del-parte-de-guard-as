import unittest

from app.app import App
from tests.tests_app.helpers_app import simular, reset


class TestGestionarFalloAutentificacion(unittest.TestCase):
    def test_imprime_mensaje_credenciales_incorrectas(self):
        _, salida = simular('S\n', App().gestionar_fallo_autentificacion)
        assert 'incorrectas' in salida or 'clave' in salida.lower()

    def test_imprime_opciones_s_y_n(self):
        _, salida = simular('S\n', App().gestionar_fallo_autentificacion)
        assert 'S' in salida and 'N' in salida

    def test_imprime_separador(self):
        _, salida = simular('S\n', App().gestionar_fallo_autentificacion)
        assert '·' in salida

    def test_opcion_s_no_sale(self):
        reset()
        simular('S\n', App().gestionar_fallo_autentificacion)
        assert App.fin is False

    def test_opcion_s_minuscula_no_sale(self):
        reset()
        simular('s\n', App().gestionar_fallo_autentificacion)
        assert App.fin is False

    def test_opcion_n_llama_salir(self):
        reset()
        simular('N\n', App().gestionar_fallo_autentificacion)
        assert App.fin is True

    def test_opcion_n_minuscula_llama_salir(self):
        reset()
        simular('n\n', App().gestionar_fallo_autentificacion)
        assert App.fin is True

    def test_opcion_invalida_redirige_a_gestionar_entrada(self):
        reset()
        simular('X\n2\n', App().gestionar_fallo_autentificacion)
        assert App.fin is True

    def test_no_propaga_excepciones_s(self):
        try:
            simular('S\n', App().gestionar_fallo_autentificacion)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_n(self):
        try:
            simular('N\n', App().gestionar_fallo_autentificacion)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
