from fastapi import APIRouter
from models import Usuario, db 
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix='/auth', tags=['auth'])

# Rota inicial (home)
@auth_router.get('/')
async def home_auth_router():
    return {
            "title": "Página principal de 'autenticação'",
            "status": "online",
            "message": "APIRouter (/auth)",
           }

# Criar usuário
@auth_router.post('/criar_conta')
async def criar_conta(email: str, senha: str, nome: str):
    # cria conexão com banco de dados
    Session = sessionmaker(bind=db)
    # Abre uma conexão com o banco
    session = Session()
    # Faz busca na tabela Usuario e compara o email
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        # Existe um user com esse email
        return {"mensagem": "já existe um usuário cadastrado com esse email."}
    else:
        # Não existe um user com esse email | Cadastro
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso!"}




