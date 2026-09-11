from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.utils.errors import register_error_handlers


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    config_class.validate()

    CORS(app)  # scope this to the actual frontend origin before production deployment

    register_error_handlers(app)

    from app.routes.detect import detect_bp
    from app.routes.authenticate import authenticate_bp
    from app.routes.verify import verify_bp

    app.register_blueprint(detect_bp)
    app.register_blueprint(authenticate_bp)
    app.register_blueprint(verify_bp)

    @app.route("/api/health")
    def health():
        return {"success": True, "data": {"status": "ok"}}

    return app
