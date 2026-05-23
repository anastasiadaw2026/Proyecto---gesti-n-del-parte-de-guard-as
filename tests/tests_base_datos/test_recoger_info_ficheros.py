import unittest
import os

from lib.profesor import Profesor
from recursos_externos.bbdd.base_datos import BaseDatos


class TestRecogerInfoFicheros(unittest.TestCase):
    FICHERO_CURSOS = '../recursos_externos/ficheros/cursos.csv'
    FICHERO_AULAS = '../recursos_externos/ficheros/aulas.txt'
    FICHERO_HORAS = '../recursos_externos/ficheros/horas.txt'
    FICHERO_PROFESORES = '../recursos_externos/ficheros/profesores.csv'

    def _ficheros_disponibles(self):
        return all(os.path.isfile(f) for f in [
            self.FICHERO_CURSOS,
            self.FICHERO_AULAS,
            self.FICHERO_HORAS,
            self.FICHERO_PROFESORES,
        ])

    def test_fallo_devuelve_false_si_ficheros_ausentes(self):
        if self._ficheros_disponibles():
            return  # skip si hay ficheros
        resultado = BaseDatos.recoger_info_ficheros()
        assert resultado is False, (
            "Si los ficheros no existen, recoger_info_ficheros debe devolver False"
        )

    def test_exito_devuelve_tupla_de_cuatro_listas(self):
        if not self._ficheros_disponibles():
            return
        resultado = BaseDatos.recoger_info_ficheros()
        assert isinstance(resultado, tuple), "Debe devolver una tupla"
        assert len(resultado) == 4, "La tupla debe tener 4 elementos"
        cursos, aulas, horas, profesores = resultado
        assert isinstance(cursos, list), "cursos debe ser list"
        assert isinstance(aulas, list), "aulas debe ser list"
        assert isinstance(horas, list), "horas debe ser list"
        assert isinstance(profesores, list), "profesores debe ser list"

    def test_cursos_no_vacio(self):
        if not self._ficheros_disponibles():
            return
        cursos, _, _, _ = BaseDatos.recoger_info_ficheros()
        assert len(cursos) > 0, "La lista de cursos no debe estar vacía"

    def test_cursos_contiene_strings(self):
        if not self._ficheros_disponibles():
            return
        cursos, _, _, _ = BaseDatos.recoger_info_ficheros()
        for c in cursos:
            assert isinstance(c, str), f"Cada curso debe ser str, encontrado: {type(c)}"

    def test_cursos_con_formato_ciclo_letra(self):
        if not self._ficheros_disponibles():
            return
        cursos, _, _, _ = BaseDatos.recoger_info_ficheros()
        for c in cursos:
            assert '-' in c, f"El curso '{c}' debe contener '-'"

    def test_cursos_sin_espacios_extremos(self):
        if not self._ficheros_disponibles():
            return
        cursos, _, _, _ = BaseDatos.recoger_info_ficheros()
        for c in cursos:
            assert c == c.strip(), f"El curso '{c}' no debe tener espacios al inicio/fin"

    def test_cursos_no_contienen_saltos_de_linea(self):
        if not self._ficheros_disponibles():
            return
        cursos, _, _, _ = BaseDatos.recoger_info_ficheros()
        for c in cursos:
            assert '\n' not in c, f"El curso '{c}' no debe contener saltos de línea"

    def test_cursos_no_hay_duplicados(self):
        if not self._ficheros_disponibles():
            return
        cursos, _, _, _ = BaseDatos.recoger_info_ficheros()
        assert len(cursos) == len(set(cursos)), "No debe haber cursos duplicados"

    def test_aulas_no_vacio(self):
        if not self._ficheros_disponibles():
            return
        _, aulas, _, _ = BaseDatos.recoger_info_ficheros()
        assert len(aulas) > 0, "La lista de aulas no debe estar vacía"

    def test_aulas_contiene_strings(self):
        if not self._ficheros_disponibles():
            return
        _, aulas, _, _ = BaseDatos.recoger_info_ficheros()
        for a in aulas:
            assert isinstance(a, str), f"Cada aula debe ser str, encontrado: {type(a)}"

    def test_aulas_en_mayusculas(self):
        if not self._ficheros_disponibles():
            return
        _, aulas, _, _ = BaseDatos.recoger_info_ficheros()
        for a in aulas:
            assert a == a.upper(), f"El aula '{a}' debe estar en mayúsculas"

    def test_aulas_sin_espacios_extremos(self):
        if not self._ficheros_disponibles():
            return
        _, aulas, _, _ = BaseDatos.recoger_info_ficheros()
        for a in aulas:
            assert a == a.strip(), f"El aula '{a}' no debe tener espacios al inicio/fin"

    def test_aulas_no_contienen_saltos_de_linea(self):
        if not self._ficheros_disponibles():
            return
        _, aulas, _, _ = BaseDatos.recoger_info_ficheros()
        for a in aulas:
            assert '\n' not in a, f"El aula '{a}' no debe contener saltos de línea"

    def test_horas_no_vacio(self):
        if not self._ficheros_disponibles():
            return
        _, _, horas, _ = BaseDatos.recoger_info_ficheros()
        assert len(horas) > 0, "La lista de horas no debe estar vacía"

    def test_horas_contiene_strings(self):
        if not self._ficheros_disponibles():
            return
        _, _, horas, _ = BaseDatos.recoger_info_ficheros()
        for h in horas:
            assert isinstance(h, str), f"Cada hora debe ser str, encontrado: {type(h)}"

    def test_horas_sin_espacios_extremos(self):
        if not self._ficheros_disponibles():
            return
        _, _, horas, _ = BaseDatos.recoger_info_ficheros()
        for h in horas:
            assert h == h.strip(), f"La hora '{h}' no debe tener espacios al inicio/fin"

    def test_horas_no_contienen_saltos_de_linea(self):
        if not self._ficheros_disponibles():
            return
        _, _, horas, _ = BaseDatos.recoger_info_ficheros()
        for h in horas:
            assert '\n' not in h, f"La hora '{h}' no debe contener saltos de línea"

    def test_horas_no_contienen_comas(self):
        if not self._ficheros_disponibles():
            return
        _, _, horas, _ = BaseDatos.recoger_info_ficheros()
        for h in horas:
            assert ',' not in h, f"La hora '{h}' no debe contener comas"

    def test_profesores_no_vacio(self):
        if not self._ficheros_disponibles():
            return
        _, _, _, profesores = BaseDatos.recoger_info_ficheros()
        assert len(profesores) > 0, "La lista de profesores no debe estar vacía"

    def test_profesores_son_instancias_de_profesor(self):
        if not self._ficheros_disponibles():
            return
        _, _, _, profesores = BaseDatos.recoger_info_ficheros()
        for p in profesores:
            assert isinstance(p, Profesor), (
                f"Cada elemento debe ser Profesor, encontrado: {type(p)}"
            )

    def test_profesores_tienen_id_no_vacio(self):
        if not self._ficheros_disponibles():
            return
        _, _, _, profesores = BaseDatos.recoger_info_ficheros()
        for p in profesores:
            assert p.id is not None and p.id != '', (
                f"El profesor debe tener id no vacío"
            )

    def test_profesores_tienen_nombre_no_vacio(self):
        if not self._ficheros_disponibles():
            return
        _, _, _, profesores = BaseDatos.recoger_info_ficheros()
        for p in profesores:
            assert p.nombre is not None and str(p.nombre) != '', (
                "El profesor debe tener nombre no vacío"
            )

    def test_profesores_clave_encriptada_no_vacia(self):
        if not self._ficheros_disponibles():
            return
        _, _, _, profesores = BaseDatos.recoger_info_ficheros()
        for p in profesores:
            assert p.clave_encriptada is not None and p.clave_encriptada != '', (
                "La clave encriptada del profesor no debe estar vacía"
            )

    def test_profesores_clave_encriptada_empieza_con_bcrypt_prefix(self):
        if not self._ficheros_disponibles():
            return
        _, _, _, profesores = BaseDatos.recoger_info_ficheros()
        for p in profesores:
            clave = p.clave_encriptada
            assert clave.startswith('$2b$') or clave.startswith('$2a$'), (
                f"El hash bcrypt de '{p.id}' debe empezar con '$2b$' o '$2a$'"
            )

    def test_profesores_salto_de_cabecera(self):
        if not self._ficheros_disponibles():
            return
        _, _, _, profesores = BaseDatos.recoger_info_ficheros()
        ids = [p.id for p in profesores]
        assert 'id' not in ids and 'ID' not in ids, (
            "La fila de cabecera del CSV de profesores no debe incluirse"
        )

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.recoger_info_ficheros()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada, (
            "recoger_info_ficheros no debe propagar excepciones"
        )


if __name__ == '__main__':
    unittest.main()
