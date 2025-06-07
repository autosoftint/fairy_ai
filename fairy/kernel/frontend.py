# -*- coding: utf-8 -*-
# cython: language_level=3
import json
import os
import uvicorn
import aiofiles
import traceback
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.websockets import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from websockets.asyncio.client import connect
from lib.version import VERSION
from lib import path
from config import driver as driver_config, agent as agent_config

app = FastAPI(title="Fairy Localhost Server",
              version=VERSION,)
# Mount the static file from the web directory.
app.mount("/static", StaticFiles(directory=path.PATH_WEB_STATIC), name="static")
# Construct the homepage path.
path_homepage: str = os.path.join(path.PATH_WEB, "index.html")
# Prepare the homepage cache.
homepage_modified: float | None = None
homepage_cache: str = ""
# Prepare the client message queue.
client_socket: WebSocket | None = None


class ChatContent(BaseModel):
    mode: str
    text: Optional[str] = None


@app.get("/ui_settings", response_class=JSONResponse)
async def fetch_ui_settings():
    return JSONResponse({"code": 200,
                         "result": agent_config.UI_SETTINGS})


@app.post("/chat", response_class=JSONResponse)
async def start_chat(request: ChatContent):
    try:
        # Send request to agent.
        async with connect(f"ws://127.0.0.1:{driver_config.AGENT_PORT}") as ws:
            # Construct the payload command.
            payload: dict = {"op": "start", "mode": request.mode}
            if request.mode == "text":
                payload["text"] = request.text
            # Send the user payload to the worker agent socket.
            await ws.send(json.dumps(payload))
            # Read the replied JSON value.
            return JSONResponse(json.loads(await ws.recv()))
    except Exception as e:
        print(f"Error happens during start chat: {e}")
        return JSONResponse({"code": 503})


@app.post("/stop")
async def stop():
    try:
        # Send request to agent.
        async with connect(f"ws://127.0.0.1:{driver_config.AGENT_PORT}") as ws:
            # Send the command to socket.
            await ws.send(json.dumps({"op": "stop"}))
            # Read the replied JSON value, send back to frontend.
            return JSONResponse(json.loads(await ws.recv()))
    except Exception as e:
        print(f"Error happens during start chat: {e}")
        return JSONResponse({"code": 500})


@app.get("/", response_class=HTMLResponse)
async def homepage():
    # This serves the index.html for the root path, check file existence.
    if os.path.isfile(path_homepage):
        global homepage_cache
        # Check whether the homepage is loaded.
        current_timestamp: float = os.path.getmtime(path_homepage)
        if homepage_modified is None or current_timestamp > homepage_modified:
            # Need to update the homepage cache.
            async with aiofiles.open(path_homepage, "r", encoding="utf-8") as homepage_file:
                homepage_cache = await homepage_file.read()
        # Provide the content as HTMLResponse.
        return HTMLResponse(homepage_cache)
    raise HTTPException(status_code=404)


@app.websocket("/send")
async def send_message_to_client(websocket: WebSocket):
    # Loop and accept the socket.
    try:
        await websocket.accept()
        while True:
            # Re-route the request to the web client.
            request: dict = await websocket.receive_json()
            # Check whether the client socket exists.
            if client_socket is not None:
                await client_socket.send_json(request)
    except WebSocketDisconnect:
        pass


@app.websocket("/")
async def client_message_queue(incoming_socket: WebSocket):
    global client_socket
    # Check whether there is already a client accessing.
    if client_socket is not None:
        # Already got one connecting.
        return
    # Accept the client socket.
    try:
        # Save the incoming socket as the global socket.
        client_socket = incoming_socket
        await client_socket.accept()
        # Keep the connection, ignoring all the incoming message.
        client_not_closed: bool = True
        while client_not_closed:
            client_message: dict = dict(await client_socket.receive())
            # Update the client closed message
            client_not_closed = client_message["type"] != "websocket.disconnect"
    except WebSocketDisconnect:
        pass
    except Exception:
        print(f"Error happens during message queue:\n{traceback.format_exc()}")
    finally:
        # Reset the client socket.
        client_socket = None


def main() -> None:
    print(f"starting frontend server at http://127.0.0.1:{driver_config.FRONTEND_PORT}/", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=driver_config.FRONTEND_PORT,
                ws_ping_timeout=3600,
                log_level=driver_config.FRONTEND_LOG)


if __name__ == "__main__":
    main()
