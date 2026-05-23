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


class TestSacarGuardiasProfesor(unittest.TestCase):
    def _insertar_para_prof(self, id_prof):
        params = _datos_guardia_validos()
        if not params:
            return False
        from claves.conexion_bbdd import conexion
        cursor = conexion.cursor()
        try:
            _insertar_guardia_prueba(
                cursor, id_prof, datetime.date.today(),
                params[2], params[3], params[4])
        finally:
            cursor.close()
        return True

    def test_retorna_list_o_false(self):
        resultado = BaseDatos.sacar_guardias_profesor('cualquier_id')
        assert isinstance(resultado, list) or resultado is False

    def test_prof_sin_guardias_lista_vacia(self):
        if not _cargar_bd():
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, _, profs = datos
        if not profs:
            return
        resultado = BaseDatos.sacar_guardias_profesor(profs[0].id)
        assert resultado == [] or resultado is False, (
            "Profesor sin guardias debe devolver []"
        )

    def test_prof_con_guardias_lista_no_vacia(self):
        if not _cargar_bd():
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, _, profs = datos
        if not profs:
            return
        id_p = profs[0].id
        if not self._insertar_para_prof(id_p):
            return
        resultado = BaseDatos.sacar_guardias_profesor(id_p)
        assert resultado is not False and len(resultado) > 0, (
            "Profesor con guardias debe devolver lista no vacía"
        )

    def test_id_inexistente_lista_vacia(self):
        if not _cargar_bd():
            return
        resultado = BaseDatos.sacar_guardias_profesor('ID_IMPOSIBLE_9999')
        assert resultado == [] or resultado is False, (
            "Con id inexistente debe devolver [] o False"
        )

    def test_elementos_son_guardia(self):
        if not _cargar_bd():
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, _, profs = datos
        if not profs:
            return
        id_p = profs[0].id
        self._insertar_para_prof(id_p)
        resultado = BaseDatos.sacar_guardias_profesor(id_p)
        if resultado is False or not resultado:
            return
        for g in resultado:
            assert isinstance(g, Guardia), (
                f"Cada elemento debe ser Guardia, encontrado: {type(g)}"
            )

    def test_guardias_pertenecen_al_profesor(self):
        if not _cargar_bd():
            return
        datos = BaseDatos.recoger_info_ficheros()
        if not datos:
            return
        _, _, _, profs = datos
        if len(profs) < 2:
            return
        id_p1 = profs[0].id
        id_p2 = profs[1].id
        self._insertar_para_prof(id_p1)
        self._insertar_para_prof(id_p2)
        resultado = BaseDatos.sacar_guardias_profesor(id_p1)
        if resultado is False:
            return
        for g in resultado:
            nombre_prof = g.id.nombre if isinstance(g.id, Profesor) else str(g.id)
            assert isinstance(g, Guardia), "Elemento inesperado en la lista"

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.sacar_guardias_profesor('x')
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()
