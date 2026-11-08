# src/dominio/usuario.py
# Cuenta de acceso de un empleado: Empleado 1 a 0..1 Usuario.
# Esta clase no conoce SQL ni bcrypt, solo valida y guarda el hash.


class Usuario:
    MIN_USUARIO = 3
    MAX_USUARIO = 40
    MIN_CLAVE = 6

    def __init__(self, nombre_usuario, password_hash, empleado_id, id_usuario=None):
        if type(empleado_id) is not int or empleado_id <= 0:
            raise ValueError("El ID del empleado debe ser positivo.")
        self._id_usuario = id_usuario
        self.empleado_id = empleado_id
        self.nombre_usuario = self.normalizar_usuario(nombre_usuario)
        self.password_hash = password_hash  # se guarda el hash, nunca la contraseña

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor):
        # lo usa el DAO para guardar el id que genera la base de datos
        self._id_usuario = valor

    @classmethod
    def normalizar_usuario(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El usuario debe ser texto.")
        nombre = nombre.strip().lower()
        if not cls.MIN_USUARIO <= len(nombre) <= cls.MAX_USUARIO:
            raise ValueError(
                f"El usuario debe tener entre {cls.MIN_USUARIO} "
                f"y {cls.MAX_USUARIO} caracteres."
            )
        if not all(c.isascii() and (c.isalnum() or c == "_") for c in nombre):
            raise ValueError("Use letras ASCII, números o guion bajo.")
        return nombre

    @classmethod
    def validar_clave(cls, clave):
        if not isinstance(clave, str):
            raise TypeError("La contraseña debe ser texto.")
        if len(clave) < cls.MIN_CLAVE:
            raise ValueError(f"Use al menos {cls.MIN_CLAVE} caracteres.")
        return clave  # sin strip ni lower: la contraseña se guarda tal cual

    def __str__(self):
        # no se muestra el hash
        return (f"Usuario(id={self.id_usuario}, usuario={self.nombre_usuario}, "
                f"empleado_id={self.empleado_id})")
