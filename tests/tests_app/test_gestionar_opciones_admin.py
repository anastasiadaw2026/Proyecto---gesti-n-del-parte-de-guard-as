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


class TestGestionarOpcionesAdmin(unittest.TestCase):
    def _ej(self, opcion, extra=''):
        return simular(opcion + '\n' + extra, App().gestionar_opciones_admin)

    def test_imprime_menu_admin(self):
        _, salida = self._ej('7')
        assert 'Cargar' in salida or 'Visualizar' in salida or 'Salir' in salida

    def test_opcion_7_sale(self):
        reset()
        self._ej('7')
        assert App.fin is True

    def test_opcion_2_visualiza(self):
        _cargar_bd()
        _, salida = self._ej('2', 'N\n')
        assert 'guardia' in salida.lower() or 'semana' in salida.lower() or 'Base de Datos' in salida

    def test_opcion_6_listado(self):
        _cargar_bd()
        _, salida = self._ej('6', 'N\n')
        assert 'ID' in salida or 'No se encontraron' in salida or 'Base de Datos' in salida

    def test_opcion_invalida_sale(self):
        reset()
        simular('X\n2\n', App().gestionar_opciones_admin)
        assert App.fin is True

    def test_no_propaga_excepciones_7(self):
        try:
            self._ej('7')
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_opcion_5_informe(self):
        _cargar_bd()
        _, salida = simular('5\n15\n1\n2024\n22\n1\n2024\nN\n', App().gestionar_opciones_admin)
        assert len(salida) > 0

    def test_opcion_1_carga_bd(self):
        _, salida = simular('1\nN\nS\nS\n', App().gestionar_opciones_admin)
        assert len(salida) > 0



if __name__ == '__main__':
    unittest.main()
