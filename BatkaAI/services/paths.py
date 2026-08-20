from pathlib import Path


def get_folder_path(folder):
    folders = {
        "desktop": Path.home() / "Desktop",
        "downloads": Path.home() / "Downloads",
        "documents": Path.home() / "Documents",
        "pictures": Path.home() / "Pictures",
        "music": Path.home() / "Music",
        "videos": Path.home() / "Videos"
    }

    return folders.get(folder)


def get_search_locations():
    return [
        Path.home() / "Desktop",
        Path.home() / "Downloads",
        Path.home() / "Documents"
    ]