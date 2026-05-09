from logging import exception

from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.domain import code_request
from backend.domain.code_request import CodeRequest
from backend.services.qr_generator import QRCodeGenerator
from backend.services.barcode_generator import BarcodeGenerator

application = Flask(__name__)
CORS(application)

_generators ={
    "qrcode": QRCodeGenerator(),
    "barcode": BarcodeGenerator(),
}

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





