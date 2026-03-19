from flask import Flask, request, Response
import requests, argparse, json

def main():
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
        print("Status code:", resp.status_code)
        print("\033[31m Final .url:", url, "\033[0m")

        return Response(resp.content, resp.status_code)

    app.run(port=args.port)

if __name__ == "__main__":
    main()
