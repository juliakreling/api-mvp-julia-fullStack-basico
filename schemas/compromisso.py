from pydantic import BaseModel
from typing import Optional, List
from model.compromisso import Compromisso


class CompromissoCreateSchema(BaseModel):
    """ Define como um novo compromisso a ser inserido deve ser representado
    """
    nome: str


class CompromissoUpdateSchema(BaseModel):
    """ Define como um compromisso existente deve ser representado para atualização 
    """
    id: int
    nome: str


class CompromissoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Compromisso.
    """
    nome: str


class ListagemCompromissoSchema(BaseModel):
    """ Define como uma listagem de Compromissos será retornada.
    """
    compromissos: List[CompromissoCreateSchema]


def apresenta_compromissos(compromissos: List[Compromisso]):
    """ Retorna uma representação do compromisso seguindo o schema definido em
        CompromissoViewSchema.
    """
    result = []
    for compromisso in compromissos:
        result.append({
            "id": compromisso.id,
            "nome": compromisso.nome,
        })

    return {"compromissos": result}


class CompromissoViewSchema(BaseModel):
    """ Define como um compromisso será retornado.
    """
    id: int
    nome: str


class CompromissoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_compromisso(compromisso: Compromisso):
    """ Retorna uma representação do compromisso seguindo o schema definido em
        CompromissoViewSchema.
    """
    return {
        "id": compromisso.id,
        "nome": compromisso.nome,
    }
