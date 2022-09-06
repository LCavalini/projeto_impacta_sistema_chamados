class CalculoDistanciaException(Exception):

    def __init__(self, message: str = 'erro ao calcular a distância de dois pontos') -> None:
        super().__init__(message)


class SemTecnicosDisponiveisException(Exception):

    def __init__(self, message: str = 'não há técnicos disponíveis') -> None:
        super().__init__(message)
