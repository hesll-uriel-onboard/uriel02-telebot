import argparse
from datetime import date, datetime, timedelta
from operator import call
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from priceapi.api import duys_strategy

def get_cred() -> str:
	parser = argparse.ArgumentParser(prog='hellobot')
	parser.add_argument("--cred")
	cred_file = parser.parse_args(sys.argv[1:]).cred

	try:
		token = open(cred_file).readline()
	except:
		print("failed")
		sys.exit(1)
	return token

async def send_a_message(context: ContextTypes.DEFAULT_TYPE) -> None:
	begin_time = datetime.now()

	try:
		query_time = begin_time - timedelta(seconds=begin_time.second + 1, microseconds=begin_time.microsecond)
		result = duys_strategy(end_time = query_time)
		message = f"""
			Time: {datetime.now().strftime("%H:%M:%S.%f")}
			Frame: {result["time"]}
			Closed price: {result["price"]}
			Coef: {result["coef"]}
		"""
	except:
		message = "Failed to retrieve information from Binance"

	chat_id = context.job.chat_id
	if chat_id is not None:
		end_time = datetime.now() - begin_time
		message += f"Latency: {end_time.seconds}.{end_time.microseconds}"
		await context.bot.sendMessage(chat_id = chat_id, text = message)

async def send_continously(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_text(text = 'Welcome to the Bot')
	assert update.effective_chat is not None
	chat_id = update.effective_chat.id

	context.job_queue.run_once(callback=send_a_message, chat_id=chat_id, when=datetime.now())
	
	now = datetime.now()
	seconds = now.second + now.microsecond / 1000000
	context.job_queue.run_repeating(
		callback = send_a_message,
		interval = 60,
		chat_id = chat_id,
		first =  60 - seconds
	)

def main() -> None:
	cred_token = get_cred()
	application = Application.builder().token(cred_token).build()
	application.add_handler(CommandHandler("start", send_continously))
	application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
	main()
