from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.helpers import *
import asyncio
import utils.config as cfg
import logging
import importlib

def dynamic_import_backend(module_name, target):
    try:
        imported_module = importlib.import_module(f'backends.{module_name}')
        return getattr(imported_module, target)
    except (ModuleNotFoundError, AttributeError) as e:
        logging.error(f"Error importing backend: {e}")
        return None

async def make(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Make Processing ########")
    user_id = str(update.effective_user.id)
    await ensure_user_config(user_id)
    user_config = cfg.user_configs[user_id]
    
    result = filter_command(update.message.text.strip())
    if not result:
        ret = await update.message.reply_text("提示词为空！")
        await asyncio.gather(update.message.delete(), ret.delete())
        return
    
    user_config['last_prompt'] = result
    logging.info(f"User ID: {user_id}")
    
    t2i = dynamic_import_backend(user_config['current_model'], "t2i")
    if not t2i:
        await update.message.reply_text("模型加载失败，请联系管理员")
        return
    
    prompt = replace_wildcards(user_config['last_prompt'])
    identifier = await update.message.reply_text("生成中...")
    
    try:
        file_path = await t2i(prompt, user_config['img_res'])
        await async_retry_on_error(
            update.message.reply_photo,
            photo=file_path,
            caption=f"**>`{escape_telegram_reserved_characters(prompt)}`||\n",
            parse_mode="MarkdownV2",
            read_timeout=10,
            write_timeout=10
        )
    except Exception as e:
        logging.error(f"生成失败: {e}")
        await update.message.reply_text("生成失败，请稍后再试")
    finally:
        await identifier.delete()
    
    logging.info("######## Make Processed ########")

async def again(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Again Processing ########")
    user_id = str(update.effective_user.id)
    await ensure_user_config(user_id)
    user_config = cfg.user_configs[user_id]
    
    result = filter_command(update.message.text.strip())
    cnt = int(result) if result.strip().isdigit() else 1
    
    if not user_config['last_prompt'].strip():
        ret = await update.message.reply_text("上次提示词为空！")
        await asyncio.gather(update.message.delete(), ret.delete())
        return
    
    t2i = dynamic_import_backend(user_config['current_model'], "t2i")
    if not t2i:
        await update.message.reply_text("模型加载失败，请联系管理员")
        return
    
    identifier = await update.message.reply_text(f"使用上次提示词生成中[{cnt}张]...")
    
    try:
        for _ in range(cnt):
            prompt = replace_wildcards(user_config['last_prompt'])
            file_path = await t2i(prompt, user_config['img_res'])
            await async_retry_on_error(
                update.message.reply_photo,
                photo=file_path,
                caption=f"**>`{escape_telegram_reserved_characters(prompt)}`||\n",
                parse_mode="MarkdownV2",
                read_timeout=10,
                write_timeout=10
            )
    except Exception as e:
        logging.error(f"再次生成失败: {e}")
        await update.message.reply_text("生成失败，请稍后再试")
    finally:
        await identifier.delete()
    
    logging.info("######## Again Processed ########")