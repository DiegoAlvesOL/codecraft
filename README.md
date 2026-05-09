# CodeCraft

A text-to-code generator that converts any value into a **QR Code** or **Code128 Barcode**, delivered as a downloadable PNG. Built with Python, Flask, and a retro-tech frontend. Fully containerised with Docker and deployed on Railway.

---

## Features

- Converts any text input into QR Code or Code128 Barcode
- Toggle between code types without reloading the page
- Live preview of the generated image
- One-click PNG download named after the input value
- Input validation with character limits enforced on both frontend and backend
- REST API ready for integration with other systems

---

## Architecture

```
Browser (index.html)
       │  HTTP POST /generate
       ▼
  ┌─────────────────────────────────────┐  Railway
  │  ┌───────────────────────────────┐  │
  │  │  Gunicorn (WSGI · 2 workers)  │  │  Docker
  │  │            │                  │  │
  │  │       Flask API               │  │
  │  │      /generate                │  │
  │  │       ┌──────┴──────┐         │  │
  │  │   Domain         Services     │  │
  │  │  CodeRequest   QR · Barcode   │  │
  │  └───────────────────────────────┘  │
  └─────────────────────────────────────┘
       │  base64 JSON
       ▼
Browser (renders image)
```

The request enters through Gunicorn, which acts as the production WSGI server in front of Flask. Flask validates the input via the `CodeRequest` domain entity and delegates image generation to the appropriate service. The result is returned as a base64-encoded PNG string inside a JSON response.

---

## Tech Stack

| Technology | Role | Why |
|---|---|---|
| Python 3.14 | Language | Mature ecosystem for image generation and web APIs |
| Flask | Web framework | Lightweight, no-overhead REST API without boilerplate |
| Gunicorn | WSGI server | Production-grade server that handles concurrent requests safely |
| qrcode + Pillow | QR Code generation | De facto standard library for QR in Python |
| python-barcode | Barcode generation | Supports Code128, which handles full alphanumeric input |
| Docker | Containerisation | Identical environment in development and production |
| Railway | Cloud hosting | Simple Docker-based deploy with automatic HTTPS |
| pytest | Testing | Clean, readable test syntax with excellent Python support |

---

## Design Patterns & Methodology

**Object-Oriented Programming (OOP):** Every concern is encapsulated in its own class. The `CodeRequest` entity owns its own validation. The generators own their own image-building logic.

**Strategy Pattern:** `QRCodeGenerator` and `BarcodeGenerator` both inherit from the abstract `CodeGenerator` base class and implement the same `generate()` interface. The API layer selects the correct strategy at runtime based on the request, without needing to know the implementation details of either generator.

**N-Tier Architecture:** The project is divided into three layers with strict boundaries: Domain (business rules), Services (use cases), and API (delivery). No layer reaches into a layer it does not own.

---

## Project Structure

```
codecraft/
├── backend/
│   ├── domain/
│   │   └── code_request.py        # CodeRequest entity with input validation
│   ├── services/
│   │   ├── code_generator.py      # Abstract base class (Strategy interface)
│   │   ├── qr_generator.py        # QRCodeGenerator implementation
│   │   └── barcode_generator.py   # BarcodeGenerator implementation
│   ├── api/
│   │   └── server.py              # Flask server — POST /generate endpoint
│   └── main.py                    # Application entry point
├── frontend/
│   ├── index.html                 # UI with toggle, input, preview and download
│   └── logo_dcode.png             # DCODE Solutions logo
├── tests/
│   ├── domain/
│   │   └── test_code_request.py   # Unit tests for CodeRequest (13 tests)
│   └── services/
│       └── test_generators.py     # Unit tests for generators (6 tests)
├── Dockerfile                     # Production container definition
├── requirements.txt               # Python dependencies
└── README.md
```

---

## Running Locally

**Prerequisites:** Python 3.14, Git

```bash
# Clone the repository
git clone https://github.com/DiegoAlvesOL/codecraft.git
cd codecraft

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
python3 -m backend.main
```

Open `http://127.0.0.1:5000` in your browser.

---

## Running with Docker

```bash
# Build the image
docker build -t codecraft .

# Run the container
docker run -p 8000:8000 codecraft
```

Open `http://127.0.0.1:8000` in your browser.

---

## Running Tests

```bash
python3 -m pytest tests/ -v
```

Expected output: **19 tests passing**.

---

## API Reference

**POST** `/generate`

Request body:
```json
{
  "value": "251D13501",
  "code_type": "qrcode"
}
```

Response:
```json
{
  "image": "<base64-encoded PNG>",
  "code_type": "qrcode"
}
```

| Field | Type | Accepted values |
|---|---|---|
| `value` | string | Any text, max 500 chars for QR Code, max 80 chars for Barcode |
| `code_type` | string | `qrcode` or `barcode` |

Error response (400):
```json
{
  "error": "Barcode value cannot exceed 80 characters. Received: 95."
}
```

---

## License

MIT

---

<p align="center">
  Powered by <strong>DCODE Solutions</strong>
</p>