from flask import Flask, request, Response, jsonify
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def convert_json_to_cxml():
    if request.content_type != "application/json":
        return Response(
            "Erro: O cabeçalho Content-Type deve ser 'application/json'",
            status=415
        )

    data = request.json
    if not data:
        return Response("Erro: JSON inválido ou ausente", status=400)

    # Seu código para processar o JSON e gerar o XML aqui...

    timestamp_iso = format_timestamp(data.get("timestamp", ""))

    cxml = ET.Element("cXML", {
        "payloadID": data.get("payloadID", ""),
        "xml:lang": data.get("xml_lang", ""),
        "timestamp": timestamp_iso
    })

    header = ET.SubElement(cxml, "Header")

    # <From>
    from_elem = ET.SubElement(header, "From")
    from_cred = ET.SubElement(from_elem, "Credential", {"domain": data.get("From_domain", "")})
    ET.SubElement(from_cred, "Identity").text = data.get("From_Identity", "")

    # <To>
    to_elem = ET.SubElement(header, "To")
    to_cred = ET.SubElement(to_elem, "Credential", {"domain": data.get("To_domain", "")})
    ET.SubElement(to_cred, "Identity").text = data.get("To_Identity", "")

    # <Sender>
    sender_elem = ET.SubElement(header, "Sender")
    sender_cred = ET.SubElement(sender_elem, "Credential", {"domain": data.get("Sender_domain", "")})
    ET.SubElement(sender_cred, "Identity").text = data.get("Sender_Identity", "")
    ET.SubElement(sender_cred, "SharedSecret").text = data.get("Sender_SharedSecret", "")
    ET.SubElement(sender_elem, "UserAgent").text = data.get("Sender_UserAgent", "")

    # <Message>
    message = ET.SubElement(cxml, "Message")
    punchout_order_msg = ET.SubElement(message, "PunchOutOrderMessage")
    ET.SubElement(punchout_order_msg, "BuyerCookie").text = data.get("BuyerCookie", "")

    header_elem = ET.SubElement(punchout_order_msg, "PunchOutOrderMessageHeader", {
        "operationAllowed": data.get("PunchOutOrderMessageHeader_operationAllowed", "")
    })
    total_elem = ET.SubElement(header_elem, "Total")
    money_elem = ET.SubElement(total_elem, "Money", {"currency": data.get("Total_Money_currency", "")})
    money_elem.text = data.get("Total_Money_value", "")

    item_in = ET.SubElement(punchout_order_msg, "ItemIn", {"quantity": data.get("ItemIn_quantity", "")})
    item_id = ET.SubElement(item_in, "ItemID")
    ET.SubElement(item_id, "SupplierPartID").text = data.get("ItemID_SupplierPartID", "")
    ET.SubElement(item_id, "SupplierPartAuxiliaryID").text = data.get("ItemID_SupplierPartAuxiliaryID", "")

    item_detail = ET.SubElement(item_in, "ItemDetail")
    unit_price = ET.SubElement(item_detail, "UnitPrice")
    money = ET.SubElement(unit_price, "Money", {"currency": data.get("ItemDetail_UnitPrice_Money_currency", "")})
    money.text = data.get("ItemDetail_UnitPrice_Money_value", "")
    ET.SubElement(item_detail, "Description").text = data.get("ItemDetail_Description", "")
    ET.SubElement(item_detail, "ShortName").text = data.get("ItemDetail_ShortName", "")
    ET.SubElement(item_detail, "UnitOfMeasure").text = data.get("ItemDetail_UnitOfMeasure", "")
    classification = ET.SubElement(item_detail, "Classification", {
        "domain": data.get("ItemDetail_Classification_domain", "")
    })
    classification.text = data.get("ItemDetail_Classification_value", "")
    ET.SubElement(item_detail, "ManufacturerPartID").text = data.get("ItemDetail_ManufacturerPartID", "")
    ET.SubElement(item_detail, "ManufacturerName").text = data.get("ItemDetail_ManufacturerName", "")
    ET.SubElement(item_detail, "LeadTime").text = data.get("ItemDetail_LeadTime", "")

    for extrinsic_key in [
        "cus_flagtopunchout", "cus_ncmcode", "cus_materialorigin", "cus_purchaseorg",
        "cus_taxcategory", "cus_erpcommoditycode", "cus_incoterms",
        "cus_incotermsnotes", "cus_region", "cus_minimumamounttoinvoice"
    ]:
        ET.SubElement(item_detail, "Extrinsic", {"name": extrinsic_key}).text = data.get(f"Extrinsic_{extrinsic_key}", "")

    xml_data = ET.tostring(cxml, encoding="utf-8", method="xml").decode("utf-8")
    xml_with_header = f'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE cXML SYSTEM "http://xml.cxml.org/schemas/cXML/1.2.011/cXML.dtd">\n{xml_data}'

    return Response(xml_with_header, mimetype="application/xml")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
