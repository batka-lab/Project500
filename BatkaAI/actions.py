import subprocess


def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
        print("Блокнот успешно открыт.")
    except Exception as e:
        print(f"Ошибка при открытии блокнота: {e}")
def open_browser():
    try:
        subprocess.Popen(["cmd", "/c", "start", "https://www.google.com"])
        print("Браузер успешно открыт.")
    except Exception as e:
        print(f"Ошибка при открытии браузера: {e}")