from fastapi import APIRouter


auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def default_auth_router():
    return {
            "title": "Página principal de 'autenticação'",
            "status": "online",
            "message": "APIRouter (/auth)",
           }
