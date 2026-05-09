from backend.domain.code_request import CodeRequest
from backend.services.barcode_generator import BarcodeGenerator
from backend.services.qr_generator import QRCodeGenerator

request = CodeRequest(value="251D13501", code_type="qrcode")
generator = QRCodeGenerator()
result = generator.generate(request)

print("Base64 gerado com sucesso!")
print(f"Primeiros 80 caracteres: {result[:80]}")
print(f"Tamanho total: {len(result)} caracteres")

barcode_request = CodeRequest(value="251D13501", code_type="barcode")
barcode_generator = BarcodeGenerator()
barcode_result = barcode_generator.generate(barcode_request)

print("\nBarcodeGenerator:")
print(f"  Primeiros 80 caracteres: {barcode_result[:80]}")
print(f"  Tamanho total: {len(barcode_result)} caracteres")
