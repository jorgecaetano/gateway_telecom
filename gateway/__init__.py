from flask import Flask

from gateway.rest_resources.dialer.handler import dialer_bp


def create_app():
    """Método que criar a instancia app do Flask"""

    app = Flask(__name__)
    app.register_blueprint(dialer_bp)

    return app
