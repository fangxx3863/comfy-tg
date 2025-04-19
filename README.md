# comfy-tg 🤖🎨

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Docker Image](https://img.shields.io/docker/pulls/fangxx/comfy-tg.svg)](https://hub.docker.com/r/fangxx/comfy-tg)

一个基于Python的Telegram机器人，实现与ComfyUI绘图工具的无缝对接，让你在聊天中轻松调用AI绘图能力！

## ✨ 功能特性
- 通过Telegram消息直接生成AI绘图
- 限制指定群组使用（开发中）
- 自定义工作流模板
- Docker容器化部署
- 多用户处理

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Telegram Bot Token
- 可访问的ComfyUI服务

### 📦 常规安装
```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env  # 编辑配置

# 启动服务
python main.py
```

### 🐳 Docker部署
```bash
# 从DockerHub拉取最新镜像
docker pull fangxx/comfy-tg:latest

# 运行容器（示例）
docker run -d \
  -e BOT_TOKEN="YOUR_BOT_TOKEN" \
  -e COMFYUI_IP="192.168.1.100" \
  -e COMFYUI_PORT=8188 \
  -v /path/to/backends:/app/backends \
  fangxx/comfy-tg
```

## 🔧 环境变量配置
| 变量名          | 必填 | 说明                          |
|-----------------|------|-------------------------------|
| BOT_TOKEN       | ✅   | Telegram机器人Token          |
| COMFYUI_IP      | ✅   | ComfyUI服务IP地址            |
| COMFYUI_PORT    | ✅   | ComfyUI服务端口              |
| ADMIN_ID        | ❌   | 管理员用户ID（开发中）        |
| GROUP_ID        | ❌   | 授权群组ID（开发中）          |

## 🎨 自定义工作流
首次运行后会在项目根目录生成以下结构：
```
backends/
├── illustrious_xl_v1_0_fast_mix_hires.py
├── noobai_xl_ep1_1_fast_mix_hires.py
└── ...
```

1. 复制任意一份配置文件作为模板  
2. 替换`prompt_text`变量为你自定义的工作流  
3. 修改`async def t2i(prompt, res)`中的变量替换    

## 💬 使用示例
```
用户 ➔ /help
机器人 ➔ 发送使用指南和命令列表

用户 ➔ /make 1girl, school uniform
机器人 ➔ [生成图片中...]
机器人 ➔ [返回生成结果]

用户 ➔ /again
机器人 ➔ [使用上次提示词生成...]
机器人 ➔ [返回生成结果]
```

## 📌 注意事项
1. 确保ComfyUI服务已正确配置并开放对应端口  
2. 生产环境建议使用Docker部署  

## 🤝 贡献指南
欢迎提交PR！请确保：
1. 遵循现有代码风格  
2. 更新相关文档  

## 📄 许可证
MIT License © 2025 [fangxx3863]
