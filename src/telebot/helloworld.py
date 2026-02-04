import argparse
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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


async def send_a_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_text(text = 'Hello World')


def main() -> None:
	cred_token = get_cred()
	application = Application.builder().token(cred_token).build()
	application.add_handler(CommandHandler("start", send_a_message))
	application.run_polling()

if __name__ == "__main__":
	main()
