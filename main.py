from flask import Flask, request, Response
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

# Lista para armazenar XMLs recebidos
received_xmls = []

@app.route("/", methods=["POST"])
def receive_xml():
    try:
        # Obtém o XML do corpo da requisição
        xml_data = request.data.decode('utf-8')

        # Parseia o XML para obter o timestamp
        root = ET.fromstring(xml_data)
        timestamp = root.attrib.get('timestamp')

        # Verifica e formata o timestamp
        try:
            timestamp_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            return Response("Erro: Timestamp inválido no XML", status=400)

        # Adiciona o XML e o timestamp na lista
        received_xmls.append({"timestamp": timestamp_dt, "xml": xml_data})

        # Ordena os XMLs por timestamp
        received_xmls.sort(key=lambda x: x["timestamp"])

        return Response("XML recebido com sucesso", status=200)
    except ET.ParseError:
        return Response("Erro: XML inválido", status=400)

@app.route("/poomtest", methods=["GET"])
def show_received_xmls():
    # Retorna os XMLs em ordem
    response_html = "<h1>XMLs Recebidos</h1>"
    for entry in received_xmls:
        response_html += f"<h3>Timestamp: {entry['timestamp']}</h3>"
        response_html += f"<pre>{entry['xml']}</pre><hr>"

    return response_html

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
