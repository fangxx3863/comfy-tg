import logging
import os
import threading
import time
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from actions.bot_commands import setup_handlers
from utils.config import *

# 加载环境变量
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN set in .env file")

# 加载配置文件
config_setup()

# 缓存定时清理
def clean_tmp_folder():
    while True:
        tmp_folder = 'tmp'  # Replace with your tmp folder path
        current_time = time.time()
        for file in os.listdir(tmp_folder):  # Iterate through files
            file_path = os.path.join(tmp_folder, file)
            file_mod_time = os.path.getmtime(file_path)
            if current_time - file_mod_time > 60*30:  # Check if file is older than 30 minutes
                os.remove(file_path)  # Delete the file
        time.sleep(60)  # Sleep for 1 minute


# 配置日志记录器
# 自定义过滤器类
class NoGetUpdatesFilter(logging.Filter):
    def filter(self, record):
        # 如果日志级别是 INFO 并且消息中包含 "getUpdates"，则过滤掉
        if record.levelno == logging.INFO and 'getUpdates "HTTP/1.1 200 OK"' in record.getMessage():
            return False
        return True
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
# 获取根日志记录器
logger = logging.getLogger()
# 将自定义过滤器添加到所有处理器中
for handler in logger.handlers:
    handler.addFilter(NoGetUpdatesFilter())

# 启动清理线程
cleaning_thread = threading.Thread(target=clean_tmp_folder, daemon=True)
cleaning_thread.start()

# 启动配置更新线程
config_thread = threading.Thread(target=config_update, daemon=True)
config_thread.start()

# 启动机器人线程
app = ApplicationBuilder().token(BOT_TOKEN).build()
setup_handlers(app)
app.run_polling(timeout=20, poll_interval=0)

