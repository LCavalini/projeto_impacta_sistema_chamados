import urllib
import requests


def converter_endereco_coordenadas(endereco: str) -> tuple:
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(endereco) + '?format=json'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        resultado = resposta.json()
        longitude = resultado[0]['lon']
        latitude = resultado[0]['lat']
        return (longitude, latitude)
    raise Exception(f'Erro ao consultar o endereço {endereco}')


if __name__ == '__main__':
    endereco = 'Praça da Sé'
    longitude, latitude = converter_endereco_coordenadas(endereco)
    print(longitude, latitude)
