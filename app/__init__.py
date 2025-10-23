# -*- coding: utf-8 -*-
"""
Descrição do arquivo
"""

import hashlib
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import requests
from flask import Flask, jsonify


app = Flask(__name__)


def obter_timeout() -> int:
    """
    Retorna as definições para connection e read timeout

    Returns:
        int: definições para connection e read timeout
    """
    return (5, 5)


def do_get(url: str, timeout: int | tuple[int, int] = obter_timeout()) -> Any:
    """
    Encapsula requests.get

    Args:
        url (str): url a ser consumida
        timeout (int | tuple[int, int], optional): Definições de timeout. Defaults to obter_timeout().

    Returns:
        Any: Resposta da requisição
    """
    return requests.get(url=url, timeout=timeout)


def agora(tz: str = "America/Sao_Paulo") -> datetime:
    """
    Retorna a data/hora atual com tz oficial BR

    Args:
        tz (str, optional): timezone a ser utilizada. Defaults to "America/Sao_Paulo".

    Returns:
        datetime: data/hora atual com tz oficial BR
    """
    return datetime.now(ZoneInfo(tz))


@app.route("/", methods=["GET"])
def get():
    """
    Descrição da função

    Returns:
        tipo de retorno da função: descrição do retorno da função
    """
    url = "http://www.google.com.br"

    r = do_get(url=url)

    retorno = jsonify(
        {
            "url": url,
            "requests.get.status_code": r.status_code,
            "requests.get.text.length": len(r.text),
            "requests.get.text.hash": hashlib.sha512(r.text.encode()).hexdigest(),
            "teste": "çãé",
        }
    )

    return retorno


if __name__ == "__main__":
    app.run()
