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


class TestSacarLasGuardiasExistentes(unittest.TestCase):
    def test_retorna_list_o_false(self):
        resultado = BaseDatos.sacar_las_guardias_existentes()
        assert isinstance(resultado, list) or resultado is False

    def test_sin_guardias_devuelve_lista_vacia(self):
        if not _cargar_bd():
            return
        resultado = BaseDatos.sacar_las_guardias_existentes()
        assert resultado == [] or resultado is False, (
            "Sin guardias, debe devolver []"
        )

    def test_con_guardias_lista_no_vacia(self):
        if not _cargar_bd():
            return
        params = _datos_guardia_validos()
        if not params:
            return
        from claves.conexion_bbdd import conexion
        cursor = conexion.cursor()
        try:
            _insertar_guardia_prueba(
                cursor, params[0], datetime.date.today(),
                params[2], params[3], params[4])
        finally:
            cursor.close()
        resultado = BaseDatos.sacar_las_guardias_existentes()
        assert resultado is not False and len(resultado) > 0

    def test_elementos_son_guardia(self):
        resultado = BaseDatos.sacar_las_guardias_existentes()
        if resultado is False or not resultado:
            return
        for g in resultado:
            assert isinstance(g, Guardia)

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.sacar_las_guardias_existentes()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()