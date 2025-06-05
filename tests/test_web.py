import importlib
import pathlib
import sys

pytest = importlib.import_module('pytest')

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from ui_app import application


def test_index_route() -> None:
    status: list[str] = []

    def start_response(code: str, _headers: list[tuple[str, str]]) -> None:
        status.append(code)

    body = b"".join(
        application({"REQUEST_METHOD": "GET", "PATH_INFO": "/"}, start_response)
    )

    assert status[0].startswith("200")
    assert b"AI Trading Bot" in body
