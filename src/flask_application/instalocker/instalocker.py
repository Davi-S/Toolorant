import flask
import asyncio
import threading

instalocker_bp = flask.Blueprint('instalocker_bp', __name__,
                                 template_folder='templates')


def init_app(app: flask.Flask):
    app.register_blueprint(instalocker_bp)


class Websocket:
    def __init__(self) -> None:
        self.running = False

    async def _web_socket(self):
        print('starting ws')
        count = 0
        while self.running:
            count += 1
            await asyncio.sleep(1)

            if count >= 10:  # Match found
                # TODO: implement how to proceed when the match is found
                break

        print('stopping ws')

    def start(self):
        asyncio.run(self._web_socket())


websocket = Websocket()


@instalocker_bp.route('/start', methods=['POST'])
def start() -> bool:
    global websocket
    if websocket.running:
        return flask.jsonify({'success': False})

    websocket.running = True
    ws_t = threading.Thread(target=websocket.start, args=(), daemon=True)
    ws_t.start()
    return flask.jsonify({'success': True})


@instalocker_bp.route('/stop', methods=['POST'])
def stop() -> bool:
    global websocket
    if not websocket.running:
        return flask.jsonify({'success': False})

    websocket.running = False
    return flask.jsonify({'success': True})
