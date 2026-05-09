import io
import base64
import qrcode



from backend.domain.code_request import CodeRequest
from backend.services.code_generator import CodeGenerator


class QRCodeGenerator(CodeGenerator):

    """

    """
    def generate(self, request:CodeRequest) ->str:
        """

        :param request:
        :return:
        """

        qr_code_image = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr_code_image.add_data(request.value)
        qr_code_image.make(fit=True)

        rendered_image = qr_code_image.make_image(
            fill_color="black",
            back_color="white",
        )

        image_buffer = io.BytesIO()
        rendered_image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        encoded_image = base64.b64encode(image_buffer.read()).decode("utf-8")

        return encoded_image