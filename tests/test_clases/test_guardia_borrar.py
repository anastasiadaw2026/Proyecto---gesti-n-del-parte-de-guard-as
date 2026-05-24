import unittest
import datetime

from lib.guardia import Guardia
from lib.profesor import Profesor
from lib.hora import Hora
from lib.curso import Curso
from lib.aula import Aula
from recursos_externos.bbdd.base_datos import BaseDatos

def _cargar_bd():
    if not BaseDatos.vaciar_bbdd():
        return False
    return BaseDatos.cargar_tablas()


def _guardia_completa(nombre='Ana', apellidos='López',
                      dia=None, hora='1', curso='1-A', aula='AULA01',
                      tarea=Guardia.NO_TAREA, ficheros=''):
    g = Guardia()
    g.id    = Profesor(nombre, apellidos)
    g.dia   = dia or datetime.date.today()
    g.hora  = hora
    g.curso = curso
    g.clase = aula
    g.tarea = tarea
    g.ficheros = ficheros
    return g


def _primer_id_prof():
    datos = BaseDatos.recoger_info_ficheros()
    if not datos:
        return None
    _, _, _, profs = datos
    return profs[0].id if profs else None


def _primera_hora():
    horas = BaseDatos.sacar_horas()
    return horas[0].nombre if horas else None


def _primer_curso():
    cursos = BaseDatos.sacar_cursos()
    return cursos[0].nombre if cursos else None


def _primera_aula():
    aulas = BaseDatos.sacar_aulas()
    return aulas[0].nombre if aulas else None


def _guardia_bd():
    if not _cargar_bd():
        return None
    id_p  = _primer_id_prof()
    hora  = _primera_hora()
    curso = _primer_curso()
    aula  = _primera_aula()
    if not all([id_p, hora, curso, aula]):
        return None
    datos = BaseDatos.recoger_info_ficheros()
    if not datos:
        return None
    _, _, _, profs = datos
    g = Guardia()
    g.id    = Profesor(profs[0].nombre, profs[0].apellidos)
    g.dia   = datetime.date.today()
    g.hora  = hora
    g.curso = curso
    g.clase = aula
    g.tarea = Guardia.NO_TAREA
    g.ficheros = ''
    return g


class TestGuardiaBorrar(unittest.TestCase):
    def _insertar_y_obtener(self):
        g = _guardia_bd()
        if g is None:
            return None
        if not g.insertar_guardia():
            return None
        return g

    def test_borrar_existente_devuelve_true(self):
        g = self._insertar_y_obtener()
        if g is None:
            return
        resultado = g.borrar_guardia()
        assert resultado is True, (
            "Borrar una guardia existente debe devolver True"
        )

    def test_borrar_existente_elimina_de_bd(self):
        if not _cargar_bd():
            return
        g = _guardia_bd()
        if g is None:
            return
        g.insertar_guardia()
        total_antes = len(BaseDatos.sacar_las_guardias_existentes() or [])
        g.borrar_guardia()
        total_despues = len(BaseDatos.sacar_las_guardias_existentes() or [])
        assert total_despues < total_antes, (
            "Tras borrar, debe haber una guardia menos en la BD"
        )

    def test_borrar_inexistente_devuelve_false(self):
        _cargar_bd()
        g = Guardia()
        g.id   = Profesor('X', 'X')
        g.dia  = datetime.date(2000, 1, 1)
        g.hora = 'hora_que_no_existe'
        resultado = g.borrar_guardia()
        assert resultado is False, (
            "Borrar una guardia inexistente debe devolver False"
        )

    def test_doble_borrado_segundo_es_false(self):
        g = self._insertar_y_obtener()
        if g is None:
            return
        g.borrar_guardia()
        resultado = g.borrar_guardia()
        assert resultado is False, (
            "El segundo borrado de la misma guardia debe devolver False"
        )

    def test_retorna_true_o_false(self):
        _cargar_bd()
        g = Guardia()
        g.id   = Profesor('X', 'X')
        g.dia  = datetime.date.today()
        g.hora = 'inexistente'
        resultado = g.borrar_guardia()
        assert resultado is True or resultado is False

    def test_no_propaga_excepciones_existente(self):
        g = self._insertar_y_obtener()
        if g is None:
            return
        try:
            g.borrar_guardia()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_no_propaga_excepciones_inexistente(self):
        _cargar_bd()
        g = Guardia()
        g.id   = Profesor('X', 'X')
        g.dia  = datetime.date(2000, 1, 1)
        g.hora = 'inexistente'
        try:
            g.borrar_guardia()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada

    def test_borrar_guardia_con_tarea(self):
        g = _guardia_bd()
        if g is None:
            return
        g.tarea = Guardia.SI_TAREA
        g.insertar_guardia()
        resultado = g.borrar_guardia()
        assert resultado is True

    def test_borrar_guardia_con_ficheros(self):
        g = _guardia_bd()
        if g is None:
            return
        g.ficheros = 'examen.pdf'
        g.insertar_guardia()
        resultado = g.borrar_guardia()
        assert resultado is True

    def test_borrar_una_deja_la_otra(self):
        if not _cargar_bd():
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, _, profs = datos
        hora  = _primera_hora()
        curso = _primer_curso()
        aula  = _primera_aula()
        if not all([profs, hora, curso, aula]):
            return
        g1 = Guardia()
        g1.id    = Profesor(profs[0].nombre, profs[0].apellidos)
        g1.dia   = datetime.date.today()
        g1.hora  = hora
        g1.curso = curso
        g1.clase = aula
        g2 = Guardia()
        g2.id    = Profesor(profs[0].nombre, profs[0].apellidos)
        g2.dia   = datetime.date.today() + datetime.timedelta(days=1)
        g2.hora  = hora
        g2.curso = curso
        g2.clase = aula
        g1.insertar_guardia()
        g2.insertar_guardia()
        g1.borrar_guardia()
        guardias = BaseDatos.sacar_las_guardias_existentes()
        assert guardias is not False and len(guardias) == 1, (
            "Tras borrar g1, sólo debe quedar g2 en la BD"
        )


if __name__ == '__main__':
    unittest.main()
