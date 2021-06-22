from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll


class BotServer:

    def __init__(self, api_token: str, group_id: int, name: str="default"):
        """
        Set up server for group with corresponding token

        :param str api_token: The api token for your vk group
        :param int grop_id: The id of the corresponding group
        :param str name: The name of your server
        """

        self.name = name
        self.group_id = group_id

        # Get VkApi object, and corresponding vk api interface
        self.vk = VkApi(token=api_token)
        self.vk_api = self.vk.get_api

        # Get long-poll object
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)


    def send_msg(self, peer_id: int, message: str):
        """
        Send specified message to peer

        :param int peer_id: The id of the peer (user, chat, community) that will recieve the message
        :param str message: The message text 
        """

        # Call the messages.send method from vk api
        self.vk_api.messages.send(peer_id=peer_id, message=message, random_id=0)


    def start(self):
        """
        Starts listening and responding to long-poll events. 
        """

        # Looping over events
        for event in self.long_poll.listen():
            # Picking out incoming message events
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(event)

