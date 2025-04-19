from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import logging
import os
import utils.config as cfg
import importlib
from utils.helpers import *

async def model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Model Processing ########")
    user_id = str(update.effective_user.id)
    await ensure_user_config(user_id)
    
    # 获取可用模型列表
    try:
        files = os.listdir("backends")
        model_filenames = [
            os.path.splitext(file)[0] 
            for file in files 
            if file.endswith('.py') and not file.startswith('_')
        ]
        
        # 生成带用户ID标识的按钮
        buttons = [
            [InlineKeyboardButton(
                name.split('.')[0],
                callback_data=f"model_choice:{user_id}:{name}"
            )]
            for name in model_filenames
        ]
        
        await update.message.reply_text(
            f"🛠️ 用户 {user_id} 请选择模型:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logging.error(f"获取模型列表失败: {e}")
        await update.message.reply_text("模型列表加载失败，请联系管理员")
    
    logging.info("######## Model Processed ########")

async def model_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # 解析回调数据格式：model_choice:{user_id}:{model_name}
    _, user_id, model_name = query.data.split(":")
    
    # 验证用户身份
    if str(query.from_user.id) != user_id:
        await query.edit_message_text("这不是你的操作！")
        return
    
    await ensure_user_config(user_id)
    cfg.user_configs[user_id]['current_model'] = model_name
    
    try:
        # 添加模型加载验证
        imported_module = importlib.import_module(f'backends.{model_name}')
        if not hasattr(imported_module, 't2i'):
            raise AttributeError(f"模型 {model_name} 缺少必要方法")
            
        await query.edit_message_text(
            f"用户 {user_id} 模型已切换至:\n【{model_name}】"
        )
        logging.info(f"User {user_id} switched to model {model_name}")
    except Exception as e:
        logging.error(f"模型加载失败: {e}")
        await query.edit_message_text(f"模型加载失败: {model_name}\n{str(e)}")