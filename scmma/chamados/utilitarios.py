from decimal import Decimal
from geopy.distance import distance
from geopy.geocoders import Nominatim

from .exceptions import CalculoDistanciaException, ConversaoEnderecoGeolocalizacaoException


def calcular_distancia_pontos(inicial: tuple, final: tuple) -> float:
    try:
        if inicial is None or final is None:
            raise Exception
        distancia = distance(inicial, final)
    except Exception:
        raise CalculoDistanciaException()
    return Decimal(str(distancia.km))


def converter_endereco_geolocalizacao(endereco: str) -> tuple:
    geolocalizador = Nominatim(user_agent='scmma')
    geolocalizacao = geolocalizador.geocode(endereco)
    try:
        latitude = Decimal(str(geolocalizacao.latitude))
        longitude = Decimal(str(geolocalizacao.longitude))
        return (latitude, longitude)
    except Exception:
        raise ConversaoEnderecoGeolocalizacaoException
