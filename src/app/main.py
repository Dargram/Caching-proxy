from quart import Quart
from src.app.routes import proxy_bp
from src.utils.logging import setup_logging
from src.utils.config import load_config

def create_app():
    setup_logging()
    app = Quart(__name__)
    app.register_blueprint(proxy_bp)
    return app

app = create_app()

if __name__ == "__main__":
    config = load_config()
    app.run(host=config['server']['host'], port=config['server']['port'])
