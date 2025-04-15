from telegram import Update, InputMediaPhoto
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from utils.helpers import *
from pathlib import Path

def get_wildcards_str(folder_path):
    path = Path(folder_path)
    txt = "**"
    txt += '\n'.join(
        f'>`{file.name}`'  # 添加反引号包裹
        for file in sorted(  # 保持排序功能
            path.rglob("*.txt"), 
            key=lambda x: x.name.lower()  # 不区分大小写排序
        )
        if file.is_file()
    ).replace(".txt", "")
    txt += "||"
    return txt

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Help Processing ########")
    help_message = """
/make [提示词] 文生图(可使用/通配符/)
/again [张数] 使用上次提示词重新生成
/set_res [图片竖屏[简写PV] 图片横屏[简写PH] 竖屏[简写NV] 横屏[简写NH] 超高[简写SV] 超宽[简写SH] 宽*高]
/model 修改基础模型
/search [Tag] 查询Tag
/get_wildcards 查询支持的通配符

直接发送图片可反推提示词
    """
    await update.message.reply_text(help_message)
    logging.info("######## Help Processed ########")

async def get_wildcards(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Get Wildcards Processing ########")
    await update.message.reply_text(f"通配符列表：\n{get_wildcards_str('wildcards')}", parse_mode="MarkdownV2")
    logging.info("######## Get Wildcards Processed ########")

