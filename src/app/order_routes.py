from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido, Usuario

order_router = APIRouter(
        prefix='/pedidos',
        tags=['orders'],
        dependencies=[Depends(verificar_token)]
)
 
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

# cancelar pedido
@order_router.post("/Pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(
                    status_code=400,
                    detail="Pedido não econtrado."
                )
    
    pedido.status = "CANCELADO"

    session.commit()
    return {
        "mensagem": f"Pedido [{id_pedido}] concelado com sucesso!",
        "pedido"  : pedido
    }



