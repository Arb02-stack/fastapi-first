from fastapi import APIRouter


order_router = APIRouter(prefix='/orders', tags=['orders'])
 
@order_router.get("/")
async def default_orders():
    return {
            "title": "Página principal de 'pedidos'",
            "status": "Online",
            "message": "APIRouter (/orders)"
           } 
