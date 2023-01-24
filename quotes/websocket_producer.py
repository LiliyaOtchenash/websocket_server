import asyncio
import json
import logging
import os
import sys
from pathlib import Path
import websockets

PROJECT_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(level=logging.INFO)


async def handler():
    sys.path.append(str(PROJECT_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

    import django

    django.setup()

    uri = 'ws://localhost:8080'
    async with websockets.connect(uri) as websocket:
        while True:
            points = await update_points()
            logging.info(f'<<<< {points}')
            await websocket.send(json.dumps(points))
            await asyncio.sleep(1)


async def update_points():
    from quotes.operations import get_updates, get_currencies_from_list,\
        write_new_points_and_prepare_response
    data = await get_updates()
    handled_data = await get_currencies_from_list(data)
    points = await write_new_points_and_prepare_response(handled_data)
    return {'new_points': points}


if __name__ == '__main__':
    asyncio.run(handler())

