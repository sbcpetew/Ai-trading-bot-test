from __future__ import annotations

import sys
import threading
from typing import Any, Callable

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    def load_dotenv() -> None:
        """Stub if python-dotenv is not installed."""
        pass

from wsgiref.simple_server import make_server

load_dotenv()

_log: list[str] = []
_log_lock = threading.Lock()


def _append(message: str) -> None:
    with _log_lock:
        _log.append(message)


def _log_text() -> str:
    with _log_lock:
        return "\n".join(_log)


# ---------------------------------------------------------------------------
# Thin wrappers around CLI modules


def train_agent() -> str:
    """Run the training module."""
    from alphafive import train

    argv = sys.argv[:]
    sys.argv = ["train"]
    try:
        train.main()
    finally:
        sys.argv = argv
    return "done"


def run_paper() -> str:
    """Run the paper trading module."""
    from alphafive import paper

    argv = sys.argv[:]
    sys.argv = ["paper"]
    try:
        paper.main()
    finally:
        sys.argv = argv
    return "done"


def run_live() -> str:
    """Run the live trading module with confirmation."""
    from alphafive import live

    argv = sys.argv[:]
    sys.argv = ["live", "--confirm"]
    try:
        live.main()
    finally:
        sys.argv = argv
    return "done"


# ---------------------------------------------------------------------------
# Web server helpers


def _run_task(func: Callable[[], Any], name: str) -> None:
    def target() -> None:
        _append(f"\u25ba {name} started …")
        try:
            result = func()
            _append(f"\u2713 {name} finished: {result}")
        except Exception as exc:  # pragma: no cover - runtime error display
            _append(f"\u2717 {name} error: {exc}")

    threading.Thread(target=target, daemon=True).start()


INDEX_HTML = """<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<title>AI Trading Bot</title>
<script>
function start(name){ fetch('/run/'+name,{method:'POST'}); }
function update(){
    fetch('/log').then(r=>r.text()).then(t=>{
        const pre=document.getElementById('log');
        pre.textContent=t;
        pre.scrollTop=pre.scrollHeight;
    });
}
setInterval(update,1000);
</script>
</head>
<body>
<button onclick=\"start('train')\">Train</button>
<button onclick=\"start('paper')\">Paper Trade</button>
<button onclick=\"start('live')\">Live Trade</button>
<pre id='log' style='height:300px;overflow-y:auto;border:1px solid #ccc'></pre>
</body>
</html>"""


def application(environ: dict[str, Any], start_response: Callable[..., Any]):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")

    if method == "GET" and path == "/":
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [INDEX_HTML.encode()]

    if method == "GET" and path == "/log":
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
        return [_log_text().encode()]

    if method == "POST" and path.startswith("/run/"):
        task = path.split("/")[-1]
        mapping: dict[str, tuple[Callable[[], Any], str]] = {
            "train": (train_agent, "Train"),
            "paper": (run_paper, "Paper Trade"),
            "live": (run_live, "Live Trade"),
        }
        item = mapping.get(task)
        if not item:
            start_response("400 Bad Request", [("Content-Type", "text/plain")])
            return [b"Unknown task"]
        _run_task(*item)
        start_response("204 No Content", [])
        return [b""]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not Found"]


def main() -> None:
    with make_server("0.0.0.0", 8000, application) as server:
        server.serve_forever()


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
