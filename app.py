import os
import json
from flask import Flask, request, Response
import xml.etree.ElementTree as ET


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/api/environment")
def environment():
    output = []
    for key, value in os.environ.items():
        output.append(f"{key}: {value}")

    format = request.args.get('format', 'html')

    if format == 'json':
        response = Response(json.dumps(output), content_type="application/json")
    elif format == 'xml':
        root = ET.Element('environment')
        for key, value in os.environ.items():
            node = ET.SubElement(root, key)
            node.text = value
        xml_str = ET.tostring(root, encoding='utf8', method='xml')
        response = Response(xml_str, content_type="application/xml")
    else:
        output = []
        for key, value in os.environ.items():
            output.append(f'{key}: {value}')
        response = Response(f"<br>\n".join(output), content_type="text/html")

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
