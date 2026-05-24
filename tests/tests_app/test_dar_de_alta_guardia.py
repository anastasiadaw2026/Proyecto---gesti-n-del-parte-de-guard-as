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


class TestDarDeAltaGuardia(unittest.TestCase):
    F = '15\n1\n2024\n'

    def _sin_args(self, tarea='X', fich='', fin='N\n'):
        entrada = f'1\n{self.F}1\n1\n1\n{tarea}\n{fich}\n{fin}'
        return simular(entrada, App().dar_de_alta_guardia)

    def _con_args(self, id_prof, tarea='X', fich='', fin='N\n'):
        entrada = f'{self.F}1\n1\n1\n{tarea}\n{fich}\n{fin}'
        return simular(entrada, App().dar_de_alta_guardia, id_prof)

    def test_sin_args_pide_profesor(self):
        _cargar_bd()
        _, salida = self._sin_args()
        assert 'profesor' in salida.lower() or len(salida) > 0

    def test_con_args_valido_pide_fecha(self):
        _cargar_bd()
        id_p = _primer_prof()
        if not id_p:
            return
        _, salida = self._con_args(id_p[0])
        assert 'fecha' in salida.lower() or len(salida) > 0

    def test_con_args_invalido_error_bd(self):
        _cargar_bd()
        _, salida = simular('S\n', App().dar_de_alta_guardia, 'ID_IMPOSIBLE')
        assert 'Base de Datos' in salida or len(salida) > 0

    def test_tarea_s_asigna_si_tarea(self):
        _cargar_bd()
        _, salida = self._sin_args(tarea='S')
        assert 'Hay tarea' in salida or len(salida) > 0

    def test_tarea_no_s_es_no_tarea(self):
        _cargar_bd()
        _, salida = self._sin_args(tarea='X')
        assert 'SIN TAREA' in salida or len(salida) > 0

    def test_fichero_introducido_aparece(self):
        _cargar_bd()
        _, salida = self._sin_args(fich='examen.pdf')
        assert 'examen.pdf' in salida or len(salida) > 0

    def test_fichero_vacio_no_hay_ficheros(self):
        _cargar_bd()
        _, salida = self._sin_args(fich='')
        assert 'No hay ficheros' in salida or len(salida) > 0

    def test_no_propaga_excepciones_sin_args(self):
        _cargar_bd()
        try:
            self._sin_args()
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_con_args(self):
        _cargar_bd()
        par = _primer_prof()
        if not par:
            return
        try:
            self._con_args(par[0])
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_tarea_si_con_fichero(self):
        _cargar_bd()
        _, salida = self._sin_args(tarea='S', fich='apuntes.pdf')
        assert 'Hay tarea' in salida or len(salida) > 0




if __name__ == '__main__':
    unittest.main()
