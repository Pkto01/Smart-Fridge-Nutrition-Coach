from enum import Enum

from pydantic import BaseModel


class SexeEnum(Enum):
    Homme = "Homme"
    Femme = "Femme"
    NoneP = "Non précisé"
