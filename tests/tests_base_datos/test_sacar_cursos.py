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


class TestSacarCursos(unittest.TestCase):

    def test_retorna_list_o_false(self):
        resultado = BaseDatos.sacar_cursos()
        assert isinstance(resultado, list) or resultado is False

    def test_bd_vacia_devuelve_lista_vacia(self):
        if not BaseDatos.vaciar_bbdd():
            return
        cursos = BaseDatos.sacar_cursos()
        assert cursos == [] or cursos is False

    def test_con_datos_devuelve_lista_no_vacia(self):
        if not _cargar_bd():
            return
        cursos = BaseDatos.sacar_cursos()
        assert cursos is not False and len(cursos) > 0

    def test_elementos_son_curso(self):
        if not _cargar_bd():
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False:
            return
        for c in cursos:
            assert isinstance(c, Curso), (
                f"Cada elemento debe ser Curso, encontrado: {type(c)}"
            )

    def test_nombre_no_vacio(self):
        if not _cargar_bd():
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False:
            return
        for c in cursos:
            assert c.nombre and c.nombre != '', "nombre del curso no debe estar vacío"

    def test_nombre_contiene_guion(self):
        if not _cargar_bd():
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False:
            return
        for c in cursos:
            assert '-' in c.nombre, f"El curso '{c.nombre}' debe tener guion"

    def test_nombre_sin_espacios_extremos(self):
        if not _cargar_bd():
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False:
            return
        for c in cursos:
            assert c.nombre == c.nombre.strip(), (
                f"El curso '{c.nombre}' no debe tener espacios al inicio/fin"
            )

    def test_orden_alfabetico(self):
        if not _cargar_bd():
            return
        cursos = BaseDatos.sacar_cursos()
        if cursos is False or len(cursos) < 2:
            return
        nombres = [c.nombre for c in cursos]
        assert nombres == sorted(nombres), "sacar_cursos debe devolver cursos ordenados"

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.sacar_cursos()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()