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

