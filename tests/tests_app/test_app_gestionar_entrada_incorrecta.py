import unittest

from app.app import App
from tests.tests_app.helpers_app import simular, reset


class TestGestionarEntradaIncorrecta(unittest.TestCase):
    def test_imprime_menu_error(self):
        _, salida = simular('2\n', App().gestionar_entrada_incorrecta, lambda: None)
        assert 'opción' in salida.lower() or 'incorrecta' in salida.lower() or 'opcion' in salida.lower()

    def test_imprime_separador(self):
        _, salida = simular('2\n', App().gestionar_entrada_incorrecta, lambda: None)
        assert '·' in salida

    def test_opcion_1_llama_funcion(self):
        llamadas = []
        def fn():
            llamadas.append(True)
            return 'resultado'
        retorno, _ = simular('1\n', App().gestionar_entrada_incorrecta, fn)
        assert len(llamadas) == 1
        assert retorno == 'resultado'

    def test_opcion_1_pasa_un_arg(self):
        recibido = []
        def fn(x):
            recibido.append(x)
        simular('1\n', App().gestionar_entrada_incorrecta, fn, 'arg1')
        assert recibido == ['arg1']

    def test_opcion_1_pasa_dos_args(self):
        recibido = []
        def fn(a, b):
            recibido.extend([a, b])
        simular('1\n', App().gestionar_entrada_incorrecta, fn, 'a', 'b')
        assert recibido == ['a', 'b']

    def test_opcion_2_llama_salir(self):
        reset()
        simular('2\n', App().gestionar_entrada_incorrecta, lambda: None)
        assert App.fin is True

    def test_opcion_invalida_recursiona_y_sale(self):
        reset()
        simular('X\n2\n', App().gestionar_entrada_incorrecta, lambda: None)
        assert App.fin is True

    def test_opcion_1_sin_args(self):
        llamadas = []
        def fn():
            llamadas.append(True)
        simular('1\n', App().gestionar_entrada_incorrecta, fn)
        assert len(llamadas) == 1

    def test_no_propaga_excepciones_uno(self):
        try:
            simular('1\n', App().gestionar_entrada_incorrecta, lambda: None)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_dos(self):
        try:
            simular('2\n', App().gestionar_entrada_incorrecta, lambda: None)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
