from flask import Flask, request, Response

import requests
import argparse
import json
import logging

def main():

    logging.basicConfig(level=logging.INFO, format="%(asctime)s \033[36m[%(levelname)s]\033[0m %(message)s")
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-o", "--origin", type=str)
    args = parser.parse_args()

    with open("config.json", "r") as f:
        config = json.load(f)

    origin = config['proxy']['target']
    app = Flask(__name__)

    @app.route('/', defaults={"path":""}, methods=["GET"])
    @app.route("/<path:path>", methods=["GET"])
    def proxy(path):
        url = f"{args.origin or origin}/{path}"
        headers = dict(request.headers)
        headers.pop("Host", None)

        resp = requests.request(url=url, headers=headers, params=request.args, method=request.method)
        logger.info(f"Status code: \033[36m{resp.status_code}\033[0m")
        print("Final url:", url)

        return Response(resp.content, resp.status_code)

    app.run(port=args.port)

if __name__ == "__main__":
    main()
