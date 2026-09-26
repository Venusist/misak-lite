import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
from data_fetcher import fetch_transactions, DataFetchError

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    address = request.form.get("address", "").strip()

    if not address.startswith("0x"):
        return "Hata: Adres 0x ile başlamalı."

    if len(address) != 42:
        return "Hata: Ethereum adresi 42 karakter olmalı."

    data = get_transactions(address)

    transactions = data.get("result", [])

    return render_template(
        "result.html",
        address=address,
        transactions=transactions


    )

def get_transactions(address):

    url = "https://api.etherscan.io/v2/api"

    params = {
        "chainid": 1,
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 10,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    app.run(debug=True)