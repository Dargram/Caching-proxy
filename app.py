from flask import Flask
import requests, argparse, json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

def app():
    app = Flask(__name__)

    @app.route('/', defaults={"path":""})
    @app.route("/<path:path>")
    def proxy(path):
        #тут requests

    return app

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-o", "--origin", type=str, required=True)
    args = parser.parse_args()

    return args


def json_loader():
    with open("config.json", "r") as f:
        config = json.load(f)
        return config

def main():
    args_parser()
    json_loader()
    app()

if __name__ == "__main__":
    main()
