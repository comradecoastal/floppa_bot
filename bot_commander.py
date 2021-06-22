from vk_api import VkApi
from vk_api.upload import VkUpload



class Commander:

    def __init__(self, vk: VkApi, peer_id: int) -> None:

        self.peer_id = peer_id
        self.vk = vk
        self.vk_api = vk.get_api()
        self.upload = VkUpload(self.vk)
        self.photos = {'nobingus': self.upload_image('images/NOCyberbing.png', peer_id),
                       'bingus': self.upload_image('images/Cyberbing.png', peer_id),
                       'floppa': self.upload_image('images/Cyberflop.png', peer_id)}


    def get_username(self, user_id: int) -> tuple:
        """
        Returns first and second name of user with a given id

        :param int user_id: The id of the user
        :returns: Tuple with first name and second name
        :rtype: tuple(str, str)
        """

        data = self.vk_api.users.get(user_ids=user_id)[0]
        return data["first_name"], data["last_name"]  


    def upload_image(self, path, id) -> str:
        
        arr = self.upload.photo_messages(path, id)
        return f"photo{arr[0]['owner_id']}_{arr[0]['id']}"


    def input(self, message: dict) -> str:
        text = message['text']
        sender_id = message['from_id']
        peer_id = message['peer_id']

        if text.startswith('танцуй'):
            return "Floppadan dance to music", "video-129440544_456249641"
        else:
            first_name, second_name = self.get_username(sender_id)

            if 'bingus' in text.lower():
                return f"Floppadan Floppashevich says: for the use of word \"bingus\" {first_name} {second_name} must be executed!", self.photos['nobingus']
            else:
                return f"Floppadan Floppashevich considers {first_name} {second_name}\'s words: \"{text}\" to be very stupid", self.photos['floppa']