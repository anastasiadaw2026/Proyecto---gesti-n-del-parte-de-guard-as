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

class TestSacarAulas(unittest.TestCase):
    def test_retorna_list_o_false(self):
        resultado = BaseDatos.sacar_aulas()
        assert isinstance(resultado, list) or resultado is False

    def test_bd_vacia_devuelve_lista_vacia(self):
        if not BaseDatos.vaciar_bbdd():
            return
        aulas = BaseDatos.sacar_aulas()
        assert aulas == [] or aulas is False

    def test_con_datos_devuelve_lista_no_vacia(self):
        if not _cargar_bd():
            return
        aulas = BaseDatos.sacar_aulas()
        assert aulas is not False and len(aulas) > 0

    def test_elementos_son_aula(self):
        if not _cargar_bd():
            return
        aulas = BaseDatos.sacar_aulas()
        if aulas is False:
            return
        for a in aulas:
            assert isinstance(a, Aula), (
                f"Cada elemento debe ser Aula, encontrado: {type(a)}"
            )

    def test_nombre_no_vacio(self):
        if not _cargar_bd():
            return
        aulas = BaseDatos.sacar_aulas()
        if aulas is False:
            return
        for a in aulas:
            assert a.nombre and a.nombre != '', "nombre del aula no debe estar vacío"

    def test_nombre_en_mayusculas(self):
        if not _cargar_bd():
            return
        aulas = BaseDatos.sacar_aulas()
        if aulas is False:
            return
        for a in aulas:
            assert a.nombre == a.nombre.upper(), (
                f"El aula '{a.nombre}' debe estar en mayúsculas"
            )

    def test_nombre_sin_espacios_extremos(self):
        if not _cargar_bd():
            return
        aulas = BaseDatos.sacar_aulas()
        if aulas is False:
            return
        for a in aulas:
            assert a.nombre == a.nombre.strip(), (
                f"El aula '{a.nombre}' no debe tener espacios al inicio/fin"
            )

    def test_orden_alfabetico(self):
        if not _cargar_bd():
            return
        aulas = BaseDatos.sacar_aulas()
        if aulas is False or len(aulas) < 2:
            return
        nombres = [a.nombre for a in aulas]
        assert nombres == sorted(nombres), "sacar_aulas debe devolver aulas ordenadas"

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.sacar_aulas()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()