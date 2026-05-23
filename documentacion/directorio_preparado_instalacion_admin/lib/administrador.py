class Administrador:
    def __init__(self, id_ad, clave):
        self._id = id_ad
        self._clave = clave

    def __eq__(self, other):
        return self._id == other._id and self._clave == other._clave