import pytest
from apps.chat.models import ChatRoom, Message


@pytest.mark.django_db
def test_chat_room_creation():
    room = ChatRoom.objects.create(stream_id=1, name="Test Room")
    assert room.stream_id == 1
    assert room.name == "Test Room"


@pytest.mark.django_db
def test_message_creation():
    room = ChatRoom.objects.create(stream_id=1, name="Test Room")
    message = Message.objects.create(room=room, user_id=1, username="testuser", content="Hello!")
    assert message.content == "Hello!"
    assert message.room == room
