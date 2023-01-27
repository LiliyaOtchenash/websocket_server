import asyncio
import json
import logging

import websockets

logging.basicConfig(level=logging.INFO)
{"action": "assets", "message": {}}
{"action": "subscribe", "message": {"assetId": 4}}

async def handler():
    uri = 'ws://localhost:8080'
    async with websockets.connect(uri) as websocket:
        ask_assets_list = {'action': 'assets', 'message': {}}
        await websocket.send(json.dumps(ask_assets_list))
        assets_list = await websocket.recv()
        logging.info(f'<<< {assets_list}')
        name = input('What asset do you need (from 1 to 5)')
        ask_for_subscriptions = {
            'action': 'subscribe', 'message': {'assetId': int(name)}}
        await websocket.send(json.dumps(ask_for_subscriptions))
        while True:
            messages = await websocket.recv()
            logging.info(f'>>> {messages}')
            await websocket.pong()
            messages = await websocket.recv()
            logging.info(f'>>> {messages}')

if __name__ == '__main__':
    asyncio.run(handler())
