from .client import CustomClient

def init_app(app):
    app.client = CustomClient()