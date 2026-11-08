# servicios/indicadores.py
# Consulta del dólar observado a una API (mindicador.cl).
# Este archivo solo obtiene y valida datos; mostrarlos le toca al menú.
import math
from datetime import date

import requests

URL_DOLAR = "https://mindicador.cl/api/dolar"


def obtener_datos():
    respuesta = requests.get(URL_DOLAR, timeout=(3, 5))
    respuesta.raise_for_status()  # primero se revisa el estado HTTP
    return respuesta.json()


def extraer_primero(datos):
    """Devuelve (fecha, valor) del primer registro de la serie."""
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")
    if datos.get("unidad_medida") != "Pesos":
        raise ValueError("Unidad inesperada.")
    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles.")

    registro = serie[0]
    valor = registro["valor"]
    # solo números finitos y mayores que cero
    if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
        raise ValueError("Valor del indicador inválido.")
    # '2026-01-02T00:00:00.000Z' queda como '2026-01-02'
    fecha = date.fromisoformat(registro["fecha"][:10]).isoformat()
    return fecha, valor


def clp_a_usd(monto_clp, valor_dolar):
    if valor_dolar <= 0 or monto_clp < 0:
        raise ValueError("Valores inválidos para la conversión.")
    return monto_clp / valor_dolar
