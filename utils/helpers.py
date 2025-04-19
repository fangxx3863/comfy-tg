# helpers.py
import os
import re
import random
import logging
from dotenv import load_dotenv
import logging
import asyncio
import utils.config as cfg
from telegram import error as telegram_error

# Load API configuration from environment variables
load_dotenv()
COMFYUI_IP = os.getenv("COMFYUI_IP")
COMFYUI_PORT = os.getenv("COMFYUI_PORT")

async def ensure_user_config(user_id):
    """确保用户配置存在，不存在则初始化"""
    user_id_str = str(user_id)
    if user_id_str not in cfg.user_configs:
        cfg.user_configs[user_id_str] = {
            'last_prompt': '',
            'img_res': cfg.DEFAULT_IMG_RES,
            'current_model': cfg.DEFAULT_CURRENT_MODEL
        }

def filter_command(text):
    """去除字符串中的命令部分（第一个分割后的元素）"""
    parts = text.strip().split()
    if not parts:
        return ""
    parts.pop(0)
    return ' '.join(parts)

def progress_bar(percentage):
    max_length = 10  # Define the length of the progress bar
    filled_length = int(max_length * percentage // 100)  # Calculate filled length
    bar_of_the_progress = '█' * filled_length + '-' * (max_length - filled_length)  # Create the bar
    return f"[{bar_of_the_progress}] {percentage}%"

def escape_reserved_characters(text):
    # 定义需要转义的保留字符
    reserved_chars = ['!', '(', ')', '=', '+', '{', '}', '[', ']', '>', '<', '#', '&', '|']
    
    # 对每个保留字符进行转义
    for char in reserved_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def escape_telegram_reserved_characters(text):
    # 定义需要转义的保留字符
    reserved_chars = ['_', '.', '!', '(', ')', '=', '+', '{', '}', '[', ']', '>', '<', '#', '&', '|']
    
    # 对每个保留字符进行转义
    for char in reserved_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

async def async_retry_on_error(func, wait=0.1, retry=20, *args, **kwargs):
    """
    异步重试装饰器，支持指数退避（示例固定等待时间）
    
    :param func: 需要重试的异步函数
    :param wait: 基础等待时间（秒）
    :param retry: 最大重试次数（0表示无限重试）
    """
    i = 0
    while True:
        try:
            return await func(*args, **kwargs)
        except telegram_error.NetworkError as e:
            logging.exception(f"Network Error. Retry attempt {i+1}/{retry if retry else '∞'}")
            i += 1
            
            if retry and i >= retry:
                raise Exception(f"Max retries {retry} exceeded") from e
                
            await asyncio.sleep(wait)




def replace_wildcards(text):
    """
    替换文本中的通配符/filename/为对应文件中的随机行内容
    参数：
        text: 包含通配符的原始字符串
    返回：
        替换后的字符串
    """
    # 预加载通配符文件
    wildcard_dir = 'wildcards'
    wildcard_dict = {}
    
    if os.path.exists(wildcard_dir):
        for filename in os.listdir(wildcard_dir):
            if filename.endswith('.txt'):
                key = filename[:-4]
                try:
                    with open(os.path.join(wildcard_dir, filename), 
                             'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f if line.strip()]
                        if lines:
                            wildcard_dict[key] = lines
                except Exception as e:
                    logging.error(f"读取文件 {filename} 失败: {str(e)}")
    
    # 定义替换逻辑
    def replacer(match):
        name = match.group(1)
        return random.choice(wildcard_dict[name]) if name in wildcard_dict else match.group(0)
    
    # 执行全局替换
    return re.sub(r'/(\w+)/', replacer, text)
