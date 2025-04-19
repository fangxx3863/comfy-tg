from telegram import Update
from telegram.ext import ContextTypes
import logging
import utils.config as cfg
import asyncio
from utils.helpers import *

async def set_res(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Set Resolution Processing ########")
    user_id = str(update.effective_user.id)
    await ensure_user_config(user_id)
    user_config = cfg.user_configs[user_id]
    
    result = filter_command(update.message.text.strip())
    
    if not result:
        await update.message.reply_text("请按以下格式设置分辨率：\n图片竖屏[PV] 图片横屏[PH]\n竖屏[NV] 横屏[NH]\n超高[SV] 超宽[SH]\n或直接输入 宽*高")
        return
    
    result_upper = result.upper()
    resolution_map = {
        "PV": "896*1152",
        "PH": "1152*896",
        "NV": "768*1344",
        "NH": "1344*768",
        "SV": "670*1564",
        "SH": "1564*670"
    }
    
    # 处理特殊简写
    if "*" in result:
        if len(result.split("*")) == 2:
            user_config['img_res'] = result
        else:
            await update.message.reply_text("分辨率格式错误！请使用 宽*高 格式")
            return
    else:
        for key, value in resolution_map.items():
            if key in result_upper or any(word in result for word in value.split("_")):
                user_config['img_res'] = value
                break
        else:
            await update.message.reply_text("分辨率不合法！")
            return
    
    await update.message.reply_text(f"用户 {user_id} 设置成功！\n当前分辨率为：{user_config['img_res']}")
    logging.info(f"User {user_id} set resolution to {user_config['img_res']}")
    logging.info("######## Set Resolution Processed ########")