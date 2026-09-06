from pydantic import BaseModel
from typing import List

class UsuarioSchema(BaseModel):
    nome:  str
    email: str
    senha: str
    ativo: bool = True
    admin: bool = False 

    # Informa que são informações de banco de dados
    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    id_usuario: int # id chave estrangeira da tabela 'pedidos' que vem da tabela 'usuarios'

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade:     int
    sabor:          str
    tamanho:        str
    preco_unitario: float

    class Config:
        from_attributes = True

class ResponsePedidoSchema(BaseModel):
    id:     int
    status: str
    preco:  float
    itens:  List[ItemPedidoSchema]

    class Config:
        from_attributes = True


