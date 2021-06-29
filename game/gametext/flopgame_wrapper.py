from flopmessage import Message, MessageType
import os
import flopgame

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "gamecommands.txt")
gfile = open(filename)
game = flopgame.Game(gfile)

while True:
    message = game.step()

    if message.type == MessageType.TEXT:
        print(message.content)
    elif message.type == MessageType.REQUEST:
        text = input(message.content)
        game.input(Message(1, text))
    elif message.type == MessageType.STOP:
        break
