import os
import asyncio
import logging
import sqlite3
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

#logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

conn = sqlite3.connect("notes.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    remind_time DATETIME NOT NULL
)
""")
conn.commit()

@dp.message(Command("start", "help"))
async def send_welcome(message: Message):
    instructions = (
        "👋 Привет! Я бот для заметок и напоминаний. Вот что я умею:\n\n"
        "📌 /add [текст] — добавить заметку\n"
        "🗑 /delete [текст] — удалить заметку\n"
        "📜 /list — показать все заметки\n"
        "⏰ /remind [минуты] [текст] — установить напоминание\n\n"
        "При напоминании будет кнопка для повторного напоминания через 5 минут."
    )
    await message.answer(instructions)

@dp.message(Command("add"))
async def add_note(message: Message):
    note = message.text[len("/add "):].strip()
    if not note:
        await message.answer("Пожалуйста, укажите текст заметки после команды /add")
        return
    cursor.execute("INSERT INTO notes (text) VALUES (?)", (note,))
    conn.commit()
    await message.answer(f"Заметка добавлена: {note}")

@dp.message(Command("delete"))
async def delete_note(message: Message):
    note = message.text[len("/delete "):].strip()
    cursor.execute("DELETE FROM notes WHERE text = ?", (note,))
    conn.commit()
    await message.answer(f"Заметка удалена: {note}")

@dp.message(Command("remind"))
async def set_reminder(message: Message):
    try:
        parts = message.text.split(" ", 2)
        minutes = int(parts[1])
        text = parts[2]
        remind_time = datetime.now() + timedelta(minutes=minutes)
        cursor.execute("INSERT INTO reminders (text, remind_time) VALUES (?, ?)", (text, remind_time))
        conn.commit()
        scheduler.add_job(send_reminder, "date", run_date=remind_time, args=[message.chat.id, text])
        await message.answer(f"Напоминание установлено через {minutes} минут: {text}")
    except (IndexError, ValueError):
        await message.answer("Используйте формат: /remind 10 Текст напоминания")

async def send_reminder(chat_id, text):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔁 Напомнить через 5 минут", callback_data=f"remind_again|{text}")]
        ]
    )
    await bot.send_message(chat_id, f"🔔 Напоминание: {text}", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("remind_again"))
async def remind_again(callback_query: types.CallbackQuery):
    text = callback_query.data.split("|", 1)[1]
    remind_time = datetime.now() + timedelta(minutes=5)
    scheduler.add_job(send_reminder, "date", run_date=remind_time, args=[callback_query.message.chat.id, text])
    await callback_query.answer("Напоминание повторится через 5 минут!")

@dp.message(Command("list"))
async def list_notes(message: Message):
    cursor.execute("SELECT text FROM notes")
    notes = cursor.fetchall()
    if not notes:
        await message.answer("У вас нет заметок.")
    else:
        notes_text = "\n".join([note[0] for note in notes])
        await message.answer(f"Ваши заметки:\n{notes_text}")

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())