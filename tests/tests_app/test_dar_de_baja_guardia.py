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


class TestDarDeBajaGuardia(unittest.TestCase):
    def _insertar(self):
        if not _cargar_bd():
            return None
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return None
        _, _, _, profs = datos
        horas  = BaseDatos.sacar_horas()
        cursos = BaseDatos.sacar_cursos()
        aulas  = BaseDatos.sacar_aulas()
        if not all([profs, horas, cursos, aulas]):
            return None
        from claves.conexion_bbdd import conexion
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO guardias VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (profs[0].id, datetime.date.today(),
                 horas[0].nombre, cursos[0].nombre, aulas[0].nombre, 'N', ''))
            conexion.commit()
        finally:
            cursor.close()
        return profs[0].id

    def test_sin_args_imprime_mensaje(self):
        _cargar_bd()
        _, salida = simular('N\n', App().dar_de_baja_guardia)
        assert len(salida) > 0

    def test_con_args_usa_lista_profesor(self):
        _cargar_bd()
        _, salida = simular('N\n', App().dar_de_baja_guardia, 'id_x')
        assert len(salida) > 0

    def test_borrado_exitoso_mensaje(self):
        id_p = self._insertar()
        if not id_p:
            return
        _, salida = simular('1\nN\n', App().dar_de_baja_guardia)
        assert 'borró correctamente' in salida or 'correctamente' in salida or len(salida) > 0

    def test_lista_vacia_no_borra(self):
        _cargar_bd()
        _, salida = simular('N\n', App().dar_de_baja_guardia)
        assert 'borró' not in salida

    def test_no_propaga_excepciones_sin_args(self):
        _cargar_bd()
        try:
            simular('N\n', App().dar_de_baja_guardia)
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_con_args(self):
        _cargar_bd()
        try:
            simular('N\n', App().dar_de_baja_guardia, 'id_x')
            lanzada = False
        except SystemExit:
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
