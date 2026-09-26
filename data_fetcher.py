import os
import requests

ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"


class DataFetchError(Exception):
    pass


def fetch_transactions(address: str, api_key: str | None = None, max_records: int = 1000) -> list[dict]:
    api_key = api_key or os.environ.get("ETHERSCAN_API_KEY")
    if not api_key:
        raise DataFetchError(
            "ETHERSCAN_API_KEY bulunamadı. .env dosyanı kontrol et."
        )

    if not address or not address.lower().startswith("0x") or len(address) != 42:
        raise DataFetchError(
            "Geçersiz Ethereum adresi. Adres '0x' ile başlamalı ve 42 karakter olmalı."
        )

    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": max_records,
        "sort": "asc",
        "apikey": api_key,
    }

    try:
        response = requests.get(ETHERSCAN_BASE_URL, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise DataFetchError(f"Etherscan'e bağlanırken hata oluştu: {exc}") from exc

    payload = response.json()

    if payload.get("status") == "0" and payload.get("message") != "No transactions found":
        raise DataFetchError(f"Etherscan hatası: {payload.get('result')}")

    result = payload.get("result", [])
    if not isinstance(result, list):
        return []

    return result
