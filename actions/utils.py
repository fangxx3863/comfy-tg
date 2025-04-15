from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ContextTypes
from utils.helpers import *
import utils.config as cfg

async def set_res(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Set Resolution Processing ########")
    result = filter_command(update.message.text.strip())
    
    if result.strip() == "":
        ret = await update.message.reply_text("请按以下格式设置分辨率：图片竖屏[简写PV] 图片横屏[简写PH] 竖屏[简写NV] 横屏[简写NH] 超高[简写SV] 超宽[简写SH] 宽*高")
        await update.message.delete()
        return
    if ("图片竖屏" in result) or ("PV" in result.upper()):
        cfg.img_res = "896*1152"
    elif ("图片横屏" in result) or ("PH" in result.upper()):
        cfg.img_res = "1152*896"
    elif ("竖屏" in result) or ("NV" in result.upper()):
        cfg.img_res = "768*1344"
    elif ("横屏" in result) or ("NH" in result.upper()):
        cfg.img_res = "1344*768"
    elif ("超高" in result) or ("SV" in result.upper()):
        cfg.img_res = "670*1564"
    elif ("超宽" in result) or ("SH" in result.upper()):
        cfg.img_res = "1564*670"
    elif "*" in result:
        cfg.img_res = result
    else:
        await update.message.reply_text("分辨率不合法！")
        return
    await update.message.reply_text(f"设置成功！当前分辨率为：{cfg.img_res}")
    
    logging.info("######## Set Resolution Processed ########")
