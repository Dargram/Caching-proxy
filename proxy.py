from flask import Flask, request, Response

import requests
import argparse
import json
import logging

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def logging_options():
    logging.basicConfig(level=logging.INFO,
        format="%(asctime)s \033[36m[%(levelname)s]\033[0m %(message)s")

    return logging.getLogger(__name__)

def main():

    logger = logging_options()
    config = load_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int)
    parser.add_argument("-o", "--origin", type=str)
    args = parser.parse_args()

    origin = config['proxy']['target']
    app = Flask(__name__)

    @app.route('/', defaults={"path":""}, methods=["GET"])
    @app.route("/<path:path>", methods=["GET"])
    def proxy(path):
        url = f"{args.origin or origin}/{path}"
        headers = dict(request.headers)
        headers.pop("Host", None)

        resp = requests.request(url=url, headers=headers, params=request.args, method=request.method)
        logger.info(f"\033[32mFinal url: {url} -> Status code: [{resp.status_code}]\033[0m")

        return Response(resp.content, resp.status_code)

    app.run(port=args.port)

if __name__ == "__main__":
    main()
