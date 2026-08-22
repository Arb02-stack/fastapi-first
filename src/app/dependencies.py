# conexão com banco de dados

from models import db 
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        # cria conexão com banco de dados
        Session = sessionmaker(bind=db)
        # Abre uma conexão com o banco
        session = Session()
        yield session
    finally:
        session.close()
