import asyncio
import uvicorn
from app.main import app          # FastAPI приложение
from kurs_bot.bot_calendr import main as bot_main   # асинхронная main() бота

async def main():
    # Конфигурация uvicorn без автоматической перезагрузки,
    # потому что reload=True несовместим с общим event loop
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, reload=False)
    server = uvicorn.Server(config)

    # Запускаем сервер и бота параллельно
    await asyncio.gather(
        server.serve(),
        bot_main()
    )

if __name__ == "__main__":
    asyncio.run(main())