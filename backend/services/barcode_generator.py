# Purpose    : Generates Code128 barcode images from a CodeRequest.
# Consumed by: Flask API endpoint (API layer)
# Layer      : Services


import io
import base64
import barcode

from barcode.writer import ImageWriter
from backend.domain.code_request import CodeRequest
from backend.services.code_generator import CodeGenerator


class BarcodeGenerator(CodeGenerator):
    """
    Concrete implementation of CodeGenerator for Code128 barcode images.

    Generates a Code128 barcode from the value stored in the CodeRequest
    and returns it as a base64-encoded PNG string.

    Code128 is used because it supports all alphanumeric characters,
    which covers vehicle plates and general text input.
    """

    def generate(self, request: CodeRequest) -> str:
        """
        Generates a Code128 barcode image from the given CodeRequest.

        :param request: A validated CodeRequest instance with code_type 'barcode'.
        :returns: A base64-encoded string representing the PNG image.
        """
        code128_class = barcode.get_barcode_class("code128")

        image_buffer = io.BytesIO()

        generated_barcode = code128_class(
            request.value,
            writer=ImageWriter()
        )

        generated_barcode.write(image_buffer)
        image_buffer.seek(0)

        encoded_image = base64.b64encode(image_buffer.read()).decode("utf-8")

        return encoded_image