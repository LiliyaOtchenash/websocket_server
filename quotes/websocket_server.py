import asyncio
import os
import sys
from pathlib import Path

import websockets
import json
import collections
import logging


PROJECT_DIR = Path(__file__).resolve().parent.parent


logging.basicConfig(level=logging.INFO)


CONNECTIONS = collections.defaultdict(set)


async def handle_connections(websocket):
    sys.path.append(str(PROJECT_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    import django
    django.setup()

    try:
        async for messages in websocket:
            message = json.loads(messages)
            action = message.get('action', None)
            if action == 'assets':
                await send_assets_list(websocket)
            elif action == 'subscribe':
                asset_id = message['message']['assetId']
                await subscribe(websocket, asset_id)
                await send_asset_history(websocket, asset_id)
            elif message.get('new_points'):
                new_points = message.get('new_points')
                await send_points(new_points)

            else:
                logging.error(f'Unsupported action in message {message}')
                await websocket.wait_closed()

    finally:
        logging.error(f'<<<<<<<< Finally case {CONNECTIONS}')
        unsubscribe(websocket)


def unsubscribe(websocket):
    for queue, users_set in CONNECTIONS.items():
        if websocket in users_set:
            users_set.remove(websocket)
            return


async def subscribe(websocket, asset_id):
    unsubscribe(websocket)
    CONNECTIONS[asset_id].add(websocket)


async def send_assets_list(websocket):
    from quotes.operations import get_assets_list
    assets_list = await get_assets_list()
    if assets_list:
        await websocket.send(json.dumps(assets_list))


async def send_asset_history(websocket, asset_id):
    from quotes.operations import get_asset_history
    asset_history = await get_asset_history(asset_id)
    await websocket.send(json.dumps(asset_history))


async def send_points(points):
    for conn, point in points.items():
        connect = CONNECTIONS[int(conn)]
        if not connect or not point:
            logging.info(f'{connect}, {point}')
            continue
        logging.info(f'<<< {connect}')
        logging.info(f'<<< {point}')

        websockets.broadcast(connect, json.dumps(point))



async def main():
    async with websockets.serve(handle_connections, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
