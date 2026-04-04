from quart import Quart, request, Response

import httpx
import argparse
import json
import logging

def load_config():
    with open("config.json", mode="r") as f:
        data = json.loads(f.read())
    return data

def logging_options():
    logging.basicConfig(level=logging.INFO,
        format="%(asctime)s \033[34m[%(levelname)s]\033[0m %(message)s")


    logging.getLogger("hypercorn.error").disabled = True
    logging.getLogger("hypercorn.access").disabled = True
    logging.getLogger("uvicorn.error").disabled = True
    logging.getLogger("werkzeug").disabled = True
    logging.getLogger("httpx").disabled = True

    return logging.getLogger(__name__)

def main():

    logger = logging_options()
    config = load_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int)
    parser.add_argument("-o", "--origin", type=str)
    args = parser.parse_args()


    origin = config['proxy']['target']
    host_ip = config['server']['host']

    print(f" * Server running on {host_ip}:{args.port}")
    app = Quart(__name__)

    @app.route('/', defaults={"path":""}, methods=["GET"])
    @app.route("/<path:path>", methods=["GET"])
    async def proxy(path):

        target_url = f"{args.origin or origin}/{path}"
        headers = dict(request.headers)
        print("\033[91m")
        print(json.dumps(headers, indent=4))
        print("\033[0m")
        headers.pop("Host", None)

        client_ip = request.remote_addr
        method = request.method

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.request(
                url=target_url,
                headers=headers,
                params=request.args,
                method=method
            )
        logger.info(
            f"\033[93m{client_ip}\033[0m "
            f"\033[94m{method}\033[0m "
            f"\033[97m->\033[0m  "
            f"\033[96m{target_url}\033[0m "
            f"\033[92m[{resp.status_code}]\033[0m "
        )

        return Response(
            resp.content,
            resp.status_code
        )

    app.run(host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()
