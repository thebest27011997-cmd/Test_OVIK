[app]
title = Тест_ОВ
package.name = testovikapp
package.domain = org.ovik
source.dir = .
source.include_exts = py,dat,ttf
source.include_patterns = assets/*, assets/questions/*, assets/fonts/*
version = 1.0.0

# Фиксируем flet 1.0.0 и зависимости
requirements = python3,flet==1.0.0,pandas,openpyxl,pycryptodome,reportlab

orientation = portrait
fullscreen = 0

# Настройки Android
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# ЖЕСТКАЯ ФИКСАЦИЯ СТАБИЛЬНЫХ ВЕРСИЙ (Запрещаем качать альфа-версию 37.0.0)
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.build_tools_version = 34.0.0

android.debug_artifact = apk
android.archs = arm64-v8a
