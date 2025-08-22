from pydantic import BaseModel, Field
from typing import List

class Service(BaseModel):
    servico_nome: str = Field(description="Nome do serviço")
    valor: float = Field(description="Preço do serviço")


class OutputBudget(BaseModel):
    services: List[Service] = Field(default=[], description="Lista de serviços encontrados")
    message: str = Field(default="", description="Mensagem de resposta")
    quantity: int = Field(default=0, description="Quantidade de serviços encontrados")