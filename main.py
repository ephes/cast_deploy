import asyncio
import subprocess

from fastapi.responses import HTMLResponse
from fastapi import BackgroundTasks, FastAPI, WebSocket

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat 4</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

OUTPUT={"foo": []}

@app.get("/")
async def get():
    return HTMLResponse(html)


ws = None


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global ws
    ws = websocket
    while True:
        data = await websocket.receive_text()
        print(f"received data: {data}")
        output = ''.join(OUTPUT['foo'])
        await websocket.send_text(f"Message text was: {output}")


async def run_deploy():
    print("running deployment")
    proc = await asyncio.create_subprocess_shell(
        #"./deploy_cast_hosting.sh",
        "./sample.sh",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    while True:
        data = await proc.stdout.readline()
        if len(data) == 0:
            break
      
        data = data.decode('UTF-8')
        print("data: ", data, end="")
        await ws.send_text(data)

    print('return code:', proc.returncode)
    print("deployment complete")


@app.post("/deploy")
async def deploy(background_tasks: BackgroundTasks):
    print("received deploy event")
    background_tasks.add_task(run_deploy)
    return {"message": "deploying"}