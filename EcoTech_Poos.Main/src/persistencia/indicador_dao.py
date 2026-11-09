from dominio.indicador import Indicador
from persistencia.base_dao import ejecutar_escritura, consultar
from persistencia.conexion import marcador_sql, obtener_motor

_COLUMNAS = "fuente, codigo, fecha, valor, unidad, verificado_en"


class IndicadorDAO:
    # MAPEO FILA => OBJETO
    @staticmethod
    def _fila_a_indicador(fila):
        return Indicador(
            fuente=fila[0],
            fecha=str(fila[2]),  # MariaDB entrega un objeto date
            valor=float(fila[3]),  # y un DECIMAL
            verificado_en=str(fila[5]),  # y un datetime
        )

    # CREATE / UPDATE
    @staticmethod
    def _sql_guardar():
        m = marcador_sql()
        insertar = (
            f"INSERT INTO indicador_api ({_COLUMNAS}) "
            f"VALUES ({m}, {m}, {m}, {m}, {m}, {m})"
        )
        # indicador + fecha: se actualiza la fila en vez de duplicarla
        if obtener_motor() == "sqlite":
            return insertar + (
            " ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET "
            "valor = excluded.valor, unidad = excluded.unidad, "
            "verificado_en = excluded.verificado_en"
        )
        return insertar + (
            " ON DUPLICATE KEY UPDATE "
            "valor = VALUES(valor), unidad = VALUES(unidad), "
            "verificado_en = VALUES(verificado_en)"
        )

        # Prueba Archivo Update en Github

    @staticmethod
    def guardar(indicador):
        """Inserta la observación o si existe, actualiza valor y última verificación."""
        ejecutar_escritura(
            IndicadorDAO._sql_guardar(),
            (indicador.fuente, indicador.codigo, indicador.fecha, indicador.valor,
             indicador.unidad, indicador.verificado_en),
        )

    # READ
    @staticmethod
    def listar(codigo="dolar"):
        """Historial del más reciente al más antiguo."""
        sql = (f"SELECT {_COLUMNAS} FROM indicador_api WHERE codigo = {marcador_sql()} "
               "ORDER BY fecha DESC")
        return [IndicadorDAO._fila_a_indicador(fila) for fila in consultar(sql, (codigo,))]

    @staticmethod
    def ultimo(codigo="dolar"):
        """Dato más reciente guardado, o None si no hay ninguno."""
        sql = (f"SELECT {_COLUMNAS} FROM indicador_api WHERE codigo = {marcador_sql()} "
               "ORDER BY fecha DESC LIMIT 1")
        fila = consultar(sql, (codigo,), uno=True)
        return None if fila is None else IndicadorDAO._fila_a_indicador(fila)