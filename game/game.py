def game(game_file):
    
    def text():



    commands = {}

    while True:
        line = game_file.readline()
        print(line, end='')

        if line.strtswith('/'):
            command, arg = *line[1:].split(maxsplit=1)
            commands[command](arg)

        if not line:
            break


if __name__ == "__main__":
    with open("gametext.txt", "r") as game_file:
        game(game_file)
