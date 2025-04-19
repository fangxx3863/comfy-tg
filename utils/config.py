import configparser
import os
import time
import logging

# 用户配置字典，键为用户ID字符串，值为配置字典
user_configs = {}
DEFAULT_IMG_RES = "896*1152"
DEFAULT_CURRENT_MODEL = "malaIllustriousxl_xl_v20_fast_mix_hires"

def config_setup():
    global user_configs
    user_configs = {}
    config = configparser.ConfigParser()
    
    if not os.path.exists('config.ini'):
        # 创建默认配置文件
        config['DEFAULT'] = {
            'img_res': DEFAULT_IMG_RES,
            'current_model': DEFAULT_CURRENT_MODEL
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config.read('config.ini')
        # 加载所有用户配置
        for section in config.sections():
            user_id = section
            user_configs[user_id] = {
                'last_prompt': config.get(section, 'last_prompt', fallback=''),
                'img_res': config.get(section, 'img_res', fallback=DEFAULT_IMG_RES),
                'current_model': config.get(section, 'current_model', fallback=DEFAULT_CURRENT_MODEL)
            }

def config_update():
    global user_configs
    while True:
        time.sleep(10)
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # 更新或添加用户配置
        for user_id, config_data in user_configs.items():
            user_id_str = str(user_id)
            if not config.has_section(user_id_str):
                config.add_section(user_id_str)
            
            # 更新配置项
            config.set(user_id_str, 'last_prompt', config_data['last_prompt'])
            config.set(user_id_str, 'img_res', config_data['img_res'])
            config.set(user_id_str, 'current_model', config_data['current_model'])
        
        # 写入配置文件
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        # logging.info("Config updated.")