import qrcode
import base64
from datetime import datetime
from flask import Flask, request, render_template, send_file

app = Flask("__name__")

@app.route("/start", methods=["GET", "POST"])
def main():
    return render_template("index.html")

@app.route("/generate_qr_code/<data>")
def gen_qr_code(data):
    data = str(base64.b64decode(data))
    # Create qr code instance
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
    )

    # Add data
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    img.save("image.png")
    print("Image was saved")
    img_url = str(base64.b64encode("http://localhost:5000/qr_image".encode("utf-8")).encode("ASCII"))
    print(img_url)
    return img_url


@app.route("/qr_image")
def return_image():
    return send_file("image.png", attachment_filename="image.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)