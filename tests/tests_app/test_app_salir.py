import unittest
from app.app import App
from tests.tests_app.helpers_app import reset, simular


class TestSalir(unittest.TestCase):
    def test_lanza_system_exit(self):
        lanzada = False
        try:
            App.salir()
        except SystemExit:
            lanzada = True
        assert lanzada, "salir() debe lanzar SystemExit"

    def test_pone_fin_a_true(self):
        reset()
        try:
            App.salir()
        except SystemExit:
            pass
        assert App.fin is True

    def test_fin_cambia_de_false_a_true(self):
        reset()
        assert App.fin is False
        try:
            App.salir()
        except SystemExit:
            pass
        assert App.fin is True

    def test_imprime_adios(self):
        _, salida = simular('', App.salir)
        assert 'Adiós' in salida

    def test_imprime_separador(self):
        _, salida = simular('', App.salir)
        assert '·' in salida

    def test_es_estatico(self):
        lanzada = False
        try:
            App.salir()
        except SystemExit:
            lanzada = True
        except TypeError:
            assert False, "salir() no debe necesitar instancia"
        assert lanzada

    def test_llamadas_repetidas_lanzan_system_exit(self):
        for _ in range(3):
            reset()
            lanzada = False
            try:
                App.salir()
            except SystemExit:
                lanzada = True
            assert lanzada


if __name__ == '__main__':
    unittest.main()
