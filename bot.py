import telebot
import requests
import os

# --- SÉCURITÉ : RÉCUPÉRATION DES CLÉS VIA VARIABLES D'ENVIRONNEMENT ---
# Sur ton PC, tu peux remettre tes clés à la place des os.environ.get(...) pour tester
# Mais pour GitHub, laisse os.environ.get !
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')

# Vérification si les clés existent (pour éviter les crashs silencieux)
if not TELEGRAM_TOKEN or not ETHERSCAN_API_KEY:
    print("ERREUR: Les clés API ne sont pas configurées dans les variables d'environnement.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_gas_price():
    url = f"https://api.etherscan.io/v2/api?chainid=1&module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == '1':
            return data['result']
        return None
    except:
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! 👋 Type /gas to check current Ethereum fees.")

@bot.message_handler(commands=['gas', 'fees'])
def send_gas(message):
    bot.send_chat_action(message.chat.id, 'typing')
    data = get_gas_price()
    
    if data:
        slow = round(float(data['SafeGasPrice']), 2)
        avg = round(float(data['ProposeGasPrice']), 2)
        fast = round(float(data['FastGasPrice']), 2)

        msg = (
            f"⛽ **Ethereum Gas**\n"
            f"━━━━━━━━━━━━━\n"
            f"🐢 **Slow:** {slow} gwei\n"
            f"🚗 **Avg:** {avg} gwei\n"
            f"🚀 **Fast:** {fast} gwei"
        )
        bot.reply_to(message, msg, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ Error. Check configuration.")

if __name__ == "__main__":
    print("Bot en ligne...")
    bot.infinity_polling()