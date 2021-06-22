from vk_api import VkApi
import vk_api
from vk_api.vk_api import VkApiMethod

class Commander:

    def __init__(self, vk_api: VkApiMethod) -> None:
        self.vk_api = vk_api


    def get_username(self, user_id: int) -> tuple:
        """
        Returns first and second name of user with a given id

        :param int user_id: The id of the user
        :returns: Tuple with first name and second name
        :rtype: tuple(str, str)
        """

        data = self.vk_api.users.get(user_ids=user_id)[0]
        return data["first_name"], data["last_name"]  



    def input(self, message: dict) -> str:
        text = message['text']
        sender_id = message['from_id']

        if text.startswith('/'):
            return "Floppadan does not understand you"
        else:

            first_name, second_name = self.get_username(sender_id)
            return f"Floppadan Floppashevich considers {first_name} {second_name}\'s the words: \"{text}\" to be very stupid"