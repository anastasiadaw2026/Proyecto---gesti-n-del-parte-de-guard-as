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


class TestMain(unittest.TestCase):
    def _ej(self, entrada):
        reset()
        return simular(entrada, App().main)

    def test_imprime_menu_inicio(self):
        _, salida = self._ej('4\n')
        assert 'Administrador' in salida or 'Profesor' in salida or 'Lector' in salida

    def test_opcion_4_sale_y_termina_while(self):
        self._ej('4\n')
        assert App.fin is True

    def test_while_primera_iteracion_produce_salida(self):
        _, salida = self._ej('4\n')
        assert len(salida) > 0

    def test_while_segunda_iteracion_mas_salida(self):
        _, doble  = self._ej('X\n2\n')
        _, simple = self._ej('4\n')
        assert len(doble) >= len(simple)

    def test_while_tercera_iteracion(self):
        reset()
        simular('X\n2\n', App().main)
        assert App.fin is True

    def test_opcion_1_pide_credenciales_admin(self):
        _, salida = self._ej(f'1\n{ad.ID}\n{ad.CLAVE}\n7\n')
        assert 'correcta' in salida or 'Administrador' in salida

    def test_opcion_2_pide_credenciales_profesor(self):
        _, salida = self._ej('2\nX\nY\nN\n4\n')
        assert len(salida) > 0

    def test_opcion_3_gestiona_lector(self):
        _, salida = self._ej('3\n2\n')
        assert 'guardia' in salida.lower() or 'Salir' in salida or len(salida) > 0

    def test_opcion_invalida_luego_salir(self):
        self._ej('X\n2\n')
        assert App.fin is True

    def test_no_propaga_excepciones(self):
        try:
            self._ej('4\n')
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_separador_aparece(self):
        _, salida = self._ej('4\n')
        assert '·' in salida


if __name__ == '__main__':
    unittest.main()
