from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

# Configuração de logging para o Heroku
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/cxml")
async def receive_cxml(request: Request):
    try:
        # Lê o conteúdo do cXML enviado
        cxml_data = await request.body()
        cxml_str = cxml_data.decode("utf-8")
        
        # Log do cXML recebido
        logger.info(f"cXML Recebido: {cxml_str}")
        
        return JSONResponse(content={"message": "cXML recebido com sucesso!"}, status_code=200)
    except Exception as e:
        logger.error(f"Erro ao processar o cXML: {e}")
        return JSONResponse(content={"error": "Erro ao processar o cXML"}, status_code=500)

@app.get("/")
def home():
    return {"message": "Servidor FastAPI funcionando! Poste seu cXML em /cxml"}
