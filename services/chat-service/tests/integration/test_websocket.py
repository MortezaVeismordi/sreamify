import pytest
from channels.testing import WebsocketCommunicator
from config.asgi import application


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_connection():
    communicator = WebsocketCommunicator(application, "/ws/chat/1/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()
