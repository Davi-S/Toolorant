from .client import CustomClient

def init_app(app):
    # Using "na" as region if none is given or found
    app.client = CustomClient('na')