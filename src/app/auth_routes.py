from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context

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
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        # Existe um user com esse email
        raise HTTPException(
                    status_code=400,
                    detail="E-mail de usuário já cadastrado no sistema."
                )
    else:
        # Se não existir um user com esse email cria o Cadastro
        senha_criptografada = bcrypt_context.hash(senha) # criptografa a senha
        novo_usuario = Usuario(nome, email, senha_criptografada) 
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso! [{email}]"}





