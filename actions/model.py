from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ContextTypes
from utils.helpers import *
import utils.config as cfg


async def model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Model Processing ########")
    
    # 获取目录下的所有文件
    files = os.listdir("backends")
    # 提取model_filenames
    model_filenames = [os.path.splitext(file)[0] for file in files if file.endswith('.py')]

    # 生成所需的格式
    formatted_content = [
        [InlineKeyboardButton(filename.split('.')[0], callback_data="&model&:"+filename)]
        for filename in model_filenames
    ]
    reply_markup = InlineKeyboardMarkup(formatted_content)
    await update.message.reply_text('请选择模型:', reply_markup=reply_markup)
    
    logging.info("######## Model Processed ########")

async def model_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    model_name = query.data.replace("&model&:", "")
    cfg.current_model = model_name
    await query.edit_message_text(text=f"当前模型: \n{model_name}")