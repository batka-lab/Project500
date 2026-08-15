def understand_command(command):
    if "блокнот" in command:
        return "OPEN_NOTEPAD"

    if "браузер" in command:
        return "OPEN_BROWSER"

    if command == "привет":
        return "HELLO"

    if command == "помощь":
        return "HELP"

    if command == "выйти":
        return "EXIT"

    return "UNKNOWN"