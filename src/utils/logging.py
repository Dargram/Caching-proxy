import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s \033[34m[%(levelname)s]\033[0m %(message)s"
    )
    for lib in ["httpx", "werkzeug", "uvicorn.error", "uvicorn.access"]:
        logging.getLogger(lib).disabled = True
    return logging.getLogger("proxy_app")
