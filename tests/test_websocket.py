import asyncio
import json
import websockets
from drunken_team.routes.serve_dashboard import telemetry_ws_handler


def test_telemetry_ws_handler_unauthorized(monkeypatch):
    monkeypatch.setenv("EDGE_TELEMETRY_API_KEY", "secret-key-123")

    async def run_test():
        async with websockets.serve(telemetry_ws_handler, "localhost", 8282):
            try:
                async with websockets.connect(
                    "ws://localhost:8282/ws/telemetry?token=wrong"
                ) as _ws:
                    await _ws.recv()
                assert False, "Should have raised ConnectionClosed"
            except websockets.exceptions.ConnectionClosed as e:
                assert e.code == 4001

    asyncio.run(run_test())


def test_telemetry_ws_handler_authorized(monkeypatch):
    monkeypatch.setenv("EDGE_TELEMETRY_API_KEY", "secret-key-123")

    async def run_test():
        async with websockets.serve(telemetry_ws_handler, "localhost", 8383):
            async with websockets.connect(
                "ws://localhost:8383/ws/telemetry?token=secret-key-123"
            ) as ws:
                await ws.send(json.dumps({"telemetry": "test"}))
                response = await ws.recv()
                data = json.loads(response)
                assert data["status"] == "received"
                assert data["data"]["telemetry"] == "test"

    asyncio.run(run_test())


def test_telemetry_ws_handler_no_key(monkeypatch):
    monkeypatch.delenv("EDGE_TELEMETRY_API_KEY", raising=False)

    async def run_test():
        async with websockets.serve(telemetry_ws_handler, "localhost", 8484):
            try:
                async with websockets.connect(
                    "ws://localhost:8484/ws/telemetry?token=secret"
                ) as _ws:
                    await _ws.recv()
                assert False, "Should have raised ConnectionClosed"
            except websockets.exceptions.ConnectionClosed as e:
                assert e.code == 1011

    asyncio.run(run_test())
