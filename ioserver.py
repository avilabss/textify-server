import socketio
from helpers import getTextFromBase64

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print(sid, "CONNECTED")


@sio.event
async def getText(sid, data):
    print(">>>>>>>>>>>>>TRIGGERED<<<<<<<<<<<<<<<<<<<")
    b64_string = "".join(data.split(",")[1]).encode("utf-8")
    text = getTextFromBase64(b64_string)
    print(text)
    await sio.emit("text", text, to=sid)


@sio.event
async def disconnect(sid):
    print(sid, "DISCONNECTED")
