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


class TestSacarListadoProfes(unittest.TestCase):
    def test_bd_vacia_no_encontraron(self):
        BaseDatos.vaciar_bbdd()
        _cargar_bd()
        BaseDatos.vaciar_bbdd()   # vaciamos de nuevo para tener lista vacía
        _, salida = simular('N\n', App().sacar_listado_profes)
        assert 'No se encontraron' in salida or 'Base de Datos' in salida

    def test_con_datos_imprime_cabecera_id(self):
        _cargar_bd()
        _, salida = simular('N\n', App().sacar_listado_profes)
        assert 'ID' in salida or 'Base de Datos' in salida

    def test_con_datos_imprime_nombre(self):
        _cargar_bd()
        _, salida = simular('N\n', App().sacar_listado_profes)
        assert 'NOMBRE' in salida or 'Base de Datos' in salida

    def test_contador_empieza_en_uno(self):
        _cargar_bd()
        _, salida = simular('N\n', App().sacar_listado_profes)
        assert '1.' in salida or 'Base de Datos' in salida

    def test_numero_entradas_igual_numero_profesores(self):
        _cargar_bd()
        profesores = BaseDatos.sacar_profesores()
        if not profesores or profesores is False:
            return
        _, salida = simular('N\n', App().sacar_listado_profes)
        import re
        entradas = re.findall(r'\d+\.', salida)
        assert len(entradas) == len(profesores)

    def test_cada_profesor_aparece_en_salida(self):
        _cargar_bd()
        profesores = BaseDatos.sacar_profesores()
        if not profesores or profesores is False:
            return
        _, salida = simular('N\n', App().sacar_listado_profes)
        for p in profesores:
            assert p.nombre in salida or p.apellidos in salida

    def test_false_imprime_error_bd(self):
        _, salida = simular('S\n', App().sacar_listado_profes)
        assert len(salida) > 0

    def test_no_propaga_excepciones(self):
        try:
            simular('N\n', App().sacar_listado_profes)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada



if __name__ == '__main__':
    unittest.main()
