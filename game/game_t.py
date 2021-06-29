def title(text: str):

    l = len(text)
    print('-' * l)
    print(text)
    print('-' * l)


def speaker(text: str):
    print('[' + text + ']:')


def choises(choises):
    while True:
        answer = input("[" + "/".join(choises) + "] > ").lower()
        if answer in choises:
            return answer
        print("Anser incorrect")


def main():

    title("Who wants to be a millionaire")
    speaker("Big Floppa")
    print("Welcome to who wants to be a millionaire! My name is Big floppa" \
          " and I will be your host today!")
    print("You will have to answer 10 questions to get ONE MILLION floppa" \
          " cois!")
    print("Let the questionning begin!")
    print("First question!")
    print("Is bingus gay?")
    answer = choises(["yes", "no"])
    if answer == "yes":
        print("Yes say yes! You are right!")
    elif answer == "no":
        print("You are wrong you lose!")
        return "lose"

    speaker("Big Floppa")
    print("Question TWO!!!")
    print("Floppa god?")
    answer = choises(["yes", "no", "fish"])
    if answer == "yes":
        print("Genius")
    elif answer == "no":
        print("You stupid? You lose!")
        print("You loose!")
        return "lose"
    elif answer == "fish":
        print("Genisus!")

    speaker("Big Floppa")
    print("Congratulations!! You win!!!!")
    return "win"


main()
