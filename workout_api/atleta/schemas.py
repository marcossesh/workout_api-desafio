from typing import Annotated, Optional
from pydantic import Field, PositiveFloat, BaseModel
from workout_api.contrib.schemas import BaseSchema, OutMixin
from uuid import UUID


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]


class AtletaIn(Atleta):
    categoria_id: int
    centro_treinamento_id: int


class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseModel):
    peso: Optional[float] = None
    altura: Optional[float] = None
    idade: Optional[int] = None