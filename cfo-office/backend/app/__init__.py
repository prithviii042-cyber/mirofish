from flask import Flask
from flask_cors import CORS

# In-memory store shared across request handlers
store = {
    "documents": [],
    "kpis": [],
    "scenarios": [],
    "reports": [],
}


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.api import dashboard_bp, scenario_bp, report_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(scenario_bp)
    app.register_blueprint(report_bp)

    @app.route("/api/health")
    def health():
        return {"status": "ok", "model": "claude-opus-4-6"}

    return app
