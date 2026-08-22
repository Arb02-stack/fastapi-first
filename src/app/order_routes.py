from fastapi import APIRouter, Depends
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from models import Pedido

order_router = APIRouter(prefix='/pedidos', tags=['orders'])
 
@order_router.get("/")
async def home_orders():
    return {
            "title": "Página principal de 'pedidos'",
            "status": "Online",
            "message": "APIRouter (/orders)"
           } 

# Criar pedido
@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session=Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {
            "mensagem": f"Pedido criado com sucesso.\nId do produto: [{novo_pedido.id}]"
           }
