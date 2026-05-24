import unittest

from app.app import App
from tests.tests_app.helpers_app import simular, reset


class TestComprobarResultadoBackup(unittest.TestCase):
    def test_true_imprime_correctamente(self):
        _, salida = simular('', App().comprobar_resultado_backup, (True, 'ruta/backup.sql'))
        assert 'correctamente' in salida

    def test_true_imprime_ruta(self):
        _, salida = simular('', App().comprobar_resultado_backup, (True, 'ruta/backup.sql'))
        assert 'ruta/backup.sql' in salida

    def test_true_no_pide_input(self):
        lanzada = False
        try:
            simular('', App().comprobar_resultado_backup, (True, 'r.sql'))
            lanzada = False
        except EOFError:
            lanzada = True
        except Exception:
            lanzada = True
        assert not lanzada

    def test_false_imprime_mensaje_error(self):
        _, salida = simular('S\n', App().comprobar_resultado_backup,
                            (False, 'No se pudo realizar la copia.'))
        assert 'No se pudo realizar la copia.' in salida

    def test_false_imprime_opciones_s_n(self):
        _, salida = simular('S\n', App().comprobar_resultado_backup, (False, 'Error'))
        assert 'S' in salida and 'N' in salida

    def test_false_opcion_n_llama_salir(self):
        reset()
        simular('N\n', App().comprobar_resultado_backup, (False, 'Error'))
        assert App.fin is True

    def test_false_opcion_n_minuscula_llama_salir(self):
        reset()
        simular('n\n', App().comprobar_resultado_backup, (False, 'Error'))
        assert App.fin is True

    def test_false_opcion_s_no_sale(self):
        reset()
        simular('S\n', App().comprobar_resultado_backup, (False, 'Error'))
        assert App.fin is False

    def test_false_opcion_invalida_va_a_gestionar_entrada(self):
        reset()
        simular('X\n2\n', App().comprobar_resultado_backup, (False, 'Error'))
        assert App.fin is True

    def test_imprime_separador(self):
        _, salida = simular('S\n', App().comprobar_resultado_backup, (False, 'Error'))
        assert '·' in salida

    def test_no_propaga_excepciones_true(self):
        try:
            simular('', App().comprobar_resultado_backup, (True, 'ruta.sql'))
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_false(self):
        try:
            simular('S\n', App().comprobar_resultado_backup, (False, 'error'))
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
