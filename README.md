
# Бот для заметок и напоминаний

## 📌 Описание

Этот бот создан для удобного ведения заметок и установки напоминаний. Позволяет записывать важные мысли и получать напоминания в нужное время.

## 🚀 Функционал

* Добавление заметок
* Удаление заметок
* Просмотр списка заметок
* Установка напоминаний с возможностью отложить на 5 минут

## 🔧 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/NoNeedToSleep/note-reminder-bot.git
   cd note-reminder-bot
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` и укажите в нём токен бота:
   ```
   TOKEN=your-bot-token
   ```
4. Запустите бота:
   ```bash
   python bot.py
   ```

## 📖 Команды

* `/start` или `/help` — Информация о боте и доступных командах
* `/add [текст]` — Добавить заметку
* `/delete [текст]` — Удалить заметку
* `/list` — Показать все заметки
* `/remind [минуты] [текст]` — Установить напоминание

## 📜 Требования

* Python 3.8+
* aiogram 3.2.0
* apscheduler 3.10.1
* python-dotenv 1.0.0
* sqlite3 (встроенный в Python)

## 🛠 Разработчик

**[noneedtosleep](https://github.com/NoNeedToSleep/)**
