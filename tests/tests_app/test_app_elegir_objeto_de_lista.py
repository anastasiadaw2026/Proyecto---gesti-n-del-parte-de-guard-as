import unittest

from app.app import App
from tests.tests_app.helpers_app import simular, reset


class TestElegirObjetoDeLista(unittest.TestCase):
    LISTA = ['elem_1', 'elem_2', 'elem_3']

    def test_elige_primero(self):
        retorno, _ = simular('1\n', App().elegir_objeto_de_lista, self.LISTA)
        assert retorno == 'elem_1'

    def test_elige_ultimo(self):
        retorno, _ = simular('3\n', App().elegir_objeto_de_lista, self.LISTA)
        assert retorno == 'elem_3'

    def test_elige_medio(self):
        retorno, _ = simular('2\n', App().elegir_objeto_de_lista, self.LISTA)
        assert retorno == 'elem_2'

    def test_imprime_todos_los_elementos(self):
        _, salida = simular('1\n', App().elegir_objeto_de_lista, self.LISTA)
        for elem in self.LISTA:
            assert elem in salida

    def test_imprime_numeros_correlativos(self):
        _, salida = simular('1\n', App().elegir_objeto_de_lista, self.LISTA)
        assert '1.' in salida
        assert '2.' in salida
        assert '3.' in salida

    def test_cinco_elementos_todos_aparecen(self):
        lista = [f'obj_{i}' for i in range(1, 6)]
        _, salida = simular('1\n', App().elegir_objeto_de_lista, lista)
        for obj in lista:
            assert obj in salida, f"'{obj}' debe aparecer en la salida"

    def test_imprime_separador_de_guiones(self):
        _, salida = simular('1\n', App().elegir_objeto_de_lista, self.LISTA)
        assert '----------' in salida

    def test_lista_un_elemento_solo_numero_uno(self):
        _, salida = simular('1\n', App().elegir_objeto_de_lista, ['único'])
        assert '1.' in salida
        assert '2.' not in salida

    def test_numero_fuera_de_rango_no_propaga(self):
        try:
            simular('99\n2\n', App().elegir_objeto_de_lista, self.LISTA)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_input_no_entero_no_propaga(self):
        try:
            simular('xyz\n2\n', App().elegir_objeto_de_lista, self.LISTA)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_lista_vacia_imprime_no_hay_opciones(self):
        _, salida = simular('N\n', App().elegir_objeto_de_lista, [])
        assert 'No hay opciones disponibles' in salida

    def test_lista_vacia_opcion_n_llama_salir(self):
        reset()
        simular('N\n', App().elegir_objeto_de_lista, [])
        assert App.fin is True

    def test_false_va_a_gestionar_error_bbdd(self):
        retorno, salida = simular('S\n', App().elegir_objeto_de_lista, False)
        assert 'Base de Datos' in salida or retorno is False

    def test_retorno_es_mismo_objeto(self):
        obj = object()
        retorno, _ = simular('1\n', App().elegir_objeto_de_lista, [obj])
        assert retorno is obj

    def test_imprime_separador_principal(self):
        _, salida = simular('1\n', App().elegir_objeto_de_lista, self.LISTA)
        assert '·' in salida


if __name__ == '__main__':
    unittest.main()
