from flopmessage import Message, MessageType

class Game:

    def __init__(self, game_file):
        self.game_file = game_file

        self.input = None
        self.last_choice = None
        self.wait_for_answer = False

        self.current_line = None
        self.update_line()

    def update_line(self):
        self.current_line = self.game_file.readline()

    def command_handler(self):
        command = self.current_line.split('{')[0][1:].strip()
        if command == "title":
            message = self.module_title()
        elif command == "text":
            message = self.module_text()
        elif command == "speaker":
            message = self.module_speaker()
        elif command == "mulchoice":
            message = self.module_mulchoice()
        else:
            return
        return message

    def extract_braces(self):
        pos_1 = self.current_line.find('{')
        pos_2 = self.current_line.find('}')
        while pos_1 == -1:
            self.update_line()
            pos_1 = self.current_line.find('{')
            pos_2 = self.current_line.find('}')
        if pos_2 != -1:
            text = self.current_line[pos_1 + 1:pos_2]
        else:
            text = self.current_line[pos_1 + 1:]
            self.update_line()
            pos_2 = self.current_line.find('}')
            while pos_2 == -1:
                text += self.current_line
                self.update_line()
                pos_2 = self.current_line.find('}')
            text += self.current_line[:pos_2]
        return text.strip()

    def extract_brackets(self):
        pos_1 = self.current_line.find('[')
        pos_2 = self.current_line.find(']')
        text = self.current_line[pos_1 + 1:pos_2].strip()
        return text

    def module_title(self):
        text = self.extract_braces()
        print('-' * 20, text, '-' * 20, sep='\n')
        return Message(1, text)

    def module_speaker(self):
        text = self.extract_braces()
        print('[' + text + ']')
        return Message(1, text)

    def module_text(self):
        text = self.extract_braces()
        print(text)
        return Message(1, text)

    def module_mulchoice(self):
        choices_text = self.extract_braces()
        choices = [elem.strip() for elem in choices_text.split(',')]
        text = '[' + '/'.join(choices) + '] > '
        self.choiches = choices
        self.wait_for_answer = True
        print(text)
        return Message(2, text)

    def process_choice(self):
        if self.input is not None:
            if self.input.strip().lower() in self.choiches:
                self.last_choice = self.input.strip().lower()
                self.choiches = None
                self.wait_for_answer = False
                return Message()
            
        return Message(2, "Invalid input format.\n[" + 
                        '/'.join(self.choiches) + '] > ')
        


    def step(self):
        if self.current_line.startswith('/'):
            message = self.command_handler()
        else:
            message = Message()
        self.update_line()
        return message

    def input(self, message):
        self.input = message.content


gfile = open("gamecommands.txt")
game = Game(gfile)
for i in range(10):
    game.step()

