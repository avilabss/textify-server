import socketio
import json
from helpers import processTextifyRequest

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)

online = 0
like = 0


@sio.event
async def connect(sid, environ):
    print(f"[CONNECTED] {sid}")
    global online
    online += 1

    await sio.emit("serverStats", json.dumps({"online": online, "like": like}), to=sid)
    await sio.emit("updateOnline", online)


@sio.event
async def getText(sid, data):
    await processTextifyRequest(sio=sio, sid=sid, data=data)


@sio.event
async def doLike(sid):
    global like
    like += 1
    await sio.emit("updateLike", like)


@sio.event
async def disconnect(sid):
    print(f"[DISCONNECTED] {sid}")
    global online

    online -= 1
    await sio.emit("updateOnline", online)
