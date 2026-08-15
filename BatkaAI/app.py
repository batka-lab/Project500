from actions import open_notepad, open_browser
from brain import understand_command

print("Batka AI запущен!")

while True:
    command = input("Что нужно сделать? ").strip().lower()

    intent = understand_command(command)

    if intent == "HELP":
        print("Доступные команды:")
        print("- помощь")
        print("- открыть блокнот")
        print("- открыть браузер")
        print("- привет")
        print("- выйти")

    elif intent == "OPEN_NOTEPAD":
        open_notepad()

    elif intent == "OPEN_BROWSER":
        open_browser()

    elif intent == "HELLO":
        print("Привет! Batka AI на связи.")

    elif intent == "EXIT":
        print("Завершение работы программы...")
        break

    else:
        print("Не удалось понять команду.")