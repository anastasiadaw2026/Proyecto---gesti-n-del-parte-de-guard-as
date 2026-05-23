import unittest
import datetime


from lib.guardia import Guardia
from lib.profesor import Profesor
from recursos_externos.bbdd.base_datos import BaseDatos


def _cargar_bd():
    if not BaseDatos.vaciar_bbdd():
        return False
    return BaseDatos.cargar_tablas()


def _insertar_guardia_prueba(cursor, id_prof, dia, hora, curso, aula,
                              tarea='Tarea de prueba', ficheros=''):
    from claves.conexion_bbdd import conexion
    sql = (
        "INSERT INTO guardias (id, dia, hora, curso, aula, tarea, ficheros) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(sql, (id_prof, dia, hora, curso, aula, tarea, ficheros))
    conexion.commit()


def _datos_guardia_validos():
    profesores = BaseDatos.sacar_profesores()
    horas = BaseDatos.sacar_horas()
    cursos = BaseDatos.sacar_cursos()
    aulas = BaseDatos.sacar_aulas()
    if (not profesores or not horas or not cursos or not aulas or
            profesores is False or horas is False or
            cursos is False or aulas is False):
        return None
    datos = BaseDatos.recoger_info_ficheros()
    if not datos:
        return None
    _, _, _, profs_raw = datos
    if not profs_raw:
        return None
    return (profs_raw[0].id,
            datetime.date.today(),
            horas[0].nombre,
            cursos[0].nombre,
            aulas[0].nombre)



class TestAlmacenarGuardias(unittest.TestCase):
    def _preparar_guardias(self, n=3):
        if not _cargar_bd():
            return None
        params = _datos_guardia_validos()
        if not params:
            return None
        from claves.conexion_bbdd import conexion
        cursor = conexion.cursor()
        try:
            for i in range(n):
                dia = datetime.date.today() + datetime.timedelta(days=i)
                _insertar_guardia_prueba(
                    cursor,
                    params[0], dia, params[2], params[3], params[4],
                    tarea=f'Tarea {i}')
        finally:
            cursor.close()
        return BaseDatos.sacar_las_guardias_existentes()

    def test_devuelve_lista(self):
        guardias = self._preparar_guardias(1)
        if guardias is None:
            return
        assert isinstance(guardias, list), "almacenar_guardias debe devolver list"

    def test_elementos_son_guardia(self):
        guardias = self._preparar_guardias(3)
        if not guardias:
            return
        for g in guardias:
            assert isinstance(g, Guardia), (
                f"Cada elemento debe ser Guardia, encontrado: {type(g)}"
            )

    def test_id_guardia_es_profesor(self):
        guardias = self._preparar_guardias(3)
        if not guardias:
            return
        for g in guardias:
            assert isinstance(g.id, Profesor), (
                f"guardia.id debe ser Profesor, encontrado: {type(g.id)}"
            )

    def test_dia_no_es_none(self):
        guardias = self._preparar_guardias(3)
        if not guardias:
            return
        for g in guardias:
            assert g.dia is not None, "El campo dia de la guardia no debe ser None"

    def test_hora_no_vacia(self):
        guardias = self._preparar_guardias(3)
        if not guardias:
            return
        for g in guardias:
            assert g.hora is not None and g.hora != '', (
                "El campo hora de la guardia no debe ser vacío"
            )

    def test_curso_no_vacio(self):
        guardias = self._preparar_guardias(3)
        if not guardias:
            return
        for g in guardias:
            assert g.curso is not None and g.curso != '', (
                "El campo curso de la guardia no debe ser vacío"
            )

    def test_clase_no_vacia(self):
        guardias = self._preparar_guardias(3)
        if not guardias:
            return
        for g in guardias:
            assert g.clase is not None, (
                "El campo clase de la guardia no debe ser None"
            )

    def test_tarea_no_es_none(self):
        guardias = self._preparar_guardias(3)
        if not guardias:
            return
        for g in guardias:
            assert g.tarea is not None, (
                "El campo tarea de la guardia no debe ser None"
            )

    def test_cantidad_guardias_correcta(self):
        if not _cargar_bd():
            return
        params = _datos_guardia_validos()
        if not params:
            return
        BaseDatos.vaciar_bbdd()
        _cargar_bd()
        from claves.conexion_bbdd import conexion
        cursor = conexion.cursor()
        n = 5
        try:
            for i in range(n):
                dia = datetime.date.today() + datetime.timedelta(days=i)
                _insertar_guardia_prueba(
                    cursor, params[0], dia, params[2], params[3], params[4])
        finally:
            cursor.close()
        guardias = BaseDatos.sacar_las_guardias_existentes()
        if guardias is False:
            return
        assert len(guardias) == n, (
            f"Se insertaron {n} guardias, sacar_las_guardias_existentes devolvió {len(guardias)}"
        )


if __name__ == '__main__':
    unittest.main()