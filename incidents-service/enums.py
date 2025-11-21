from enum import Enum

class StatusEnum(str, Enum):
    abierta = "abierta"
    en_progreso = "en_progreso"
    cerrada = "cerrada"