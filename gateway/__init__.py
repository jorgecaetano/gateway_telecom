from flask import Flask

from gateway.rest_resources.dialer.handler import dialer_bp
from gateway.rest_resources.report.handler import report_bp


def create_app():
    """Método que criar a instancia app do Flask"""

    app = Flask(__name__)
    app.register_blueprint(dialer_bp)
    app.register_blueprint(report_bp)

    return app
