# src/dominio/empleado.py
from __future__ import annotations
from typing import TYPE_CHECKING
from dominio.registroTiempo import RegistroTiempo

if TYPE_CHECKING:  # solo para los tipos: evita el import circular
    from dominio.departamento import Departamento
    from dominio.proyecto import Proyecto


class Empleado:
    # CONSTANTES (no son columnas de la tabla)
    # MAX_CORREO es 150 porque la columna correo es VARCHAR(150)
    MIN_NOMBRE = 2
    MAX_NOMBRE = 100
    MIN_CORREO = 6
    MAX_CORREO = 150

    # CONSTRUCTOR
    # id_empleado=None: todavía no está guardado en la base de datos
    def __init__(self, nombre, correo, salario=0.0, id_empleado=None, departamento=None):
        self.nombre = nombre
        self.correo = correo
        self.salario = salario
        self._id_empleado = id_empleado
        self._departamento = None
        # id de la clave foránea; se llena al cargar de la BD o al asignar un departamento
        self._departamento_id = None
        if departamento is not None:
            self.asignar_departamento(departamento)
        self._proyectos: list[Proyecto] = []
        self._registros: list[RegistroTiempo] = []

    # VALIDADORES (no usan input ni print, avisan el error con raise)
    @classmethod
    def validar_nombre(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser texto.")
        nombre = nombre.strip()
        if not cls.MIN_NOMBRE <= len(nombre) <= cls.MAX_NOMBRE:
            raise ValueError(
                f"El nombre debe tener entre {cls.MIN_NOMBRE} "
                f"y {cls.MAX_NOMBRE} caracteres."
            )
        return nombre

    @classmethod
    def validar_correo(cls, correo):
        if not isinstance(correo, str):
            raise TypeError("El correo debe ser texto.")
        correo = correo.strip()
        if not cls.MIN_CORREO <= len(correo) <= cls.MAX_CORREO:
            raise ValueError("Correo fuera del largo permitido.")
        if any(c.isspace() for c in correo):
            raise ValueError("El correo no debe contener espacios.")
        if correo.count("@") != 1:
            raise ValueError("El correo debe contener un solo @.")
        usuario, dominio = correo.split("@")
        if not usuario or "." not in dominio:
            raise ValueError("Use un correo como nombre@empresa.cl.")
        if any(not parte for parte in dominio.split(".")):
            raise ValueError("El dominio contiene puntos inválidos.")
        return correo

    # PROPIEDADES
    # los setters usan los validadores, así el constructor y la semilla cumplen las mismas reglas
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_nombre(valor)

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = self.validar_correo(valor).lower()

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        es_numero = isinstance(valor, (int, float)) and not isinstance(valor, bool)
        if not es_numero or valor < 0:
            raise ValueError("El salario debe ser un número mayor o igual a 0")
        self._salario = float(valor)

    @property
    def id_empleado(self):
        return self._id_empleado

    @id_empleado.setter
    def id_empleado(self, valor):
        # lo usa el DAO para guardar el id que genera la base de datos
        self._id_empleado = valor

    @property
    def departamento(self):
        return self._departamento

    @property
    def departamento_id(self):
        """Id del departamento (clave foránea). None si no tiene departamento."""
        if self._departamento is not None and self._departamento.id_departamento is not None:
            return self._departamento.id_departamento
        return self._departamento_id

    @departamento_id.setter
    def departamento_id(self, valor):
        # lo usa el DAO al reconstruir un Empleado desde la BD
        self._departamento_id = valor

    @property
    def proyectos(self) -> tuple:
        return tuple(self._proyectos)

    @property
    def registros(self) -> tuple:
        return tuple(self._registros)

    # MÉTODOS DEL UML
    def get_salario(self):
        return self._salario

    def registrar_horas(self, fecha, horas, descripcion="", proyecto=None) -> bool:
        if horas <= 0 or horas > 24:
            return False
        registro = RegistroTiempo(
            fecha, horas, descripcion,
            empleado_id=self.id_empleado,
            proyecto_id=proyecto.id_proyecto if proyecto is not None else None,
        )
        self._registros.append(registro)
        return True

    def asignar_departamento(self, departamento: Departamento) -> bool:
        """Asigna el departamento y sincroniza el otro lado de la relación."""
        if self._departamento is departamento:
            return False
        self._departamento = departamento
        self._departamento_id = departamento.id_departamento
        departamento.agregar_empleado(self)
        return True

    def agregar_proyecto(self, proyecto: Proyecto) -> bool:
        """Agrega el proyecto y sincroniza el otro lado de la relación."""
        if proyecto in self._proyectos:
            return False
        self._proyectos.append(proyecto)
        proyecto.asignar_empleado(self)
        return True

    # PRESENTACIÓN
    def __str__(self):
        return (f"Empleado(id={self.id_empleado}, nombre={self.nombre}, "
                f"correo={self.correo}, salario={self.salario}, "
                f"departamento_id={self.departamento_id})")

    def mostrar_datos(self) -> str:
        return f"[{self.id_empleado}] {self.nombre} <{self.correo}> - ${self.salario:,.0f}"