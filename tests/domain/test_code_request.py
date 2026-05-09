import pytest

from backend.domain.code_request import CodeRequest


class TestCodeRequestValidValue:
    """Tests for successfully created CodeRequest instances."""

    def test_creates_qrcode_request_with_valid_value(self):
        request = CodeRequest(value="251D13501", code_type="qrcode")

        assert request.value == "251D13501"
        assert request.code_type == "qrcode"

    def test_creates_barcode_request_with_valid_value(self):
        request = CodeRequest(value="251D13501", code_type="barcode")

        assert request.value == "251D13501"
        assert request.code_type == "barcode"

    def test_strips_whitespace_from_value(self):
        request = CodeRequest(value="  251D13501  ", code_type="qrcode")

        assert request.value == "251D13501"

    def test_normalises_code_type_to_lowercase(self):
        request = CodeRequest(value="251D13501", code_type="QRCODE")

        assert request.code_type == "qrcode"

    def test_accepts_value_at_maximum_qrcode_length(self):
        value_at_limit = "A" * CodeRequest.MAXIMUM_QR_CODE_LENGTH
        request = CodeRequest(value=value_at_limit, code_type="qrcode")

        assert len(request.value) == CodeRequest.MAXIMUM_QR_CODE_LENGTH

    def test_accepts_value_at_maximum_barcode_length(self):
        value_at_limit = "A" * CodeRequest.MAXIMUM_BARCODE_LENGTH
        request = CodeRequest(value=value_at_limit, code_type="barcode")

        assert len(request.value) == CodeRequest.MAXIMUM_BARCODE_LENGTH


class TestCodeRequestInvalidValue:
    """Tests for CodeRequest instances that must raise ValueError."""

    def test_raises_error_when_value_is_empty_string(self):
        with pytest.raises(ValueError):
            CodeRequest(value="", code_type="qrcode")

    def test_raises_error_when_value_is_only_whitespace(self):
        with pytest.raises(ValueError):
            CodeRequest(value="   ", code_type="qrcode")

    def test_raises_error_when_value_is_not_a_string(self):
        with pytest.raises(ValueError):
            CodeRequest(value=12345, code_type="qrcode")

    def test_raises_error_when_code_type_is_invalid(self):
        with pytest.raises(ValueError):
            CodeRequest(value="251D13501", code_type="pdf")

    def test_raises_error_when_code_type_is_not_a_string(self):
        with pytest.raises(ValueError):
            CodeRequest(value="251D13501", code_type=123)

    def test_raises_error_when_qrcode_value_exceeds_maximum_length(self):
        value_too_long = "A" * (CodeRequest.MAXIMUM_QR_CODE_LENGTH + 1)

        with pytest.raises(ValueError):
            CodeRequest(value=value_too_long, code_type="qrcode")

    def test_raises_error_when_barcode_value_exceeds_maximum_length(self):
        value_too_long = "A" * (CodeRequest.MAXIMUM_BARCODE_LENGTH + 1)

        with pytest.raises(ValueError):
            CodeRequest(value=value_too_long, code_type="barcode")