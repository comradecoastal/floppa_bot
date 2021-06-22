from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from bot_commander import Commander

class BotServer:

    def __init__(self, api_token: str, group_id: int, name: str="default") -> None:
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
        self.vk_api = self.vk.get_api()

        # Get long-poll object
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)

        # Self peers and corresponding commanders:
        self.users = dict()


    def send_msg(self, peer_id: int, message: str, attach: str=None) -> None:
        """
        Send specified message to peer

        :param int peer_id: The id of the peer (user, chat, community) that will recieve the message
        :param str message: The message text 
        """

        # Call the messages.send method from vk api
        if attach is None:
            self.vk_api.messages.send(peer_id=peer_id, message=message, random_id=0)
        else:
            self.vk_api.messages.send(peer_id=peer_id, message=message, random_id=0, attachment=attach)


    def start(self) -> None:
        """
        Starts listening and responding to long-poll events. 
        """

        # Looping over events
        for event in self.long_poll.listen():

            # Picking out incoming message events
            if event.type == VkBotEventType.MESSAGE_NEW:

                # Get peer and sender id
                peer_id = event.object.message["peer_id"]
                sender_id = event.object.message["from_id"]
                message_text = event.object.message["text"]

                # Group chat response
                if event.object.message["id"] == 0:

                    if peer_id not in self.users:
                        self.users[peer_id] = Commander(self.vk, peer_id)

                    text, attach = self.users[peer_id].input(event.object.message)

                    self.send_msg(peer_id, text, attach)

                # Private chat response
                else:

                    if peer_id not in self.users:
                        self.users[peer_id] = Commander(self.vk, peer_id)

                    text, attach = self.users[peer_id].input(event.object.message)

                    self.send_msg(peer_id, text, attach)


    def get_username(self, user_id: int) -> tuple:
        """
        Returns first and second name of user with a given id

        :param int user_id: The id of the user
        :returns: Tuple with first name and second name
        :rtype: tuple(str, str)
        """

        data = self.vk_api.users.get(user_ids=user_id)[0]
        return data["first_name"], data["last_name"]  
