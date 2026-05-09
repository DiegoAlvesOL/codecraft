# Purpose    : Unit tests for QRCodeGenerator and BarcodeGenerator services.
# Consumed by: pytest (test runner)
# Layer      : Tests — Services


import base64
import pytest
from backend.domain.code_request import CodeRequest
from backend.services.qr_generator import QRCodeGenerator
from backend.services.barcode_generator import BarcodeGenerator


class TestQRCodeGenerator:
    """Tests for the QRCodeGenerator service."""

    def test_returns_a_non_empty_string(self):
        request = CodeRequest(value="251D13501", code_type="qrcode")
        generator = QRCodeGenerator()

        result = generator.generate(request)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_valid_base64_encoded_string(self):
        request = CodeRequest(value="251D13501", code_type="qrcode")
        generator = QRCodeGenerator()

        result = generator.generate(request)

        decoded = base64.b64decode(result)
        assert len(decoded) > 0

    def test_generates_different_images_for_different_values(self):
        first_request = CodeRequest(value="251D13501", code_type="qrcode")
        second_request = CodeRequest(value="192AB7890", code_type="qrcode")
        generator = QRCodeGenerator()

        first_result = generator.generate(first_request)
        second_result = generator.generate(second_request)

        assert first_result != second_result


class TestBarcodeGenerator:
    """Tests for the BarcodeGenerator service."""

    def test_returns_a_non_empty_string(self):
        request = CodeRequest(value="251D13501", code_type="barcode")
        generator = BarcodeGenerator()

        result = generator.generate(request)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_valid_base64_encoded_string(self):
        request = CodeRequest(value="251D13501", code_type="barcode")
        generator = BarcodeGenerator()

        result = generator.generate(request)

        decoded = base64.b64decode(result)
        assert len(decoded) > 0

    def test_generates_different_images_for_different_values(self):
        first_request = CodeRequest(value="251D13501", code_type="barcode")
        second_request = CodeRequest(value="192AB7890", code_type="barcode")
        generator = BarcodeGenerator()

        first_result = generator.generate(first_request)
        second_result = generator.generate(second_request)

        assert first_result != second_result