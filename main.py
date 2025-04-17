#!/usr/bin/env python3
import asyncio
import os
import sys
print("Python executable:", sys.executable)
print("sys.path:", sys.path)

from api.server import run_fastapi_server
from api.websocket import start_websocket_server

async def run_servers():
    fastapi_task = asyncio.create_task(run_fastapi_server())
    websocket_task = asyncio.create_task(start_websocket_server())
    await asyncio.gather(fastapi_task, websocket_task)
asyncio.run(run_servers())






