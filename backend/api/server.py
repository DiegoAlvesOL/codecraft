
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS


from backend.domain.code_request import CodeRequest
from backend.services.qr_generator import QRCodeGenerator
from backend.services.barcode_generator import BarcodeGenerator


_frontend_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')

application = Flask(__name__, static_folder=_frontend_folder)
CORS(application)

_generators ={
    "qrcode": QRCodeGenerator(),
    "barcode": BarcodeGenerator(),
}


@application.route("/")
def index():
    """Serves the frontend index.html."""
    return send_from_directory(_frontend_folder, "index.html")

@application.route("/<path:filename>")
def static_file(filename):
    """Serves any static file from the frontend folder (css, js, images)."""
    return send_from_directory(_frontend_folder, filename)


@application.route("/generate", methods=["POST"])
def generate():
    """
    Receives a JSON payload with 'value' and 'code_type',
    generates the requested visual code, and returns it as
    a base64-encoded PNG string.

    Expected request body:
        { "value": "251D13501", "code_type": "qrcode" }

    Returns:
        200: { "image": "<base64 string>", "code_type": "qrcode" }
        400: { "error": "<validation message>" }
        500: { "error": "Internal server error." }
    """

    request_data = request.get_json()

    if not request_data:
        return jsonify({"error": "Request body must be JSON."}), 400

    value = request_data.get("value", "")
    code_type = request_data.get("code_type", "")

    try:
        code_request = CodeRequest(value=value, code_type=code_type)
    except ValueError as validation_error:
        return jsonify( {"error": str(validation_error)}), 400


    try:
        generator = _generators[code_request.code_type]
        encoded_image = generator.generate(code_request)
    except Exception:
        return jsonify({"error": "Internal server error."}), 500

    return jsonify({
        "image": encoded_image,
        "code_type": code_request.code_type,
    }), 200

if __name__ == "__main__":
    application.run(debug=True, port=5000)





