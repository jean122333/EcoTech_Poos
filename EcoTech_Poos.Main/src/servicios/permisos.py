import functools
from dominio.usuario import Usuario

# Control de acceso reutilizable: se comprueba antes de ejecutar cada operación o solo al mostrar el menú.


# COMPROBACIONES
def exigir_sesion(sesion):
    if not isinstance(sesion, dict):
        raise PermissionError("Inicie sesión.")
    if sesion.get("rol") not in Usuario.ROLES:
        raise PermissionError("Acceso no permitido.")
    empleado_id = sesion.get("empleado_id")
    if type(empleado_id) is not int or empleado_id <= 0:
        raise PermissionError("Sesión inválida.")


def exigir_admin(sesion):
    exigir_sesion(sesion)
    if sesion["rol"] != "admin":
        raise PermissionError("Acción solo para administrador.")

    # Prueba GitHub Commit

# DECORADOR
def requiere_admin(funcion):
    """Para operaciones cuyo primer parámetro es la sesión: verifica el rol antes de actuar."""
    @functools.wraps(funcion)
    def envoltura(sesion, *args, **kwargs):
        exigir_admin(sesion)
        return funcion(sesion, *args, **kwargs)
    return envoltura