import importlib
import pathlib
import sys

pytest = importlib.import_module('pytest')

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

pytest.importorskip('flask')
from ui_app import app


def test_index_route() -> None:
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
    assert b'AI Trading Bot' in res.data
