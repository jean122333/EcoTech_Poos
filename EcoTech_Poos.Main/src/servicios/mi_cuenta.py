from dominio.empleado import Empleado
from dominio.registroTiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.permisos import exigir_sesion

# Operaciones sobre los datos propios: el empleado sale siempre de la sesión, unca se pide el ID de otra persona.

# FICHA
def mi_ficha(sesion):
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    return empleado


def actualizar_mis_datos(sesion, nombre, correo):
    """Solo cambia nombre y correo propios; rol, ID, salario."""
    exigir_sesion(sesion)
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)
    empleado = mi_ficha(sesion)
    empleado.nombre, empleado.correo = nombre, correo
    return EmpleadoDAO.actualizar(empleado)


# PROYECTOS Y REGISTROS
def mis_proyectos(sesion):
    exigir_sesion(sesion)
    return ProyectoDAO.listar_por_empleado(sesion["empleado_id"])

    # Prueba github Commit

def mis_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(sesion["empleado_id"])


def registrar_mis_horas(sesion, fecha, horas, descripcion, proyecto_id):
    """Registra horas del empleado conectado, solo en proyectos que tiene asignados."""
    exigir_sesion(sesion)
    asignados = {p.id_proyecto for p in mis_proyectos(sesion)}
    if proyecto_id not in asignados:
        raise ValueError("Solo puede registrar horas en proyectos que tiene asignados.")
    registro = RegistroTiempo(fecha, horas, descripcion,
                              empleado_id=sesion["empleado_id"], proyecto_id=proyecto_id)
    return RegistroTiempoDAO.insertar(registro)