from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
from pathlib import Path
from sqlalchemy import create_engine

# cria conexão com banco de dados
BASE_DIR = Path(__file__).resolve().parent # path: src/app/db
DATABASE_URL = f"sqlite:///{BASE_DIR / 'database.db'}"

db = create_engine(DATABASE_URL)

# cria a base do banco de dados
Base = declarative_base()

# cria a classe/tabelas do banco
class Usuario(Base):
    __tablename__= "usuarios"
    id    = Column("id",    Integer, primary_key=True, autoincrement=True)
    nome  = Column("nome",  String,  nullable=False)
    email = Column("email", String,  nullable=False)
    senha = Column("senha", String,  nullable=False)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome  = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__= "pedidos"

    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id      = Column("id", Integer, primary_key=True, autoincrement=True)
    status  = Column("status", ChoiceType(choices=STATUS_PEDIDOS)) # pendente/cancelado/finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id")) # chave estrangeira com acesso a classe usuarios
    preco   = Column("preco", Float)
    # itens =

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status  = status
        self.usuario = usuario
        self.preco   = preco


class ItemPedido(Base):
    __tablename__= "itens_pedido"

    id             = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade     = Column("quantidade", Integer)
    sabor          = Column("sabor", String) 
    tamanho        = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido         = Column("pedido", ForeignKey("pedidos.id")) # precisa existir um pedido feito

    def __init__(self, pedido, sabor, tamanho, quantidade=0, preco_unitario=0) -> None:
        self.pedido         = pedido
        self.sabor          = sabor
        self.tamanho        = tamanho
        self.quantidade     = quantidade
        self.preco_unitario = preco_unitario

# cria efetivamente o banco de dados











