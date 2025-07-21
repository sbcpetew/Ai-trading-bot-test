import asyncio
from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()
metrics: Dict[str, float] = {
    "unrealised_pnl": 0.0,
    "realised_pnl": 0.0,
    "sharpe": 0.0,
    "drawdown": 0.0,
    "win_rate": 0.0,
    "trades_today": 0,
}

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Metrics</title>
</head>
<body>
<h1>AlphaFive Metrics</h1>
<ul id="metrics"></ul>
<script>
const ws = new WebSocket('ws://' + location.host + '/ws/metrics');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const ul = document.getElementById('metrics');
    ul.innerHTML = '';
    Object.entries(data).forEach(([k,v]) => {
        const li = document.createElement('li');
        li.textContent = `${k}: ${v}`;
        ul.appendChild(li);
    });
};
</script>
</body>
</html>
"""


@app.get("/")
async def index():
    return HTMLResponse(html)


@app.websocket("/ws/metrics")
async def ws_metrics(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_json(metrics)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
