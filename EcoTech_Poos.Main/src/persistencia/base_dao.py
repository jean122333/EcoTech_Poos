# persistencia/base_dao.py
"""Funciones que usan todos los DAO.

Aquí está el patrón de conexión, commit, rollback y cierre, para no repetirlo en cada DAO.
No tiene SQL de ninguna entidad.
"""
from persistencia.conexion import abrir_conexion


def ejecutar_escritura(sql, parametros=()):
    """INSERT / UPDATE / DELETE. Devuelve (filas_afectadas, ultimo_id).

    Hace commit si sale bien y rollback si falla; la conexión siempre se cierra.
    El error se propaga para que el DAO o el menú decida el mensaje.
    """
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
        return cursor.rowcount, cursor.lastrowid
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        if conexion:
            conexion.close()


def consultar(sql, parametros=(), uno=False):
    """SELECT. Devuelve una fila (o None) si uno=True; si no, una lista de filas."""
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchone() if uno else cursor.fetchall()
    finally:
        if conexion:
            conexion.close()