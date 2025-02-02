from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import logging

# Configuração de logging para o Heroku
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# URL de destino para encaminhar o cXML
DESTINATION_URL = "https://loja.rhimex.com.br/version-test/api/1.1/wf/recebe_poom"

@app.post("/cxml")
async def receive_cxml(request: Request):
    try:
        # Lê o conteúdo do cXML enviado
        cxml_data = await request.body()
        cxml_str = cxml_data.decode("utf-8")

        # Log do cXML recebido
        logger.info(f"cXML Recebido: {cxml_str}")

        # Enviar o cXML para o endpoint externo
        async with httpx.AsyncClient() as client:
            response = await client.post(DESTINATION_URL, json={"cxmlcontent": cxml_str})

        # Log do status da requisição
        logger.info(f"Resposta do destino: {response.status_code} - {response.text}")

        # Retorna o status da requisição externa
        return JSONResponse(content={"message": "cXML encaminhado com sucesso!", "status": response.status_code}, status_code=200)

    except Exception as e:
        logger.error(f"Erro ao processar ou encaminhar o cXML: {e}", exc_info=True)
        return JSONResponse(content={"error": "Erro ao processar o cXML"}, status_code=500)

@app.get("/")
def home():
    return {"message": "Servidor FastAPI funcionando! Poste seu cXML em /cxml"}
