from pydantic import BaseModel

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

