import requests
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler

# Замените YOUR_TELEGRAM_TOKEN на ваш токен Telegram Bot API
telegram_token = "YOUR_TELEGRAM_TOKEN"

# Замените YOUR_SOLANA_ADDRESS на адрес вашего кошелька в сети Solana
solana_address = "YOUR_SOLANA_ADDRESS"

# Замените YOUR_SOLANA_API_URL на URL API Solana
solana_api_url = "YOUR_SOLANA_API_URL"

def get_solana_balance(address):
    # Создаем URL-запрос к API Solana для получения баланса кошелька
    url = f"{solana_api_url}/accounts/{address}"

    # Отправляем запрос и получаем ответ
    response = requests.get(url)
    data = response.json()

    # Проверяем, что запрос прошел успешно и получаем баланс
    if "data" in data and "value" in data["data"]:
        balance = data["data"]["value"]["lamports"] / 10 ** 9
        return balance
    else:
        return None

def start(update: Update, context):
    bot = context.bot
    chat_id = update.effective_chat.id

    balance = get_solana_balance(solana_address)
    if balance is not None:
        message = f"Баланс кошелька Solana: {balance} SOL"
    else:
        message = "Ошибка при получении баланса кошелька"

    bot.send_message(chat_id=chat_id, text=message)

def main():
    bot = Bot(token=telegram_token)
    updater = Updater(bot=bot, use_context=True)

    # Добавляем обработчик команды /start
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
