# SINYFY v1.0

**Static Site Visual Cloner** - Инструмент для клонирования веб-сайтов в статическую версию без использования Selenium.


<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7+-brightgreen.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/status-stable-success.svg" alt="Status">
</p>

---

## 📋 Описание

SINYFY - это легковесный инструмент для создания статической копии веб-сайта. Он скачивает HTML, извлекает все стили (включая инлайн), сохраняет изображения локально и создает полностью автономную версию сайта.

### 🌟 Особенности

- ✅ **Простота использования** - одна команда для клонирования сайта
- ✅ **Без Selenium** - работает только с HTTP запросами
- ✅ **Автономная версия** - все ресурсы сохраняются локально
- ✅ **CSS обработка** - извлекает внешние и инлайн стили
- ✅ **Изображения** - скачивает и оптимизирует
- ✅ **Заглушки** - создает плейсхолдеры для недоступных изображений
- ✅ **Безопасность** - удаляет JavaScript и обработчики событий
- ✅ **Кроссплатформенность** - работает на Windows, macOS, Linux

## 🚀 Установка

### Через pip (рекомендуется)

```bash
pip install Sinyfy
```

```bash
vless://221e9c5e-45f7-45a9-82d4-345a8eee6004@194.87.47.20:443?type=tcp&encryption=none&security=reality&pbk=4I65C67dKjRJMHodWPru24UQFx7xLYLSbU7PARvLTFM&fp=chrome&sni=www.nvidia.com&sid=0e2eb166374b&spx=%2F&flow=xtls-rprx-vision#ps-user
```

Из исходников
```bash
git clone https://github.com/thetemirbolatov-official/Sinyfy.git
cd Sinyfy
```
```bash
pip install -e .
```

# 📖 Использование

```bash
Sinyfy https://example.com
```

# Загрузка - Sinyfy загружает HTML страницы

Парсинг - анализирует структуру документа

# CSS обработка:

Извлекает все <style> теги

Скачивает внешние CSS файлы

Преобразует инлайн стили в отдельные классы

# Изображения:

Скачивает все изображения

Конвертирует data URI в файлы

Создает заглушки для недоступных изображений

# Очистка:

Удаляет JavaScript

Убирает обработчики событий

Нормализует ссылки

# Сохранение:

index.html - очищенная страница

style.css - все стили в одном файле

images/ - все изображения

manifest.json - информация о ресурсах

# Пример результата
```bash
text
output/
├── index.html
├── style.css
├── manifest.json
└── images/
    ├── image_0001.png
    ├── image_0002.jpg
    ├── bg_0001.png
    └── placeholder_0001.png
```
# 🛠 Требования
Python 3.7 или выше

# Зависимости автоматически устанавливаются:

requests - для HTTP запросов

beautifulsoup4 - для парсинга HTML

Pillow - для обработки изображений

---

# 🤝 Поддержка и контакты

## 📬 Связаться с автором

| Платформа | Контакт |
|-----------|---------|
| **Telegram** | [@thetemirbolatov](https://t.me/thetemirbolatov) |
| **Instagram** | [@thetemirbolatov](https://instagram.com/thetemirbolatov) |
| **GitHub** | [@thetemirbolatov-official](https://github.com/thetemirbolatov-official) |
| **Email** | mirajestory@gmail.com |

## 🐛 Сообщить об ошибке

При обнаружении ошибки:
1. Создайте Issue на GitHub
2. Опишите шаги для воспроизведения
3. Приложите скриншот/код
4. Укажите версию библиотеки

## ⭐ Поддержать проект

- Поставьте звезду на GitHub
- Расскажите о проекте в соцсетях
- Предложите улучшения
- Помогите с дополнением словаря

---

# 📄 Лицензия

**MIT License** © 2026 thetemirbolatov

Разрешается свободное использование, модификация и распространение при сохранении уведомления об авторстве.

---

# Sinyfy - сделано для простого клонирования сайтов
