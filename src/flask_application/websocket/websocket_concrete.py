# TODO: Refactor this code
# https://github.com/OwOHamper/Valorant-Websocket-Logger-Python/blob/main/wss%20logger.py
# https://github.com/deadly/valorant-agent-yoinker/blob/development/src/backend/websocket.py
import ssl
import websockets
import base64

async def web_socket(lockfile: dict):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(f"wss://127.0.0.1:{lockfile['port']}",
                                  ssl=ssl_context,
                                  extra_headers={'Authorization': 'Basic ' + base64.b64encode(('riot:' + lockfile['password']).encode()).decode()}) as websocket:
        
        await websocket.send('[5, "OnJsonApiEvent"]')

        while True:
            response = await websocket.recv()
            if len(response) > 0:
                # TODO: finish this implementation
                print(response)


# asyncio.get_event_loop().run_until_complete(ws())
# asyncio.get_event_loop().run_forever()
