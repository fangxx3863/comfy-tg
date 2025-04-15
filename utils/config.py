import configparser
import os
import time
import logging

# 定义全局变量
last_prompt = ""
img_res = "1152*896"
current_model = "noobai_xl_vp1_0_fast_mix_hires"

def config_setup():
    global last_prompt, img_res, current_model
    config = configparser.ConfigParser()
    # 如果INI文件不存在，则使用默认值创建
    if not os.path.exists('config.ini'):
        config['DEFAULT'] = {
            'last_prompt': last_prompt,
            'img_res': img_res,
            'current_model': current_model
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        # 如果INI文件存在，则读取值到全局变量
        config.read('config.ini')
        last_prompt = config.get('DEFAULT', 'last_prompt', fallback=last_prompt)
        img_res = config.get('DEFAULT', 'img_res', fallback=img_res)
        current_model = config.get('DEFAULT', 'current_model', fallback=current_model)

def config_update():
    global last_prompt, img_res, current_model
    config = configparser.ConfigParser()
    while True:
        time.sleep(10)  # 每10秒检查一次
        # print("Check config.ini.")
        # 读取当前INI文件的内容
        config.read('config.ini')
        current_last_prompt = config.get('DEFAULT', 'last_prompt', fallback=None)
        current_img_res = config.get('DEFAULT', 'img_res', fallback=None)
        current_current_model = config.get('DEFAULT', 'current_model', fallback=None)
        
        
        # 检查全局变量与INI文件内容是否一致
        if (last_prompt != current_last_prompt or
            img_res != current_img_res or
            current_model != current_current_model):
            # 如果不一致，则更新INI文件
            config.set('DEFAULT', 'last_prompt', last_prompt)
            config.set('DEFAULT', 'img_res', img_res)
            config.set('DEFAULT', 'current_model', current_model)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            logging.info("Config updated.")