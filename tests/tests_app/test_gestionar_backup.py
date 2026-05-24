import unittest
import datetime

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


class TestGestionarBackup(unittest.TestCase):
    def test_imprime_menu_backup(self):
        _, salida = simular('N\nS\n', App().gestionar_backup)
        assert 'backup' in salida.lower() or 'copia' in salida.lower() or 'seguridad' in salida.lower()

    def test_opcion_s_intenta_backup(self):
        _, salida = simular('S\nS\n', App().gestionar_backup)
        assert 'copia' in salida.lower() or 'backup' in salida.lower() or 'correctamente' in salida.lower()

    def test_opcion_n_confirmacion_s_no_hace_backup(self):
        reset()
        simular('N\nS\n', App().gestionar_backup)
        assert App.fin is False

    def test_opcion_n_confirmacion_invalida_vuelve(self):
        _, salida = simular('N\nX\nN\nS\n', App().gestionar_backup)
        assert len(salida) > 0

    def test_opcion_invalida_luego_salir(self):
        reset()
        simular('X\n2\n', App().gestionar_backup)
        assert App.fin is True

    def test_opcion_s_minuscula(self):
        _, salida = simular('s\nS\n', App().gestionar_backup)
        assert len(salida) > 0

    def test_no_propaga_excepciones(self):
        try:
            simular('N\nS\n', App().gestionar_backup)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_imprime_separador(self):
        _, salida = simular('N\nS\n', App().gestionar_backup)
        assert '·' in salida



if __name__ == '__main__':
    unittest.main()
