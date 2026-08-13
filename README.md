# FastAPI | Poetry

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

