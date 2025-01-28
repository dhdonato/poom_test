from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/xml")
async def receive_xml(request: Request):
    # Lê o conteúdo do XML enviado
    xml_data = await request.body()
    print("XML Recebido:", xml_data.decode("utf-8"))  # Exibe o XML no console
    return JSONResponse(content={"message": "XML recebido com sucesso!"}, status_code=200)

@app.get("/")
def home():
    return {"message": "Servidor FastAPI funcionando! Poste seu XML em /xml"}
