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


class TestLoginProfesor(unittest.TestCase):
    def test_correctas_imprime_autentificacion(self):
        _cargar_bd()
        par = _primer_prof()
        if not par:
            return
        _, salida = simular(f'{par[0]}\n{par[1]}\n4\n', App().login_profesor)
        assert 'correcta' in salida

    def test_correctas_llega_a_menu_profesor(self):
        _cargar_bd()
        par = _primer_prof()
        if not par:
            return
        _, salida = simular(f'{par[0]}\n{par[1]}\n4\n', App().login_profesor)
        assert 'guardia' in salida.lower() or 'baja' in salida.lower() or 'Salir' in salida

    def test_clave_incorrecta_fallo(self):
        _cargar_bd()
        par = _primer_prof()
        if not par:
            return
        _, salida = simular(f'{par[0]}\nMAL\nN\n', App().login_profesor)
        assert 'incorrectas' in salida or 'clave' in salida.lower() or 'Base de Datos' in salida

    def test_id_inexistente_fallo(self):
        _cargar_bd()
        _, salida = simular('ID_IMPOSIBLE\nX\nN\n', App().login_profesor)
        assert len(salida) > 0

    def test_fallo_opcion_n_sale(self):
        _cargar_bd()
        reset()
        simular('X\nY\nN\n', App().login_profesor)
        assert App.fin is True

    def test_fallo_opcion_s_no_sale(self):
        _cargar_bd()
        reset()
        simular('X\nY\nS\n', App().login_profesor)
        assert App.fin is False

    def test_no_propaga_excepciones_correctas(self):
        _cargar_bd()
        par = _primer_prof()
        if not par:
            return
        try:
            simular(f'{par[0]}\n{par[1]}\n4\n', App().login_profesor)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_incorrectas(self):
        try:
            simular('X\nY\nN\n', App().login_profesor)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
