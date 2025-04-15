from telegram import Update, InputMediaPhoto
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from utils.helpers import *
from utils.search_tag import *

search_tag_instance = SearchTag()

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Search Processing ########")
    result = filter_command(update.message.text.strip())
    await update.effective_message.reply_text(escape_telegram_reserved_characters(search_tag_instance.search_tag(result)), parse_mode="MarkdownV2")
    logging.info("######## Search Processed ########")
    