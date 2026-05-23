import unittest

from lib.profesor import Profesor
from lib.hora import Hora
from lib.curso import Curso
from lib.aula import Aula
from recursos_externos.bbdd.base_datos import BaseDatos


def _cargar_bd():
    if not BaseDatos.vaciar_bbdd():
        return False
    return BaseDatos.cargar_tablas()


class TestSacarProfesores(unittest.TestCase):
    def test_retorna_list_o_false(self):
        resultado = BaseDatos.sacar_profesores()
        assert isinstance(resultado, list) or resultado is False, (
            "sacar_profesores debe devolver list o False"
        )

    def test_bd_vacia_devuelve_lista_vacia(self):
        if not BaseDatos.vaciar_bbdd():
            return
        profesores = BaseDatos.sacar_profesores()
        assert profesores == [] or profesores is False, (
            "Con BD vacía, sacar_profesores debe devolver []"
        )

    def test_con_datos_devuelve_lista_no_vacia(self):
        if not _cargar_bd():
            return
        profesores = BaseDatos.sacar_profesores()
        assert profesores is not False and len(profesores) > 0, (
            "Con datos en BD, sacar_profesores debe devolver lista no vacía"
        )

    def test_elementos_son_profesor(self):
        if not _cargar_bd():
            return
        profesores = BaseDatos.sacar_profesores()
        if profesores is False:
            return
        for p in profesores:
            assert isinstance(p, Profesor), (
                f"Cada elemento debe ser Profesor, encontrado: {type(p)}"
            )

    def test_nombre_no_vacio(self):
        if not _cargar_bd():
            return
        profesores = BaseDatos.sacar_profesores()
        if profesores is False:
            return
        for p in profesores:
            assert p.nombre and str(p.nombre) != '', (
                "El nombre de cada profesor no debe estar vacío"
            )

    def test_apellidos_no_vacio(self):
        if not _cargar_bd():
            return
        profesores = BaseDatos.sacar_profesores()
        if profesores is False:
            return
        for p in profesores:
            assert p.apellidos and str(p.apellidos) != '', (
                "Los apellidos de cada profesor no deben estar vacíos"
            )

    def test_nombre_y_apellidos_son_strings(self):
        if not _cargar_bd():
            return
        profesores = BaseDatos.sacar_profesores()
        if profesores is False:
            return
        for p in profesores:
            assert isinstance(p.nombre, str), "nombre debe ser str"
            assert isinstance(p.apellidos, str), "apellidos debe ser str"

    def test_orden_nombre_apellidos(self):
        if not _cargar_bd():
            return
        profesores = BaseDatos.sacar_profesores()
        if profesores is False or len(profesores) < 2:
            return
        pares = [(p.nombre, p.apellidos) for p in profesores]
        assert pares == sorted(pares), (
            "sacar_profesores debe devolver profesores ordenados por nombre y apellidos"
        )

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.sacar_profesores()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada, "sacar_profesores no debe propagar excepciones"


if __name__ == '__main__':
    unittest.main()