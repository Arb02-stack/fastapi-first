from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['auth'])


def criar_token(id_usuario):
    # padrão para a criação tokens de acesso
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {
        "sub": id_usuario,
        "exp": data_expiracao
    }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha): # compara a senha informada com a senha (hash) armazenada no DB
        return False

    # Se a senha estiver correta
    return usuario


# Rota inicial (home)
@auth_router.get('/')
async def home_auth_router():
    return {
            "title": "Página principal de 'autenticação'",
            "status": "online",
            "message": "APIRouter (/auth)",
           }
    
# Criar conta
@auth_router.post('/criar_conta')
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        # Existe um user com esse email
        raise HTTPException(
                    status_code=400,
                    detail="E-mail de usuário já cadastrado no sistema."
                )
    else:
        # Se não existir um user com esse email cria o Cadastro
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha) # criptografa a senha
        novo_usuario = Usuario(
                    usuario_schema.nome,
                    usuario_schema.email,
                    senha_criptografada,
                    usuario_schema.ativo,
                    usuario_schema.admin
                )
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso! [{usuario_schema.email}]"}

# rota login
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao) ):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não cadastrado ou credenciais inválidas.")
    else:
        access_token = criar_token(usuario.id)
        # headers
        return {
            "access_token": access_token,
            "token_type"  : "Bearer" # JWT Bearer
        }
        





