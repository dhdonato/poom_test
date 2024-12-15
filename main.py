import requests
from flask import Flask, request, Response, render_template_string
from defusedxml.ElementTree import fromstring
from datetime import datetime
import logging

# Configuração de log
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Lista para armazenar os XMLs recebidos
received_xmls = []

# Função para enviar o XML para o endpoint de destino
def send_cxml_to_app(destination_url, xml_data):
    try:
        headers = {"Content-Type": "application/xml"}
        response = requests.post(destination_url, data=xml_data, headers=headers)
        if response.status_code == 200:
            logging.debug(f"XML enviado com sucesso para {destination_url}")
        else:
            logging.error(f"Falha ao enviar XML para {destination_url}. Status: {response.status_code}")
        return response
    except requests.RequestException as e:
        logging.error(f"Erro ao enviar XML para o app de destino: {str(e)}")
        return None

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

        # Extraindo dados específicos das tags
        from_cred = root.find(".//From/Credential/Identity")
        to_cred = root.find(".//To/Credential/Identity")
        sender_cred = root.find(".//Sender/Credential/Identity")

        # Logando as credenciais e domínios
        logging.debug(f"From Identity: {from_cred.text if from_cred is not None else 'N/A'}")
        logging.debug(f"To Identity: {to_cred.text if to_cred is not None else 'N/A'}")
        logging.debug(f"Sender Identity: {sender_cred.text if sender_cred is not None else 'N/A'}")

        # Adiciona o XML na lista (com o timestamp para ordenação)
        timestamp = datetime.now().isoformat()  # Exemplo de timestamp
        received_xmls.append({"timestamp": timestamp, "xml": xml_data})

        # Aqui você pode enviar o XML para o endpoint do app de destino
        destination_url = "https://app-de-destino.com/endpoint"  # Substitua pela URL real do endpoint de destino
        send_cxml_to_app(destination_url, xml_data)

        # Retorna uma resposta de sucesso
        return Response("XML recebido e enviado para o app de destino com sucesso", status=200)
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        return Response(f"Erro inesperado: {str(e)}", status=500)

@app.route("/received-xmls", methods=["GET"])
def show_received_xmls():
    # Cria o conteúdo HTML com os XMLs recebidos
    response_html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            h1 {
                color: #2E8B57;
            }
            pre {
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                font-size: 14px;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            hr {
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <h1>XMLs Recebidos</h1>
    """

    if not received_xmls:
        response_html += "<p>Não há XMLs recebidos.</p>"

    for entry in received_xmls:
        response_html += f"<h3>Timestamp: {entry['timestamp']}</h3>"
        response_html += f"<pre>{entry['xml']}</pre><hr>"

    response_html += "</body></html>"

    return render_template_string(response_html)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
