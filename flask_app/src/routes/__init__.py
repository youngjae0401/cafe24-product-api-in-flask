from src.routes.cafe24_route import cafe24_bp

def register_blueprints(app):
    app.register_blueprint(cafe24_bp)
