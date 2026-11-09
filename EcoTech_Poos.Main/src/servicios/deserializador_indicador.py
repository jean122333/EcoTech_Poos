from dominio.indicador import Indicador
from servicios.api_dolar import extraer_primero

# Transforma la respuesta de la API (diccionario) en un objeto Indicador.

class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos):
        fecha, valor = extraer_primero(datos)  # extrae y valida los datos
        return Indicador(fecha=fecha, valor=valor)

    # No consulta la API ni guarda en la BD.