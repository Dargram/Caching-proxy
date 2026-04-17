from quart import Blueprint, request, Response
from src.core.logic import forward_request
from src.utils.config import config
import logging

origin = config['proxy']['target']
proxy_bp = Blueprint('proxy', __name__)
logger = logging.getLogger("proxy_app")

@proxy_bp.route('/', defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@proxy_bp.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_handler(path):
    target_url = f"{origin.rstrip('/')}/{path}"

    headers = dict(request.headers)

    client_ip = request.remote_addr
    host_ip   = request.host
    method    = request.method

    print(f"\nMy headers: {headers}\n")

    headers.pop("Host", None)
    headers.pop("Accept-Encoding", None)

    data         = await request.get_data()
    resp         = await forward_request(target_url, headers, request.args, request.method, data)
    resp_headers = dict(resp.headers)

    resp_headers.pop("Content-Encoding", None)
    resp_headers.pop("Transfer-Encoding", None)
    resp_headers.pop("Content-Length", None)

    logger.info(
        f"\033[93m{client_ip}\033[0m \033[97m->\033[0m "
        f"\033[91m{host_ip}\033[0m "
        f"\033[94m[{method}]\033[0m "
        f"\033[97m->\033[0m  "
        f"\033[96m{target_url}\033[0m "
        f"\033[92m[{resp.status_code}]\033[0m "
    )
    return Response(
        resp.content,
        resp.status_code,
        headers={"Content-Type": resp.headers.get("Content-Type", "text/html")}
    )
