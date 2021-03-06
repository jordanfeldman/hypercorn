import pytest

from hypercorn.middleware import HTTPToHTTPSRedirectMiddleware
from .helpers import empty_framework


@pytest.mark.asyncio
async def test_http_to_https_redirect_middleware_http() -> None:
    app = HTTPToHTTPSRedirectMiddleware(empty_framework, "localhost")
    sent_events = []

    async def send(message: dict) -> None:
        nonlocal sent_events
        sent_events.append(message)

    scope = {"type": "http", "scheme": "http", "path": "/abc", "query_string": b"a=b"}
    await app(scope, None, send)  # type: ignore

    assert sent_events == [
        {
            "type": "http.response.start",
            "status": 307,
            "headers": [(b"location", b"https://localhost/abc?a=b")],
        },
        {"type": "http.response.body"},
    ]


@pytest.mark.asyncio
async def test_http_to_https_redirect_middleware_websocket() -> None:
    app = HTTPToHTTPSRedirectMiddleware(empty_framework, "localhost")
    sent_events = []

    async def send(message: dict) -> None:
        nonlocal sent_events
        sent_events.append(message)

    scope = {
        "type": "websocket",
        "scheme": "ws",
        "path": "/abc",
        "query_string": b"a=b",
        "extensions": {"websocket.http.response": {}},
    }
    await app(scope, None, send)  # type: ignore

    assert sent_events == [
        {
            "type": "websocket.http.response.start",
            "status": 307,
            "headers": [(b"location", b"wss://localhost/abc?a=b")],
        },
        {"type": "websocket.http.response.body"},
    ]


@pytest.mark.asyncio
async def test_http_to_https_redirect_middleware_websocket_http2() -> None:
    app = HTTPToHTTPSRedirectMiddleware(empty_framework, "localhost")
    sent_events = []

    async def send(message: dict) -> None:
        nonlocal sent_events
        sent_events.append(message)

    scope = {
        "type": "websocket",
        "http_version": "2.0",
        "scheme": "ws",
        "path": "/abc",
        "query_string": b"a=b",
        "extensions": {"websocket.http.response": {}},
    }
    await app(scope, None, send)  # type: ignore

    assert sent_events == [
        {
            "type": "websocket.http.response.start",
            "status": 307,
            "headers": [(b"location", b"https://localhost/abc?a=b")],
        },
        {"type": "websocket.http.response.body"},
    ]


@pytest.mark.asyncio
async def test_http_to_https_redirect_middleware_websocket_no_rejection() -> None:
    app = HTTPToHTTPSRedirectMiddleware(empty_framework, "localhost")
    sent_events = []

    async def send(message: dict) -> None:
        nonlocal sent_events
        sent_events.append(message)

    scope = {
        "type": "websocket",
        "http_version": "2.0",
        "scheme": "ws",
        "path": "/abc",
        "query_string": b"a=b",
    }
    await app(scope, None, send)  # type: ignore

    assert sent_events == [{"type": "websocket.close"}]
