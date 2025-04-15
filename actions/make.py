from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ContextTypes
from utils.helpers import *
import asyncio
import utils.config as cfg
import logging
import importlib

def dynamic_import_backend(module_name, target):
    # 动态导入指定模块和目标函数/类
    try:
        # 动态导入模块
        imported_module = importlib.import_module(f'backends.{module_name}')
        # 获取模块中的目标函数或类
        return getattr(imported_module, target)
    except ModuleNotFoundError:
        logging.error(f"Module '{module_name}' not found.")
        return None
    except AttributeError:
        logging.error(f"Attribute '{target}' not found in module '{module_name}'.")
        return None

async def make(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Make Processing ########")
    result = filter_command(update.message.text.strip())

    # 如果提示词为空
    if result.strip() == "":
        ret = await update.message.reply_text("提示词为空！")
        await update.message.delete()
        await ret.delete()
        return
    cfg.last_prompt = result
    logging.info(f"User ID: {update.effective_user.id}")
    
    t2i = dynamic_import_backend(cfg.current_model, "t2i")
    prompt = replace_wildcards(cfg.last_prompt)
    # 生成图片
    identifier, file_path = await asyncio.gather(
        update.message.reply_text("生成中..."),
        t2i(prompt, cfg.img_res)
    )

    # 发送图片
    # await update.message.reply_document(file_path, read_timeout=10, write_timeout=10, caption=f"**>`{escape_telegram_reserved_characters(prompt)}`||\n" ,parse_mode="MarkdownV2")
    await async_retry_on_error(update.message.reply_photo, read_timeout=10, write_timeout=10, photo=file_path, caption=f"**>`{escape_telegram_reserved_characters(prompt)}`||\n" ,parse_mode="MarkdownV2")
    await identifier.delete()
    logging.info("######## Make Processed ########")


async def again(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Again Processing ########")
    result = filter_command(update.message.text.strip())
    if cfg.last_prompt.strip() == "":
        ret = await update.message.reply_text("上次提示词为空！")
        await update.message.delete()
        await ret.delete()
        return
    logging.info(f"User ID: {update.effective_user.id}")
    logging.info("Last Prompt: "+cfg.last_prompt)
    
    t2i = dynamic_import_backend(cfg.current_model, "t2i")
    prompt = replace_wildcards(cfg.last_prompt)
    if result.strip() != "":
        cnt = int(result.strip())
        identifier = await update.message.reply_text(f"使用上次提示词生成中[{cnt}张]...")
        while cnt:
            prompt = replace_wildcards(cfg.last_prompt)
            file_path = await t2i(prompt, cfg.img_res)
            # await update.message.reply_photo(file_path)
            await async_retry_on_error(update.message.reply_photo, read_timeout=10, write_timeout=10, photo=file_path, caption=f"**>`{escape_telegram_reserved_characters(prompt)}`||\n" ,parse_mode="MarkdownV2")
            cnt -= 1
    else:
        # 生成图片
        identifier, file_path = await asyncio.gather(
            update.message.reply_text("生成中..."),
            t2i(replace_wildcards(prompt), cfg.img_res)
        )

        # 发送图片
        # await update.message.reply_photo(file_path)
        await async_retry_on_error(update.message.reply_photo, read_timeout=10, write_timeout=10, photo=file_path, caption=f"**>`{escape_telegram_reserved_characters(prompt)}`||\n" ,parse_mode="MarkdownV2")
    
    await identifier.delete()
    
    logging.info("######## Again Processed ########")
