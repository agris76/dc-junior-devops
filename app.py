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
    
@app.route('/api/headers')
def headers():
    headers = dict(request.headers)
    format = request.args.get('format', 'html')

    if format == 'json':
        return headers, 200, {'Content-Type': 'application/json'}
    elif format == 'xml':
        root = ET.Element('headers')
        for key, value in headers.items():
            node = ET.SubElement(root, key)
            node.text = value
        xml_str = ET.tostring(root)
        return Response(xml_str, content_type="text/xml")
    else:
        output = []
        for key, value in headers.items():
            output.append(f'{key}: {value}')
        return '<br>'.join(output), 200, {'Content-Type': 'text/html'}
    
@app.route("/api/post", methods=["POST"])
def post():
    output = []
    for key, value in request.form.items():
        output.append(f"{key}: {value}")
    output = "\n".join(output)

    if request.args.get("format") == "json":
        response = Response(output, content_type="application/json")
    elif request.args.get("format") == "xml":
        response = Response(output, content_type="application/xml")
    else:
        response = Response(f"<pre>{output}</pre>", content_type="text/html")

    return response    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
