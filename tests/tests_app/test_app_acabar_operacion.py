import unittest
from app.app import App
from tests.tests_app.helpers_app import simular, reset


class TestAcabarOperacion(unittest.TestCase):
    def test_imprime_mensaje_operacion(self):
        _, salida = simular('S\n', App().acabar_operacion)
        assert 'correctamente' in salida or 'Operación' in salida

    def test_imprime_opciones_n_y_s(self):
        _, salida = simular('S\n', App().acabar_operacion)
        assert 'N' in salida and 'S' in salida

    def test_imprime_separador(self):
        _, salida = simular('S\n', App().acabar_operacion)
        assert '·' in salida

    def test_opcion_n_llama_salir(self):
        reset()
        simular('N\n', App().acabar_operacion)
        assert App.fin is True

    def test_opcion_n_minuscula_llama_salir(self):
        reset()
        simular('n\n', App().acabar_operacion)
        assert App.fin is True

    def test_opcion_s_devuelve_none(self):
        reset()
        retorno, _ = simular('S\n', App().acabar_operacion)
        assert retorno is None
        assert App.fin is False

    def test_opcion_s_minuscula_devuelve_none(self):
        retorno, _ = simular('s\n', App().acabar_operacion)
        assert retorno is None

    def test_opcion_invalida_va_a_gestionar_entrada(self):
        reset()
        simular('X\n2\n', App().acabar_operacion)
        assert App.fin is True

    def test_no_propaga_excepciones_s(self):
        try:
            simular('S\n', App().acabar_operacion)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_n(self):
        try:
            simular('N\n', App().acabar_operacion)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
