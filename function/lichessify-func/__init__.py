import logging

import azure.functions as func
import azure.storage.blob as blob
import paramiko
import re
import os
import json
import io
import uuid

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    block_blob_service = blob.BlockBlobService(
        account_name=os.environ["STORAGE_ACCOUNT_NAME"],
        account_key=os.environ["STORAGE_ACCOUNT_KEY"]
        )

    # write image from HTTP body to blob
    container_name = os.environ["STORAGE_CONTAINER_NAME"]
    stream = io.BytesIO(req.get_body())
    blob_name = "board_{0}.jpg".format(uuid.uuid4())
    block_blob_service.create_blob_from_stream(container_name, blob_name, stream)

    # get fen from blob using chessfenbot
    try:
        blob_url = block_blob_service.make_blob_url(container_name, blob_name)
        fen, certainty = get_fen(blob_url)
        body = {
            "link":"https://lichess.org/analysis/{0}".format(fen),
            "certainty":certainty
        }

        block_blob_service.delete_blob(container_name, blob_name)
        return func.HttpResponse(body=json.dumps(body), status_code=200)

    except:
        block_blob_service.delete_blob(container_name, blob_name)
        return func.HttpResponse(status_code=400)

def parse_fen_from_output(output: str) -> str:
    ''' Retrieve the FEN and certainty from tensorflow_chessbot output.
    '''

    match = re.search("Predicted FEN: (.*)\nFinal Certainty: (.*)%", output)
    assert(match)
    return match.group(1), float(match.group(2))

def get_fen(board_image_url: str) -> str:
    ''' SSH into the VM and run tensorflow_chessbot using board_image_url.
    '''

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