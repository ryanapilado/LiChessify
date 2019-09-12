import logging

import azure.functions as func
import paramiko
import re
import os
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # temporary test input
    board_image_url = "https://lichessifyfuncbba7.blob.core.windows.net/chessboards/2djjq4pmk4p31.jpg"

    try:
        fen, certainty = get_fen(board_image_url)
        link = "https://lichess.org/analysis/{0}".format(fen)

        body = {
            "link":link,
            "certainty":certainty
        }
        return func.HttpResponse(body=json.dumps(body), status_code=200)
    except:
        return func.HttpResponse(status_code=400)


def parse_fen_from_output(output: str) -> str:

    match = re.search("Predicted FEN: (.*)\nFinal Certainty: (.*)%", output)
    assert(match)
    return match.group(1), float(match.group(2))

def get_fen(board_image_url: str) -> str:

    hostname = os.environ['CHESSBOT_IP']
    username = os.environ['CHESSBOT_USERNAME']
    port = os.environ['CHESSBOT_PORT']
    password = os.environ['CHESSBOT_PASSWORD']

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(
        "cd tensorflow_chessbot && ./tensorflow_chessbot.py --url {0}"
        .format(board_image_url)
        )

    output = stdout.read().decode("utf-8")
    client.close()

    return parse_fen_from_output(output)