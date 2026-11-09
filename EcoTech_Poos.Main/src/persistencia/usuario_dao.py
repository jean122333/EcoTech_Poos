# persistencia/usuario_dao.py
from dominio.usuario import Usuario
from persistencia.base_dao import ejecutar_escritura, consultar
from persistencia.conexion import marcador_sql

# columnas de la tabla, en el mismo orden que usa _fila_a_usuario()
_COLUMNAS = "id_usuario, nombre_usuario, password_hash, empleado_id, rol"


class UsuarioDAO:
    # MAPEO FILA -> OBJETO
    @staticmethod
    def _fila_a_usuario(fila):
        return Usuario(
            id_usuario=fila[0],
            nombre_usuario=fila[1],
            password_hash=fila[2],
            empleado_id=fila[3],
            rol=fila[4],
        )

    # CREATE
    @staticmethod
    def insertar(usuario):
        m = marcador_sql()
        sql = (
            "INSERT INTO usuario (nombre_usuario, password_hash, empleado_id, rol) "
            f"VALUES ({m}, {m}, {m}, {m})"
        )
        _, nuevo_id = ejecutar_escritura(
            sql,
            (usuario.nombre_usuario, usuario.password_hash, usuario.empleado_id, usuario.rol),
        )
        usuario.id_usuario = nuevo_id
        return usuario

    # READ
    @staticmethod
    def _buscar_uno(columna, valor):
        # columna es una constante interna; el valor va siempre parametrizado
        sql = f"SELECT {_COLUMNAS} FROM usuario WHERE {columna} = {marcador_sql()}"
        fila = consultar(sql, (valor,), uno=True)
        return None if fila is None else UsuarioDAO._fila_a_usuario(fila)

    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        return UsuarioDAO._buscar_uno("nombre_usuario", nombre_usuario)

    @staticmethod
    def buscar_por_empleado(id_empleado):
        return UsuarioDAO._buscar_uno("empleado_id", id_empleado)

    @staticmethod
    def contar():
        return int(consultar("SELECT COUNT(*) FROM usuario", uno=True)[0])