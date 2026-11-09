# servicios/autenticacion.py
# Registro y login. Usuario tiene las reglas, UsuarioDAO guarda y el menú muestra los mensajes.
import bcrypt

from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.permisos import exigir_admin

# CONSTANTES
MAX_BYTES_BCRYPT = 72  # bcrypt no acepta más de 72 bytes


# HASH
def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")


# REGISTRO
def registrar_usuario(empleado_id, nombre, clave, rol="empleado"):
    """Guarda la cuenta. Solo la semilla pasa rol='admin'; los menús usan crear_cuenta_empleado."""
    nombre = Usuario.normalizar_usuario(nombre)
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("No existe un empleado con ese ID.")
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")
    if UsuarioDAO.buscar_por_empleado(empleado_id) is not None:
        raise ValueError("No se pudo crear esa cuenta.")
    usuario = Usuario(nombre, crear_hash(clave), empleado_id, rol=rol)
    UsuarioDAO.insertar(usuario)
    return usuario.id_usuario  # registrar no inicia sesión


def crear_cuenta_empleado(sesion, empleado_id, nombre, clave):
    """Operación protegida: solo el admin crea cuentas, y siempre con rol empleado."""
    exigir_admin(sesion)
    return registrar_usuario(empleado_id, nombre, clave, rol="empleado")


# LOGIN
def autenticar(nombre, clave):
    """Devuelve los datos de la sesión (con rol) o None si el usuario o la clave fallan."""
    nombre = Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None
    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)
    if cuenta is None:
        return None
    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        return None
    return {
        "id_usuario": cuenta.id_usuario,
        "empleado_id": cuenta.empleado_id,
        "nombre_usuario": cuenta.nombre_usuario,
        "rol": cuenta.rol,
    }