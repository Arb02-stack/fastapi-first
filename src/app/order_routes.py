from fastapi import APIRouter


order_router = APIRouter(prefix='/orders', tags=['orders'])
 
#@app.get("/")
#def home():
#    return {
#            "status": "Online",
#            "message": "FastAPI | Poetry | Python"
#           } 
