import os
from flopmessage import Message, MessageType

class Game:

    def __init__(self, game_file):
        self.game_file = game_file

        self.last_message = Message()
        self.last_input = None
        self.last_choice = None
        self.wait_for_answer = False

        self.current_line = None
        self.update_line()

    def update_line(self):
        self.current_line = self.game_file.readline()

    def command_handler(self):
        command = self.extract_command()
        if command == "title":
            message = self.module_title()
        elif command == "text":
            message = self.module_text()
        elif command == "speaker":
            message = self.module_speaker()
        elif command == "mulchoice":
            message = self.module_mulchoice()
        elif command == "choice":
            message = self.module_choice()
        elif command == "jumpcond":
            message = self.module_jumpcond()
        elif command == "end":
            message = Message(9)
        else:
            message = Message()
        return message

    def extract_command(self):
        pos_2 = None
        for i in range(1, len(self.current_line)):
            if self.current_line[i] in ' [{':
                pos_2 = i
                break
        text = self.current_line[1:pos_2]
        return text

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
        text = '-' * 20 + '\n' + text + '\n' + '-' * 20
        # print('-' * 20, text, '-' * 20, sep='\n')
        return Message(1, text)

    def module_speaker(self):
        text = self.extract_braces()
        text = '[' + text + ']'
        # print('[' + text + ']')
        return Message(1, text)

    def module_text(self):
        text = self.extract_braces()
        # print(text)
        return Message(1, text)

    def module_mulchoice(self):
        choices_text = self.extract_braces()
        choices = [elem.strip() for elem in choices_text.split(',')]
        text = '[' + '/'.join(choices) + '] > '
        self.choiches = choices
        self.wait_for_answer = True
        # print(text)
        return Message(2, text)

    def module_choice(self):
        choice = self.extract_brackets()
        if choice == self.last_choice:
            text = self.extract_braces()
            message = Message(1, text)
        else:
            message = Message()
        return message

    def module_jumpcond(self):
        cond = self.extract_brackets()
        if cond == self.last_choice:
            while not (self.current_line.startswith("#") and \
                self.current_line[1:].strip() == self.last_choice) and \
                self.current_line != '':
                self.update_line()
        return Message()

    def process_choice(self):
        if self.last_input is not None:
            if self.last_input.strip().lower() in self.choiches:
                self.last_choice = self.last_input.strip().lower()
                self.choiches = None
                self.wait_for_answer = False
                return Message()
            
        return Message(2, "Invalid input format.\n[" + 
                        '/'.join(self.choiches) + '] > ')
        
    def step(self):
        if not self.wait_for_answer:
            if self.current_line.startswith('/'):
                message = self.command_handler()
            else:
                message = Message()
            self.update_line()
        else:
            message  = self.process_choice()
            
        self.last_message = message
        return message

    def input(self, message):
        self.last_input = message.content


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "gamecommands.txt")
gfile = open(filename)
game = Game(gfile)


