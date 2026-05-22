import bcrypt

from claves.conexion_bbdd import conexion


class Profesor:
    def __init__(self, nombre: str, apellidos: str):
        self._nombre: str = nombre
        self._apellidos: str = apellidos
        self._id: str = self._generar_id()
        self._clave: str = self._generar_clave()
        self._clave_encriptada: str = self._encriptar_clave()

    def __str__(self):
        return self._nombre + ' ' + self._apellidos

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellidos(self):
        return self._apellidos

    @property
    def id(self):
        return self._id

    @property
    def clave(self):
        return self._clave

    @property
    def clave_encriptada(self):
        return self._clave_encriptada

    def imprimir_id_nombre_apellidos(self):
        print(f"{self._id.ljust(37)}{self._nombre} {self._apellidos}")

    def _generar_id(self):
        usuario: str = ''
        if self._nombre and self._apellidos:
            usuario += self._nombre[0].lower() + self._apellidos.replace(' ',
                                                            '').lower()
        else:
            usuario = ''
        return usuario

    def _generar_clave(self):
        clave: str = ''
        clave += (self._nombre.replace(' ', '').lower() +
                  str(len(self._nombre.replace(' ', '').lower()) + len(
                      self._apellidos.replace(' ', '').lower())))
        return clave

    def _encriptar_clave(self):
        clave_bytes = self._clave.encode('utf-8')
        sal = bcrypt.gensalt()
        clave_encriptada = bcrypt.hashpw(clave_bytes, sal)
        return clave_encriptada.decode('utf-8')

