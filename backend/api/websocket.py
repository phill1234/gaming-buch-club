import logging

import aiopg
import async_timeout
import psycopg2
from fastapi import APIRouter, WebSocket
from django.conf import settings
import asyncio
import redis.asyncio as redis

from project.settings import default_database_url

websocket_router = APIRouter()


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await postgres_connector(websocket)


async def redis_connector(websocket):
    redis_client = await redis.from_url(settings.CACHE_URL)
    async with redis_client.pubsub() as pubsub:
        await pubsub.subscribe("notifications")

        async def read_messages(channel):
            # wait for incoming events
            while True:
                try:
                    async with async_timeout.timeout(1):
                        message = await pubsub.get_message(
                            ignore_subscribe_messages=True
                        )
                        if message is not None:
                            print(f"(Reader) Message Received: {message}")
                            await websocket.send_text(message["data"].decode("utf-8"))
                except asyncio.TimeoutError:
                    pass

        await asyncio.create_task(read_messages(pubsub))


async def postgres_connector(websocket):
    conn = await aiopg.connect(default_database_url)
    async with conn.cursor() as cur:
        await cur.execute("LISTEN notifications;")
        while True:
            try:
                msg = await conn.notifies.get()
            except psycopg2.Error as exception:
                logging.error(exception)
                continue
            await websocket.send_text(msg.payload)
