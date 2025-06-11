from flask import Flask, request, render_template_string
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import os, base64

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Ứng dụng Ký số Đỉnh Cao</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"/>
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet"/>
<style>
  body {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #f0f0f0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  h1 {
    font-weight: 900;
    letter-spacing: 2px;
    text-shadow: 1px 1px 6px rgba(0,0,0,0.4);
  }
  .card {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 15px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  .card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.4);
  }
  .btn-primary {
    background: #8e44ad;
    border: none;
    box-shadow: 0 4px 15px #8e44ad;
    transition: background 0.3s ease;
  }
  .btn-primary:hover {
    background: #a569bd;
  }
  .form-control {
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    transition: background 0.3s ease;
  }
  .form-control:focus {
    background: rgba(255,255,255,0.35);
    color: #222;
    box-shadow: 0 0 10px #a569bd;
  }
  textarea.form-control {
    background: rgba(0,0,0,0.15);
    color: #eee;
  }
  footer {
    margin-top: 50px;
    font-size: 0.9rem;
    opacity: 0.7;
  }
</style>
</head>
<body>
<div class="container py-5">
  <h1 class="text-center mb-4">🔐 Ứng dụng Ký số Đỉnh Cao</h1>
  <div class="row g-4">
    <div class="col-md-6">
      <div class="card p-4">
        <h3 class="mb-3"><i class="bi bi-pencil-square"></i> Ký số file</h3>
        <form method="POST" action="/sign" enctype="multipart/form-data" novalidate>
          <input type="file" class="form-control mb-3" name="file" required />
          <button class="btn btn-primary w-100" type="submit">Tạo chữ ký số</button>
        </form>
      </div>
    </div>
    <div class="col-md-6">
      <div class="card p-4">
        <h3 class="mb-3"><i class="bi bi-patch-check-fill"></i> Xác minh chữ ký</h3>
        <form method="POST" action="/verify" enctype="multipart/form-data" novalidate>
          <input type="file" class="form-control mb-3" name="file" required />
          <input type="file" class="form-control mb-3" name="signature" required />
          <button class="btn btn-primary w-100" type="submit">Xác minh chữ ký</button>
        </form>
      </div>
    </div>
  </div>
  
  {% if signature %}
  <div class="mt-4">
    <h5>Chữ ký số (Base64):</h5>
    <textarea class="form-control" rows="6" readonly>{{ signature }}</textarea>
  </div>
  {% endif %}
  
  {% if result %}
  <div class="alert mt-4 {{ 'alert-success' if result == 'Hợp lệ' else 'alert-danger' }}">
    <h5>Kết quả xác minh: {{ result }}</h5>
  </div>
  {% endif %}
  
  <footer class="text-center text-light">&copy; 2025 Ứng dụng Ký số Đỉnh Cao</footer>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

def generate_keys():
    if not os.path.exists("private.pem") or not os.path.exists("public.pem"):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with open("private.pem", "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open("public.pem", "wb") as f:
            f.write(key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

def load_private_key():
    with open("private.pem", "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key():
    with open("public.pem", "rb") as f:
        return serialization.load_pem_public_key(f.read())

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

@app.route("/sign", methods=["POST"])
def sign():
    file = request.files["file"]
    data = file.read()
    private_key = load_private_key()
    signature = private_key.sign(data, padding.PKCS1v15(), hashes.SHA256())
    signature_b64 = base64.b64encode(signature).decode()
    return render_template_string(TEMPLATE, signature=signature_b64)

@app.route("/verify", methods=["POST"])
def verify():
    file = request.files["file"]
    signature_file = request.files["signature"]
    data = file.read()
    signature = base64.b64decode(signature_file.read())
    public_key = load_public_key()
    try:
        public_key.verify(signature, data, padding.PKCS1v15(), hashes.SHA256())
        result = "Hợp lệ"
    except Exception:
        result = "Không hợp lệ"
    return render_template_string(TEMPLATE, result=result)

if __name__ == "__main__":
    generate_keys()
    app.run(debug=True)
