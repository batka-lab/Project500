import subprocess

print("Batka AI запущен!")

while True:
    command = input("Что нужно сделать? ").strip().lower()

    if command == "помощь":
        print("Доступные команды:")
        print("- помощь")
        print("- открыть блокнот")
        print("- привет")
        print("- выйти")

    elif command == "открой блокнот":
        print("Открываю блокнот...")
        subprocess.Popen(["notepad.exe"])

    elif command == "привет":
        print("Привет! Batka AI на связи.")

    elif command == "выйти":
        print("Завершение работы программы...")
        break

    else:
        print("Неизвестная команда. Введите 'помощь' для списка доступных команд.")