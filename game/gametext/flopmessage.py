from enum import Enum

class MessageType(Enum):
    NULL = 0
    TEXT = 1
    REQUEST = 2
    STOP = 9


class Message:

    def __init__(self, type=0, content=None):
        self.type = MessageType(type)
        self.content = content

    def __repr__(self):
        return 'Message({type}, {content})'.format(type=str(self.type),
                                                   content=repr(self.content))

