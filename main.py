from flask import Flask, request, Response, render_template_string
from defusedxml.ElementTree import fromstring
from datetime import datetime
import logging

# Configuração de log
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Lista para armazenar os XMLs recebidos
received_xmls = []

@app.route("/", methods=["POST"])
def receive_xml():
    try:
        # Obtém o XML do corpo da requisição
        xml_data = request.data.decode('utf-8')

        # Log do XML recebido (para depuração)
        logging.debug(f"Recebido XML:\n{xml_data}")

        # Parseia o XML para garantir que está bem formado
        try:
            root = fromstring(xml_data)
        except Exception as e:
            logging.error(f"Erro ao parsear XML: {str(e)}")
            return Response(f"Erro: XML inválido. Detalhes: {str(e)}", status=400)

        # Adiciona o XML na lista (com o timestamp para ordenação)
        timestamp = datetime.now().isoformat()  # Exemplo de timestamp
        received_xmls.append({"timestamp": timestamp, "xml": xml_data})
        
        # Retorna uma resposta de sucesso
        return Response("XML recebido e impresso com sucesso", status=200)
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        return Response(f"Erro inesperado: {str(e)}", status=500)

@app.route("/received-xmls", methods=["GET"])
def show_received_xmls():
    # Cria o conteúdo HTML com os XMLs recebidos
    response_html = "<h1>XMLs Recebidos</h1>"

    if not received_xmls:
        response_html += "<p>Não há XMLs recebidos.</p>"
    
    for entry in received_xmls:
        response_html += f"<h3>Timestamp: {entry['timestamp']}</h3>"
        response_html += f"<pre>{entry['xml']}</pre><hr>"
    
    return render_template_string(response_html)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
