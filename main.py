from typing import Dict, Any
from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

app = FastAPI()

# Modelo que aceita qualquer JSON no corpo
class RequestData(BaseModel):
    content: Dict[str, Any]

# Endpoint que recebe o JSON
@app.post("/")
async def receber_json(dados: RequestData):
    try:
        # Captura o conteúdo do JSON recebido
        json_recebido = dados.content

        # URL do outro endpoint
        outro_endpoint = 'https://loja.rhimex.com.br/version-test/api/1.1/wf/json_puro'

        # Converte o JSON em uma string (texto)
        jsoncontent = f"{json_recebido}"

        # Envia o texto diretamente no corpo da requisição
        async with httpx.AsyncClient() as client:
            response = await client.post(outro_endpoint, content=jsoncontent)

        # Verifica o status da resposta
        if response.status_code == 200:
            return {"status": "success", "message": "Dados enviados com sucesso."}
        else:
            raise HTTPException(status_code=500, detail="Falha ao enviar os dados para o outro endpoint.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
