from decimal import Decimal
from geopy.distance import distance
from geopy.geocoders import Nominatim


def calcular_distancia_pontos(inicial: tuple, final: tuple) -> float:
    distancia = distance(inicial, final)
    return Decimal(str(distancia.km))


def converter_endereco_geolocalizacao(endereco: str) -> tuple:
    geolocalizador = Nominatim(user_agent='scmma')
    geolocalizacao = geolocalizador.geocode(endereco)
    latitude = Decimal(str(geolocalizacao.latitude))
    longitude = Decimal(str(geolocalizacao.longitude))
    return (latitude, longitude)
