from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters
from utils.helpers import *
from actions.help import *
from actions.make import *
from actions.describe import *
from actions.model import *
from actions.utils import *
from actions.search import *

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    callback_data = query.data
    
    if "&model&:" in callback_data:
        await model_button(update, context)

def setup_handlers(app):
    app.add_handler(CommandHandler("make", make))
    app.add_handler(CommandHandler("again", again))
    app.add_handler(CommandHandler("set_res", set_res))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.PHOTO, handle_describe))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler('model', model))
    app.add_handler(CommandHandler('search', search))
    app.add_handler(CommandHandler('get_wildcards', get_wildcards))
