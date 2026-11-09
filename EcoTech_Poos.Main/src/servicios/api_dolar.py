import requests
from dominio.indicador import Indicador

# Este solo obtiene y valida datos; guardarlos y mostrarlos le toca a otras capas.

# CONSTANTES
URL_DOLAR = "https://mindicador.cl/api/dolar"


# CONSULTA
def obtener_datos():
    respuesta = requests.get(URL_DOLAR, timeout=(3, 5))
    # se revisa el estado HTTP antes de leer el JSON (404, 500, etc. no son datos)
    if respuesta.status_code != 200:
        raise requests.exceptions.HTTPError(f"Estado HTTP {respuesta.status_code}")
    return respuesta.json()


# EXTRACCIÓN
def extraer_primero(datos):
    """Devuelve (fecha, valor) válidos del primer registro de la serie."""
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")
    if datos.get("unidad_medida") != "Pesos":
        raise ValueError("Unidad inesperada.")
    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles.")

    registro = serie[0]
    valor = Indicador.validar_valor(registro["valor"])
    # '2026-01-02T00:00:00.000Z' queda como '2026-01-02'
    fecha = Indicador.validar_fecha(registro["fecha"][:10])
    return fecha, valor