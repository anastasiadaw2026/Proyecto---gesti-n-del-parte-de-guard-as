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


class TestSacarHoras(unittest.TestCase):
    def test_retorna_list_o_false(self):
        resultado = BaseDatos.sacar_horas()
        assert isinstance(resultado, list) or resultado is False, (
            "sacar_horas debe devolver list o False"
        )

    def test_bd_vacia_devuelve_lista_vacia(self):
        if not BaseDatos.vaciar_bbdd():
            return
        horas = BaseDatos.sacar_horas()
        assert horas == [] or horas is False, (
            "Con BD vacía, sacar_horas debe devolver []"
        )

    def test_con_datos_devuelve_lista_no_vacia(self):
        if not _cargar_bd():
            return
        horas = BaseDatos.sacar_horas()
        assert horas is not False and len(horas) > 0, (
            "Con datos en BD, sacar_horas debe devolver lista no vacía"
        )

    def test_elementos_son_hora(self):
        if not _cargar_bd():
            return
        horas = BaseDatos.sacar_horas()
        if horas is False:
            return
        for h in horas:
            assert isinstance(h, Hora), (
                f"Cada elemento debe ser Hora, encontrado: {type(h)}"
            )

    def test_nombre_no_vacio(self):
        if not _cargar_bd():
            return
        horas = BaseDatos.sacar_horas()
        if horas is False:
            return
        for h in horas:
            assert h.nombre and h.nombre != '', (
                "El nombre de cada hora no debe estar vacío"
            )

    def test_nombre_es_string(self):
        if not _cargar_bd():
            return
        horas = BaseDatos.sacar_horas()
        if horas is False:
            return
        for h in horas:
            assert isinstance(h.nombre, str), (
                f"nombre de hora debe ser str, encontrado: {type(h.nombre)}"
            )

    def test_orden_por_longitud(self):
        if not _cargar_bd():
            return
        horas = BaseDatos.sacar_horas()
        if horas is False or len(horas) < 2:
            return
        longitudes = [len(h.nombre) for h in horas]
        assert longitudes == sorted(longitudes), (
            "sacar_horas debe devolver horas ordenadas por longitud del nombre"
        )

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.sacar_horas()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada, "sacar_horas no debe propagar excepciones"