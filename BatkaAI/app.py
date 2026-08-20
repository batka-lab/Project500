from actions import open_notepad, open_browser, search_web, create_file
from brain import understand_command

print("Batka AI запущен!")

while True:
    command = input("Что нужно сделать? ").strip().lower()

    intent = understand_command(command)

    action = intent["action"]
    query = intent.get("query", "")
    filename = intent.get("filename", "")
    content = intent.get("content", "")

    if action == "HELP":
        print("Доступные команды:")
        print("- помощь")
        print("- открыть блокнот")
        print("- открыть браузер")
        print("- найти что-нибудь в интернете")
        print("- создать текстовый файл")
        print("- привет")
        print("- выйти")

    elif action == "OPEN_NOTEPAD":
        open_notepad()

    elif action == "OPEN_BROWSER":
        open_browser()

    elif action == "SEARCH_WEB":
        search_web(query)

    elif action == "CREATE_FILE":
        create_file(filename, content)

    elif action == "HELLO":
        print("Привет! Batka AI на связи.")

    elif action == "EXIT":
        print("Завершение работы программы...")
        break

    else:
        print("Не удалось понять команду.")