import asyncio
import csv
import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "8030693481:AAGF2Z99u_h11JdDXeyBtd5zPsmgwwv7ZZM"
CSV_FILE = "app/calendar_data.csv"

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


def read_csv():
    """Читаем CSV и возвращаем список записей"""
    records = []
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "userID": int(row["userID"]),
                "date": row["date"],   # формат YYYY-MM-DD
                "message": row["message"]
            })
    return records


async def check_and_send():
    """Проверяем дату и отправляем сообщение"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    records = read_csv()
    for r in records:
        if r["date"] == today:
            try:
                await bot.send_message(r["userID"], r["message"])
            except Exception as e:
                print(f"Ошибка при отправке {r['userID']}: {e}")


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я бот-напоминалка. Я буду присылать сообщения из CSV в нужный день.")


async def main():
    # Запускаем планировщик: проверка каждый день в 9:00
    scheduler.add_job(check_and_send, "cron", hour=9, minute=0)
    scheduler.start()

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())