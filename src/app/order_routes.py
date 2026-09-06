from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido, Usuario, ItemPedido
from typing import List

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
@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
        id_pedido: int,
        session: Session = Depends(pegar_sessao),
        usuario: Usuario = Depends(verificar_token)
    ):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(
                    status_code=400,
                    detail="Pedido não econtrado."
                )
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Ação não autorizada para esse usuário.")
    
    pedido.status = "CANCELADO"

    session.commit()
    return {
        "mensagem": f"Pedido [{pedido.id}] concelado com sucesso!",
        "pedido"  : pedido
    }


# listar todos pedidos (apenas admin)
@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Ação não autorizada para esse usuário.")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }

# adicionar pedido
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: ItemPedidoSchema,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)
                               ):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Ação não autorizada para esse usuário.")

    item_pedido = ItemPedido( id_pedido,
                              item_pedido_schema.sabor,
                              item_pedido_schema.tamanho,
                              item_pedido_schema.quantidade,
                              item_pedido_schema.preco_unitario
                            )
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item criado com sucesso!",
        "item id": item_pedido.id,
        "preço_pedido:": pedido.preco
    }


# remover item pedido
@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido( id_item_pedido: int,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)
                               ):
   item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
   pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first() # pyright: ignore[reportOptionalMemberAccess]
   if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não encontrado.")

   if not usuario.admin and usuario.id != pedido.usuario: # pyright: ignore[reportOptionalMemberAccess]
       raise HTTPException(status_code=401, detail="Ação não autorizada para esse usuário.")

   session.delete(item_pedido)
   pedido.calcular_preco() # pyright: ignore[reportOptionalMemberAccess]
   session.commit()
   return {
       "mensagem": "Item removido com sucesso!",
       "quantidade_itens_pedido": len(pedido.itens), # pyright: ignore[reportOptionalMemberAccess]
       "pedido:": pedido
   }


# finalizar um pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(
        id_pedido: int,
        session: Session = Depends(pegar_sessao),
        usuario: Usuario = Depends(verificar_token)
    ):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(
                    status_code=400,
                    detail="Pedido não econtrado."
                )
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Ação não autorizada para esse usuário.")  
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"Pedido [{pedido.id}] finalizado com sucesso!",
        "pedido"  : pedido
    }

# vizualizar um pedido
@order_router.get("/pedido/{id_pedido}")
async def vizualizar_pedido(id_pedido: int,
                            session: Session = Depends(pegar_sessao),
                            usuario: Usuario = Depends(verificar_token)
                            ):
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
         raise HTTPException(status_code=400, detail="Item no pedido não encontrado.")
    if not usuario.admin and usuario.id != pedido.usuario: # pyright: ignore[reportOptionalMemberAccess]
        raise HTTPException(status_code=401, detail="Ação não autorizada para esse usuário.")
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# vizualizar todos os pedidos do usuário logado
@order_router.get("/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema])
async def listar_todos_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
        pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
        return pedidos 



