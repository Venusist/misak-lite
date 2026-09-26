from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    address = request.form["address"].strip()

    if not address.startswith("0x"):
        return "Hata: Adres 0x ile başlamalı."

    if len(address) != 42:
        return "Hata: Ethereum adresi 42 karakter olmalı."

    return render_template(
        "result.html",
        address=address
    )


if __name__ == "__main__":
    app.run(debug=True)