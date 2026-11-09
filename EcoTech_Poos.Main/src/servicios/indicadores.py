# servicios/indicadores.py
# Coordina sesión, consulta a la API, guardado en la BD local y respaldo.
# Devuelve resultados; mostrarlos le toca al menú.
import logging

import requests

from persistencia.indicador_dao import IndicadorDAO
from servicios.api_dolar import obtener_datos
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.permisos import exigir_sesion

# fallos esperables al consultar la API o leer su respuesta
_ERRORES_API = (requests.exceptions.RequestException, ValueError, KeyError, TypeError)


# RESPALDO
def buscar_respaldo():
    """Último dato guardado en la BD local (la API falló o respondió algo inválido)."""
    try:
        dato = IndicadorDAO.ultimo()
    except Exception:
        logging.exception("No se pudo leer el respaldo del indicador")
        dato = None

    if dato is None:
        return {"dato": None, "origen": None,
                "mensaje": "Servicio no disponible y no hay datos guardados."}
    return {"dato": dato, "origen": "BD local",
            "mensaje": "Servicio no disponible o respuesta inválida: "
                       "se muestra el último dato guardado."}


# CONSULTA
def consultar_indicador(sesion):
    exigir_sesion(sesion)
    try:
        dato = DeserializadorIndicador.desde_api(obtener_datos())
    except _ERRORES_API:
        logging.exception("Falló la consulta del dólar")  # el detalle queda en ecotech.log
        return buscar_respaldo()

    # el guardado se confirma solo si fue exitoso
    try:
        IndicadorDAO.guardar(dato)
        mensaje = "Dato guardado en la base de datos local."
    except Exception:
        logging.exception("No se pudo guardar el indicador")
        mensaje = "No se pudo guardar el dato en la base de datos local."
    return {"dato": dato, "origen": "API", "mensaje": mensaje}


# HISTORIAL
def obtener_historial(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()  # lee la BD, no llama a la API