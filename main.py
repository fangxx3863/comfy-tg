import logging
import os
import threading
import time
import shutil
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

# 复制默认配置文件
def copy_default_backends():
    backends_dir = 'backends'
    default_dir = 'backends_default'
    
    # 如果backends目录不存在，则创建并复制默认内容
    if not os.path.exists(backends_dir):
        logging.info("Backends Not Found, Copy Default.")
        shutil.copytree(default_dir, backends_dir)
        return
    
    # 检查backends目录是否为空
    if not os.listdir(backends_dir):
        # 遍历默认目录中的所有项目并复制到目标目录
        logging.info("Backends Not Found, Copy Default.")
        for item in os.listdir(default_dir):
            src_path = os.path.join(default_dir, item)
            dst_path = os.path.join(backends_dir, item)
            # 如果是目录则递归复制，否则复制文件
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)

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

# 检测配置文件并复制
copy_default_backends()

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

