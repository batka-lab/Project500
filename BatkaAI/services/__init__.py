# BatkaAI.services package
#
# ВАЖНО:
# Здесь специально нет импортов из BatkaAI.actions,
# чтобы не создавать циклические импорты.
#
# Сервисы импортируются напрямую, например:
#
# from BatkaAI.services.paths import get_folder_path
# from BatkaAI.services.task_manager import TaskManager
# from BatkaAI.services.document_reader import read_document