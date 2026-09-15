# config.py
import os
import sys

# Пароли приложения
ADMIN_PASSWORD = "TEST_OVIK"
EXCEL_PASSWORD = "TEST_OVIK"  # Ключ для дешифрования файлов вопросов .dat

# Определение базовой директории проекта (работает на ПК и в скомпилированном APK)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Настройки тестирования по умолчанию (изменяются через админку)
settings = {
    "mode": "контрольные вопросы",
    "num_questions": 25,          
    "time_limit_minutes": 15,     
    "passing_score": 20,          
}

# Список выбранных администратором файлов источников
# Если список пуст, вопросы загружаются из всех доступных документов
SELECTED_SOURCES = []
