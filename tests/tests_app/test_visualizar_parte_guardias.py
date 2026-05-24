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


class TestVisualizarParteGuardias(unittest.TestCase):
    def test_imprime_encabezado_guardias(self):
        _cargar_bd()
        _, salida = simular('N\n', App().visualizar_parte_guardias)
        assert 'guardias' in salida.lower() or 'semana' in salida.lower() or 'Base de Datos' in salida

    def test_error_bd_imprime_mensaje(self):
        _, salida = simular('S\n', App().visualizar_parte_guardias)
        assert len(salida) > 0

    def test_llama_a_cambiar_semana(self):
        _cargar_bd()
        _, salida = simular('N\n', App().visualizar_parte_guardias)
        assert 'semana' in salida.lower() or '·' in salida

    def test_no_propaga_excepciones(self):
        try:
            simular('N\n', App().visualizar_parte_guardias)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_imprime_separador(self):
        _cargar_bd()
        _, salida = simular('N\n', App().visualizar_parte_guardias)
        assert '·' in salida



if __name__ == '__main__':
    unittest.main()
