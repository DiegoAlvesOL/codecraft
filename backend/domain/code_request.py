class CodeRequest:
    """
    Represents a request to convert a text value into a visual code.

    Validates the input at construction time, ensuring no invalid
    data reaches the generator services.
    """

    MAXIMUM_QR_CODE_LENGTH = 500
    MAXIMUM_BARCODE_LENGTH = 80
    VALID_CODE_TYPES = ("qrcode", "barcode")

    def __init__(self, value: str, code_type: str):
        """
        Initialises a CodeRequest with the given value and code type.

        :param value: The text to be encoded.
        :param code_type: Either 'qrcode' or 'barcode'.
        :raises ValueError: If value or code_type are invalid.
        """
        self._code_type = self._validate_code_type(code_type)
        self._value = self._validate_value(value)

    def _validate_code_type(self, code_type: str) -> str:
        """
        Validates that the requested code type is supported.

        :param code_type: The type string provided by the user.
        :raises ValueError: If the type is not in VALID_CODE_TYPES.
        :returns: The validated code type string.
        """
        if not isinstance(code_type, str):
            raise ValueError("Code type must be a string.")

        normalised_code_type = code_type.strip().lower()

        if normalised_code_type not in self.VALID_CODE_TYPES:
            raise ValueError(
                f"Invalid code type '{code_type}'. "
                f"Accepted values: {self.VALID_CODE_TYPES}."
            )

        return normalised_code_type

    def _validate_value(self, value: str) -> str:
        """
        Validates the text value against type, emptiness and length constraints.
        Length limit depends on the code type already validated and stored.

        :param value: The raw input from the user.
        :raises ValueError: If validation fails.
        :returns: The cleaned and validated value string.
        """
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Value cannot be empty.")

        if self._code_type == "barcode":
            if len(cleaned_value) > self.MAXIMUM_BARCODE_LENGTH:
                raise ValueError(
                    f"Barcode value cannot exceed {self.MAXIMUM_BARCODE_LENGTH} "
                    f"characters. Received: {len(cleaned_value)}."
                )

        if self._code_type == "qrcode":
            if len(cleaned_value) > self.MAXIMUM_QR_CODE_LENGTH:
                raise ValueError(
                    f"QR Code value cannot exceed {self.MAXIMUM_QR_CODE_LENGTH} "
                    f"characters. Received: {len(cleaned_value)}."
                )

        return cleaned_value

    @property
    def value(self) -> str:
        """The validated text value to be encoded."""
        return self._value

    @property
    def code_type(self) -> str:
        """The validated code type: 'qrcode' or 'barcode'."""
        return self._code_type

    def __repr__(self) -> str:
        return (
            f"CodeRequest("
            f"value='{self._value}', "
            f"code_type='{self._code_type}')"
        )