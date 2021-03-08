import socketio
from helpers import processTextifyRequest

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print(f"[CONNECTED] {sid}")


@sio.event
async def getText(sid, data):
    await processTextifyRequest(sio=sio, sid=sid, data=data)


@sio.event
async def disconnect(sid):
    print(f"[DISCONNECTED] {sid}")
