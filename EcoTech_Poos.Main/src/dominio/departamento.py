from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # solo para los tipos: evita el import circular con Empleado
    from dominio.empleado import Empleado


class Departamento:
    # CONSTANTES 
    MIN_NOMBRE = 2
    MAX_NOMBRE = 100
    MIN_GERENTE = 2
    MAX_GERENTE = 100

    # CONSTRUCTOR
    def __init__(self, nombre: str, gerente: str, id_departamento: int | None = None):
        self.nombre = nombre
        self.gerente = gerente
        self._id_departamento = id_departamento
        self._empleados: list[Empleado] = []

    # VALIDADORES (no usan input ni print, avisan el error con raise)
    @classmethod
    def validar_nombre(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre del departamento debe ser texto.")
        nombre = nombre.strip()
        if not cls.MIN_NOMBRE <= len(nombre) <= cls.MAX_NOMBRE:
            raise ValueError(
                f"El nombre del departamento debe tener entre {cls.MIN_NOMBRE} "
                f"y {cls.MAX_NOMBRE} caracteres."
            )
        return nombre

    @classmethod
    def validar_gerente(cls, gerente):
        if not isinstance(gerente, str):
            raise TypeError("El gerente debe ser texto.")
        gerente = gerente.strip()
        if not cls.MIN_GERENTE <= len(gerente) <= cls.MAX_GERENTE:
            raise ValueError(
                f"El gerente debe tener entre {cls.MIN_GERENTE} "
                f"y {cls.MAX_GERENTE} caracteres."
            )
        return gerente

    # PROPIEDADES
    # los setters usan los validadores, así el constructor, el DAO y la semilla cumplen las mismas reglas
    @property
    def id_departamento(self) -> int | None:
        return self._id_departamento

    @id_departamento.setter
    def id_departamento(self, valor: int | None):
        # lo usa el DAO para guardar el id que genera la base de datos
        self._id_departamento = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = self.validar_nombre(valor)

    @property
    def gerente(self) -> str:
        return self._gerente

    @gerente.setter
    def gerente(self, valor: str):
        self._gerente = self.validar_gerente(valor)

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    # MÉTODOS DEL UML
    def agregar_empleado(self, empleado: Empleado) -> bool:
        """Agrega el empleado al departamento y sincroniza el otro lado de la relación."""
        if empleado in self._empleados:
            return False

        self._empleados.append(empleado)
        empleado.asignar_departamento(self)  # Empleado hace lo mismo con este departamento
        return True

    def cantidad_empleados(self) -> int:
        return len(self._empleados)

    # PRESENTACIÓN
    def mostrar_datos(self) -> str:
        return f"[{self.id_departamento}] {self.nombre} (gerente: {self.gerente})"

    def __str__(self):
        return (f"Departamento(id={self.id_departamento}, nombre={self.nombre}, "
                f"gerente={self.gerente})")