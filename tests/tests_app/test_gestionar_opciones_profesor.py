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


class TestGestionarOpcionesProfesor(unittest.TestCase):
    def _ej(self, opcion, id_prof='prof_x', extra=''):
        return simular(opcion + '\n' + extra, App().gestionar_opciones_profesor, id_prof)

    def test_imprime_menu_profesor(self):
        _, salida = self._ej('4')
        assert 'guardia' in salida.lower() or 'baja' in salida.lower() or 'Salir' in salida

    def test_opcion_4_sale(self):
        reset()
        self._ej('4')
        assert App.fin is True

    def test_opcion_1_visualiza(self):
        _cargar_bd()
        _, salida = self._ej('1', extra='N\n')
        assert len(salida) > 0

    def test_opcion_invalida_sale(self):
        reset()
        simular('X\n2\n', App().gestionar_opciones_profesor, 'id')
        assert App.fin is True

    def test_no_propaga_excepciones_4(self):
        try:
            self._ej('4')
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_imprime_separador(self):
        _, salida = self._ej('4')
        assert '·' in salida



if __name__ == '__main__':
    unittest.main()
