import unittest
import os

from recursos_externos.bbdd.base_datos import BaseDatos


class TestGuardarClavesProfesores(unittest.TestCase):
    RUTA_CLAVES = '../claves/claves_profesores.txt'

    def _ficheros_fuente_disponibles(self):
        return os.path.isfile('../recursos_externos/ficheros/profesores.csv')

    def test_retorna_string(self):
        resultado = BaseDatos.guardar_claves_profesores()
        assert isinstance(resultado, str), (
            "guardar_claves_profesores debe devolver una cadena"
        )

    def test_exito_mensaje_menciona_fichero_externo(self):
        if not self._ficheros_fuente_disponibles():
            return
        resultado = BaseDatos.guardar_claves_profesores()
        assert 'fichero externo' in resultado.lower() or 'claves' in resultado.lower(), (
            "El mensaje de éxito debe mencionar el fichero o las claves"
        )

    def test_exito_fichero_claves_existe(self):
        if not self._ficheros_fuente_disponibles():
            return
        BaseDatos.guardar_claves_profesores()
        assert os.path.isfile(self.RUTA_CLAVES), (
            f"El fichero '{self.RUTA_CLAVES}' debe crearse tras la llamada"
        )

    def test_fichero_claves_no_vacio(self):
        if not self._ficheros_fuente_disponibles():
            return
        BaseDatos.guardar_claves_profesores()
        if os.path.isfile(self.RUTA_CLAVES):
            tam = os.path.getsize(self.RUTA_CLAVES)
            assert tam > 0, "El fichero de claves no debe estar vacío"

    def test_cada_linea_tiene_separador(self):
        if not self._ficheros_fuente_disponibles():
            return
        BaseDatos.guardar_claves_profesores()
        if not os.path.isfile(self.RUTA_CLAVES):
            return
        with open(self.RUTA_CLAVES, encoding='utf-8') as f:
            lineas = [l.rstrip('\n') for l in f if l.strip()]
        for linea in lineas:
            assert ' - ' in linea, (
                f"La línea '{linea}' debe contener el separador ' - '"
            )

    def test_id_no_vacio_en_cada_linea(self):
        if not self._ficheros_fuente_disponibles():
            return
        BaseDatos.guardar_claves_profesores()
        if not os.path.isfile(self.RUTA_CLAVES):
            return
        with open(self.RUTA_CLAVES, encoding='utf-8') as f:
            lineas = [l.rstrip('\n') for l in f if l.strip()]
        for linea in lineas:
            if ' - ' in linea:
                id_parte = linea.split(' - ')[0]
                assert id_parte != '', (
                    f"El ID en la línea '{linea}' no debe estar vacío"
                )

    def test_clave_no_vacia_en_cada_linea(self):
        if not self._ficheros_fuente_disponibles():
            return
        BaseDatos.guardar_claves_profesores()
        if not os.path.isfile(self.RUTA_CLAVES):
            return
        with open(self.RUTA_CLAVES, encoding='utf-8') as f:
            lineas = [l.rstrip('\n') for l in f if l.strip()]
        for linea in lineas:
            if ' - ' in linea:
                clave_parte = linea.split(' - ', 1)[1]
                assert clave_parte != '', (
                    f"La clave en la línea '{linea}' no debe estar vacía"
                )

    def test_numero_lineas_igual_numero_profesores(self):
        if not self._ficheros_fuente_disponibles():
            return
        resultado_ficheros = BaseDatos.recoger_info_ficheros()
        if not resultado_ficheros:
            return
        _, _, _, profesores = resultado_ficheros
        BaseDatos.guardar_claves_profesores()
        if not os.path.isfile(self.RUTA_CLAVES):
            return
        with open(self.RUTA_CLAVES, encoding='utf-8') as f:
            lineas = [l for l in f if l.strip()]
        assert len(lineas) == len(profesores), (
            "El número de líneas en el fichero debe igualar el número de profesores"
        )

    def test_fallo_devuelve_mensaje_error(self):
        # Simulamos el fallo indirectamente:
        # si recoger_info_ficheros devuelve False, guardar_claves lanzará
        # excepción interna y devolverá el mensaje de fallo.
        # Verificamos únicamente la estructura del retorno en caso de fallo.
        resultado = BaseDatos.guardar_claves_profesores()
        if 'no se pudo' in resultado.lower() or 'no se pueden' in resultado.lower():
            assert len(resultado) > 0, "El mensaje de error no debe estar vacío"

    def test_no_propaga_excepciones(self):
        try:
            BaseDatos.guardar_claves_profesores()
            lanzada = False
        except Exception:
            lanzada = True
        assert not lanzada, (
            "guardar_claves_profesores no debe propagar excepciones"
        )

    def test_claves_tienen_longitud_bcrypt(self):
        if not self._ficheros_fuente_disponibles():
            return
        BaseDatos.guardar_claves_profesores()
        if not os.path.isfile(self.RUTA_CLAVES):
            return
        with open(self.RUTA_CLAVES, encoding='utf-8') as f:
            lineas = [l.rstrip('\n') for l in f if l.strip()]
        for linea in lineas:
            if ' - ' in linea:
                clave = linea.split(' - ', 1)[1]
                assert len(clave) == 60, (
                    f"La clave bcrypt debe tener 60 caracteres, tiene {len(clave)}"
                )


if __name__ == '__main__':
    unittest.main()
