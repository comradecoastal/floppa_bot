from bot_server import BotServer
import config

server = BotServer(config.token, config.group_id)
server.start()
