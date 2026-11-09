import math
from datetime import date, datetime


class Indicador:
    # CONSTRUCTOR
    def __init__(self, fecha, valor, verificado_en=None, fuente="mindicador.cl"):
        self.fecha = self.validar_fecha(fecha)
        self.valor = self.validar_valor(valor)
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        # última vez que se recibió una respuesta válida (la BD la entrega al cargar)
        self.verificado_en = verificado_en or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # VALIDADORES
    @staticmethod
    def validar_fecha(fecha):
        if not isinstance(fecha, str):
            raise ValueError("Fecha del indicador inválida.")
        try:
            return date.fromisoformat(fecha).isoformat()  # AAAA-MM-DD
        except ValueError:
            raise ValueError("Fecha del indicador inválida.") from None

    @staticmethod
    def validar_valor(valor):
        # solo números finitos y mayores que cero (bool queda fuera por type())
        if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
            raise ValueError("Valor del indicador inválido.")
        return valor

    # OPERACIONES
    def clp_a_usd(self, monto_clp):
        if type(monto_clp) not in (int, float) or not math.isfinite(monto_clp) or monto_clp < 0:
            raise ValueError("Monto inválido para la conversión.")
        return monto_clp / self.valor

    # PRESENTACIÓN
    def __str__(self):
        return f"{self.fecha}: {self.valor:.2f} {self.unidad}"