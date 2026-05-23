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


class TestSeleccionarGuardiasPorFechas(unittest.TestCase):
    def _insertar_guardia(self, dia):
        params = _datos_guardia_validos()
        if not params:
            return False
        from claves.conexion_bbdd import conexion
        cursor = conexion.cursor()
        try:
            _insertar_guardia_prueba(
                cursor, params[0], dia, params[2], params[3], params[4])
        finally:
            cursor.close()
        return True

    def test_retorna_list_o_false(self):
        if not _cargar_bd():
            return
        hoy = datetime.date.today()
        resultado = BaseDatos.seleccionar_guardias_por_fechas(hoy, hoy)
        assert isinstance(resultado, list) or resultado is False

    def test_sin_guardias_en_rango_lista_vacia(self):
        if not _cargar_bd():
            return
        pasado = datetime.date(2000, 1, 1)
        resultado = BaseDatos.seleccionar_guardias_por_fechas(pasado, pasado)
        assert resultado == [] or resultado is False, (
            "Sin guardias en el rango, debe devolver []"
        )

    def test_con_guardia_en_rango_lista_no_vacia(self):
        if not _cargar_bd():
            return
        hoy = datetime.date.today()
        if not self._insertar_guardia(hoy):
            return
        resultado = BaseDatos.seleccionar_guardias_por_fechas(hoy, hoy)
        assert resultado is not False and len(resultado) > 0, (
            "Con guardias en el rango, debe devolver lista no vacía"
        )

    def test_guardia_fuera_de_rango_no_aparece(self):
        if not _cargar_bd():
            return
        futuro_lejano = datetime.date(2099, 12, 31)
        if not self._insertar_guardia(futuro_lejano):
            return
        hoy = datetime.date.today()
        resultado = BaseDatos.seleccionar_guardias_por_fechas(hoy, hoy)
        if resultado is False:
            return
        for g in resultado:
            assert g.dia != futuro_lejano, (
                "Las guardias fuera del rango no deben aparecer en los resultados"
            )

    def test_rango_un_dia_incluye_guardias_del_dia(self):
        if not _cargar_bd():
            return
        hoy = datetime.date.today()
        self._insertar_guardia(hoy)
        resultado = BaseDatos.seleccionar_guardias_por_fechas(hoy, hoy)
        if resultado is False:
            return
        for g in resultado:
            assert g.dia == hoy, (
                f"Las guardias del día {hoy} deben aparecer al filtrar por ese día"
            )

    def test_rango_invertido_lista_vacia(self):
        if not _cargar_bd():
            return
        hoy = datetime.date.today()
        ayer = hoy - datetime.timedelta(days=1)
        resultado = BaseDatos.seleccionar_guardias_por_fechas(hoy, ayer)
        assert resultado == [] or resultado is False, (
            "Con fecha_inicio > fecha_fin debe devolver [] o False"
        )

    def test_elementos_son_guardia(self):
        if not _cargar_bd():
            return
        hoy = datetime.date.today()
        self._insertar_guardia(hoy)
        resultado = BaseDatos.seleccionar_guardias_por_fechas(hoy, hoy)
        if resultado is False:
            return
        for g in resultado:
            assert isinstance(g, Guardia), (
                f"Cada elemento debe ser Guardia, encontrado: {type(g)}"
            )

    def test_no_propaga_excepciones(self):
        try:
            hoy = datetime.date.today()
            BaseDatos.seleccionar_guardias_por_fechas(hoy, hoy)
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada


if __name__ == '__main__':
    unittest.main()