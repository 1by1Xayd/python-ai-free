Here's a quick showcase of this library; and how to use it:

Standart usage:
```python
from freeai4everyone import Chat, Message

# Create a chat instance
chat = Chat(model="gpt-4o")

# Send a message
response = chat.send_message(Message(content="What is the weather today?", role="user"))

# Print the response
print(response)
```

Image generation:
```python
from freeai4everyone import Chat, Message, MODES

# Create a chat instance
chat = Chat(model="gpt-4o")

# Enable image generation mode
chat.agent_mode = MODES.IMAGE_GENERATION

# Send a message to generate an image
response = chat.send_message(
    Message(
        content="Generate a realistic image of a sunset over mountains",
        role="user"
    )
)

# Print the URL
print(response)
```
