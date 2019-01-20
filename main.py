# Made by: Muhammad F. Khan
# Simple QR-Code Generator made using flask and qrcode
# Github: https://github.com/M-Faheem-Khan/
# Repo URL: https://github.com/M-Faheem-Khan/QR-Code-Generator/

# importing necessary modules
import qrcode # for generating the qr code
import base64 # for base64 conversion
from flask import Flask, request, render_template, send_file # for serving the necessary files

app = Flask("__name__")

# defining the url 
@app.route("/start", methods=["GET", "POST"])
def main():
    # returning the html page where the code will be displayed
    return render_template("index.html")

# defining the url
@app.route("/generate_qr_code/<data>")
def gen_qr_code(data):
    # Generates the qr-code based on the url data  

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
    # returning the image url
    return img_url

# defining the url
@app.route("/qr_image")
def return_image():
    # returning the qr_code image so the html page can get the image as a resource and display it in the page
    return send_file("image.png", attachment_filename="image.png")

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=5000, debug=False)