[app]
# (string) Title of your application
title = Тестирование ОВиК

# (string) Package name
package.name = test_ovik_app

# (string) Package domain (needed for android packaging)
package.domain = org.ovik

# (string) Source code directory
source.dir = .

# (list) Source files to include (including dat files and fonts)
source.include_exts = py,png,jpg,kv,atlas,dat,ttf

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*, assets/questions/*, assets/fonts/*

# (string) Application version
version = 1.0.0

# (list) Application requirements (критически важные библиотеки для вашего проекта)
requirements = python3, flet, pandas, openpyxl, pycryptodome, reportlab

# (string) Supported orientations (поддерживать и портретный, и альбомный режимы)
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# ==========================================
# Настройки Android
# ==========================================

# (list) Permissions (запрашиваем доступ к памяти для сохранения PDF-результатов)
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (int) Android API to use (минимальная и целевая версии Android)
android.api = 33
android.minapi = 21

# (bool) If True, then skip signup for Google Play and generate an unassigned debug APK
android.debug_artifact = apk

# (str) Short name of your architecture (собираем под стандартные процессоры смартфонов)
android.archs = arm64-v8a, armeabi-v7a
