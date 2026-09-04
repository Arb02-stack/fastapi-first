from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from pathlib import Path
from sqlalchemy import create_engine

# cria conexão com banco de dados
BASE_DIR = Path(__file__).resolve().parent # path: src/app/db
DATABASE_URL = f"sqlite:///{BASE_DIR / 'db' / 'database.db'}"

db = create_engine(DATABASE_URL)

# cria a base do banco de dados
Base = declarative_base()

# cria a classe/tabelas do banco
class Usuario(Base):
    __tablename__= "usuarios"
#    id    = Column("id",    Integer, primary_key=True, autoincrement=True)
#    nome  = Column("nome",  String,  nullable=False)
#    email = Column("email", String,  nullable=False)
#    senha = Column("senha", String,  nullable=False)
#    ativo = Column("ativo", Boolean, default=True)
#    admin = Column("admin", Boolean, default=False)

    id:    Mapped[int]  = mapped_column(primary_key=True, autoincrement=True)
    nome:  Mapped[str]  = mapped_column(nullable=False)
    email: Mapped[str]  = mapped_column(nullable=False)
    senha: Mapped[str]  = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(default=True)
    admin: Mapped[bool] = mapped_column(default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome  = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__= "pedidos"

   # STATUS_PEDIDOS = (
   #     ("PENDENTE", "PENDENTE"),
   #     ("CANCELADO", "CANCELADO"),
   #     ("FINALIZADO", "FINALIZADO")
   # )

    id      = Column("id", Integer, primary_key=True, autoincrement=True)
    status  = Column("status", String) # pendente/cancelado/finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id")) # chave estrangeira com acesso a classe usuarios
    preco   = Column("preco", Float)
    itens   = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status  = status
        self.usuario = usuario
        self.preco   = preco

    def calcular_preco(self):
        """ Percorrer todos os itens do pedido, somar todos
        os preços de todos os itens dos pedidos, editar no campo
        'preco' o valor final do preço do pedido. """
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


class ItemPedido(Base):
    __tablename__= "itens_pedido"

    id             = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade     = Column("quantidade", Integer)
    sabor          = Column("sabor", String) 
    tamanho        = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido         = Column("pedido", ForeignKey("pedidos.id")) # precisa existir um pedido feito

    def __init__(self, pedido, sabor, tamanho, quantidade=0, preco_unitario=0.0) -> None:
        self.pedido         = pedido
        self.sabor          = sabor
        self.tamanho        = tamanho
        self.quantidade     = quantidade
        self.preco_unitario = preco_unitario

# cria efetivamente o banco de dados











