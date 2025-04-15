from telegram import Update, InputMediaPhoto
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from utils.helpers import *
from PIL import Image
import json
import os
import io
import uuid
import requests
import aiohttp
from googletrans import Translator
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
COMFYUI_IP = os.getenv("COMFYUI_IP")
COMFYUI_PORT = os.getenv("COMFYUI_PORT")

server_address = f"{COMFYUI_IP}:{COMFYUI_PORT}"
client_id = str(uuid.uuid4())

prompt_text = '''
{
  "1": {
    "inputs": {
      "model": "wd-eva02-large-tagger-v3",
      "threshold": 0.4,
      "character_threshold": 0.75,
      "replace_underscore": false,
      "trailing_comma": false,
      "exclude_tags": "censored",
      "tags": "",
      "image": [
        "2",
        0
      ]
    },
    "class_type": "WD14Tagger|pysssss",
    "_meta": {
      "title": "WD14 Tagger"
    }
  },
  "2": {
    "inputs": {
      "image": "",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "加载图像"
    }
  }
}
'''


async def queue_prompt(prompt):
    """
    异步发送HTTP POST请求，提交prompt，并返回JSON格式的响应
    """
    p = {"prompt": prompt, "client_id": client_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://{server_address}/prompt", json=p) as resp:
            return await resp.json()

async def get_tags(ws, prompt):
    prompt_response = await queue_prompt(prompt)
    # prompt_id = prompt_response['prompt_id']
    while True:
        msg = await ws.receive()
        if msg.type == aiohttp.WSMsgType.TEXT:
            message = json.loads(msg.data)
            if message.get('type') == 'executed':
                return message['data']['output']['tags'][0]


async def img_tags(img_name):
    """
    异步构造请求，连接WebSocket，接收生成图像数据并保存为本地文件，返回保存的文件路径
    """
    # 加载预定义的JSON模板
    req = json.loads(prompt_text, strict=False)
    # 设置图像输入
    req["2"]["inputs"]["image"] = str(img_name)

    ws_url = f"ws://{server_address}/ws?clientId={client_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as ws:
            result = await get_tags(ws, req)

    return result


def translate_and_format(input_str):
    # 使用逗号分割字符串成列表
    source_list = input_str.replace('_', ' ').split(',')
    # 创建翻译器实例
    translator = Translator()
    # 使用换行符拼接成一个大字符串
    text_to_translate = '\n'.join(source.strip() for source in source_list)
    # 一次性翻译整个大字符串
    translation = translator.translate(text_to_translate, dest="zh-cn")
    # 将翻译结果按换行符分割回列表
    translated_list = translation.text.split('\n')
    # print(translated_list)
    # 初始化结果字符串
    result = "中英对照表\n**"
    # 遍历原始列表和翻译后的列表，格式化输出
    for source, dest in zip(source_list, translated_list):
        result += f">`{escape_reserved_characters(source.strip())}`    {escape_reserved_characters(dest)}\n"
    # 添加折叠引用标记
    result = result.rstrip('\n') + "||\n"
    # print(result)
    return result

def escape_parentheses(s):
    # 将 ( 替换为 \(
    s = s.replace('(', '\\(')
    # 将 ) 替换为 \)
    s = s.replace(')', '\\)')
    return s

def upload_image(image_path: str, target_url: str = f"http://{server_address}/api/upload/image"):
    """
    将图片文件上传到指定的URL，并设置 Content-Disposition 和 Content-Type。

    :param image_path: 本地图片文件的路径。
    :param target_url: 目标上传的URL。
    """
    # 检查文件是否存在
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"文件路径不存在：{image_path}")
    
    # 获取文件名
    filename = os.path.basename(image_path)
    
    # 打开文件并设置 Content-Type
    with open(image_path, 'rb') as file:
        # 构造 Multipart 文件对象
        files = {
            'image': (filename, file, 'image/jpg')  # 根据文件类型设置 Content-Type
        }
        response = requests.post(target_url, files=files)
    
    return response
    


async def handle_describe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("######## Describe Processing ########")
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        # generate guid for filename
               
        tmp_file_path = "tmp/" + photo.file_id + ".jpg"
        await file.download_to_drive(custom_path=tmp_file_path)
        file_name = photo.file_id + ".jpg"
        image = Image.open(tmp_file_path)
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')  # 根据图片格式选择合适的格式，如'JPEG', 'PNG'等
        
        upload_image(tmp_file_path)

        try:
            answer = await img_tags(file_name)
            logging.info(f"Tags: {answer}")
            await update.message.reply_text(translate_and_format(answer)+f"完整标签\n**>`{escape_parentheses(answer.replace('_', ' '))}`||\n", parse_mode="MarkdownV2")
        except Exception as e:
            logging.error("Unhandled describe_image exception: %s", e)
    
    logging.info("######## Describe Processed ########")