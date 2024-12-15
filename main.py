from flask import Flask, request, render_template_string
from defusedxml.ElementTree import fromstring

app = Flask(__name__)

# Função recursiva para extrair a hierarquia das tags
def extract_xml_hierarchy(element, parent_tag=''):
    fields = []
    tag_name = element.tag
    full_tag_name = f'{parent_tag}/{tag_name}' if parent_tag else tag_name
    fields.append({
        'name': full_tag_name,
        'value': element.text.strip() if element.text else '',
    })
    
    # Para cada subelemento, extraímos a hierarquia
    for child in element:
        fields.extend(extract_xml_hierarchy(child, full_tag_name))
    
    return fields

@app.route("/", methods=["POST"])
def receive_and_parse_xml():
    xml_data = request.data.decode('utf-8')

    # Parseia o XML
    try:
        root = fromstring(xml_data)
    except Exception as e:
        return f"Erro ao parsear XML: {str(e)}", 400

    # Extrai a hierarquia das tags
    fields = extract_xml_hierarchy(root)

    # Cria o formulário HTML com campos para cada tag
    form_html = """
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
            .field {
                margin-bottom: 15px;
            }
            label {
                font-weight: bold;
            }
            input[type="text"] {
                width: 100%;
                padding: 8px;
                margin-top: 5px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <h1>Campos do cXML Recebido</h1>
        <form action="/submit" method="POST">
    """

    # Para cada campo extraído, cria um campo no formulário
    for field in fields:
        form_html += f"""
        <div class="field">
            <label for="{field['name']}">{field['name']}</label>
            <input type="text" id="{field['name']}" name="{field['name']}" value="{field['value']}">
        </div>
        """

    form_html += """
        <button type="submit">Enviar</button>
        </form>
    </body>
    </html>
    """

    return render_template_string(form_html)


@app.route("/submit", methods=["POST"])
def submit_form():
    # Aqui, você pode processar o que foi enviado no formulário
    form_data = request.form.to_dict()
    # Faça o que for necessário com os dados, como enviá-los a outro serviço ou salvar em um banco de dados
    return f"Formulário enviado com sucesso. Dados recebidos: {form_data}"

if __name__ == "__main__":
    app.run(debug=True)
