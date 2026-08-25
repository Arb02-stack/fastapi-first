# conexão com banco de dados
from fastapi import Depends, HTTPException
from models import db, Usuario
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

def pegar_sessao():
    try:
        # cria conexão com banco de dados
        Session = sessionmaker(bind=db)
        # Abre uma conexão com o banco
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        if not SECRET_KEY:
            raise RuntimeError("[SECRET KEY] não definida.")
       
        dict_info  = jwt.decode(token, SECRET_KEY, ALGORITHM)
        sub = dict_info.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Token Inválido.")
        id_usuario = int(sub)
    except (JWTError, ValueError):     
        raise HTTPException(status_code=401, detail="Acesso Negado! Verifique a validade do token.")
    # verificar se o token é valido
    # extrair o id do usuario do token
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido.") 
    return usuario

