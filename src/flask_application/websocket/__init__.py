from .websocket import WebSocket
import threading

def init_app(app):
    ws = WebSocket()
    app.config['WEBSOCKET'] = ws
    threading.Thread(target=ws.start, args=(), daemon=True).start()