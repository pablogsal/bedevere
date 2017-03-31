from aiohttp import web
import pytest

from bedevere import __main__ as main


async def test_success(test_client):
    app = web.Application()
    app.router.add_post("/", main.main)
    client = await test_client(app)
    headers = {"x-github-event": "pull_request",
               "x-github-delivery": "1234"}
    # Sending a payload that shouldn't trigger any networking, but no errors
    # either.
    data = {"action": "closed"}
    response = await client.post("/", headers=headers, json=data)
    assert response.status == 200


async def test_failure(test_client):
    """Even in the face of an exception, the server should not crash."""
    app = web.Application()
    app.router.add_post("/", main.main)
    client = await test_client(app)
    # Missing key headers.
    response = await client.post("/", headers={})
    assert response.status == 500
