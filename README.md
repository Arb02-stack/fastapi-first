# FastAPI | Poetry | (pizzaria)

## Apenas o Backend

- Criar projeto:
    - poetry new nome_do_prjeto

- Ativar/Desativar ambiente virtual (dentro do diretório/projeto criado)
    - eval $(poetry env activate)
    - deactivate

## Instalar o FastAPI:
- Com o ambiente virtual ativado:
    - (venv) poetry add "fastapi[standard]"

### Rodar o servidor:
- fastapi dev main.py ou uvicorn main:app --reload

## criar/migrar banco de dados Alembic
- alembic revision --autogenerate -m "Initial Migration"

## Criação do banco de dados através das migrations
- poetry run alembic revision --autogenerate -m "Initial Migration"

## Aplicar a migration
- poetry run alembic upgrade head

# Alterações futuras no banco
## Alterar os modelos
- Depois de modificar models.py, por exemplo adicionando uma coluna:
    - telefone = Column(String)
- criar uma nova migration:
    - poetry run alembic revision --autogenerate -m "Add telefone to usuarios"
- Depois aplicar:
    - poetry run alembic upgrade head
