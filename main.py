from flask import Flask, request, Response
from defusedxml.ElementTree import fromstring
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
        try:
            root = fromstring(xml_data)
        except Exception as e:
            return Response(f"Erro: XML inválido. Detalhes: {str(e)}", status=400)

        # Verifica se o atributo 'timestamp' está presente
        timestamp = root.attrib.get('timestamp')
        if not timestamp:
            return Response("Erro: Atributo 'timestamp' ausente no XML", status=400)

        # Valida e formata o timestamp
        try:
            timestamp_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            return Response("Erro: Timestamp inválido no XML", status=400)

        # Adiciona o XML na lista (mantendo-a ordenada por timestamp)
        received_xmls.append({"timestamp": timestamp_dt, "xml": xml_data})
        received_xmls.sort(key=lambda x: x["timestamp"])

        return Response("XML recebido com sucesso", status=200)
    except Exception as e:
        return Response(f"Erro inesperado: {str(e)}", status=500)

@app.route("/received-xmls", methods=["GET"])
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
