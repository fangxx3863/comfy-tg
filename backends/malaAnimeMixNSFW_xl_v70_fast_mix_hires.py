import uuid
import json
import aiohttp
import asyncio
import random
import io
import os
from PIL import Image
from dotenv import load_dotenv


prompt_text = r'''
{
  "3": {
    "inputs": {
      "seed": 367481404374484,
      "steps": 4,
      "cfg": 1,
      "sampler_name": "euler_ancestral",
      "scheduler": "beta",
      "denoise": 1,
      "model": [
        "50",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "malaAnimeMixNSFW_v70WithoutVAE.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Checkpoint加载器（简易）"
    }
  },
  "5": {
    "inputs": {
      "width": 1024,
      "height": 1600,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "空Latent图像"
    }
  },
  "6": {
    "inputs": {
      "text": "",
      "clip": [
        "50",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码"
    }
  },
  "7": {
    "inputs": {
      "text": "score_6, score_5, score_4, source_furry, source_pony, source_cartoon, worst aesthetic, ai-generated, ai-assisted, stable diffusion, nai diffusion, worst quality, worst aesthetic, bad quality, normal quality, average quality, oldest, old, early, very displeasing, displeasing, adversarial noise, unknown artist, banned artist, what, off-topic, artist request, text, artist name, signature, username, logo, watermark, copyright name, copyright symbol, resized, downscaled, source larger, low quality, lowres, jpeg artifacts, compression artifacts, blurry, artistic error, bad anatomy, bad hands, bad feet, disfigured, deformed, extra digits, (extra fingers:1.22), fewer digits, missing fingers, censored, bar censor, mosaic censoring, missing, extra, fewer, bad, hyper, error, ugly, worst, tagme, unfinished, bad proportions, bad perspective, aliasing, asymmetrical, monochrome, sketch, concept art, flat color, flat colors, simple shading, jaggy lines, traditional media \\(artwork\\), microsoft paint \\(artwork\\), ms paint \\(medium\\), unclear, photo, icon, multiple views, sequence, (comic), (text), 2koma, 4koma, multiple images, turnaround, collage, panel skew, letterboxed, framed, border, speech bubble, 3d, lossy-lossless, scan artifacts, out of frame, cropped, (overfit style:12)",
      "clip": [
        "50",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "35",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "14",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  },
  "11": {
    "inputs": {
      "images": [
        "14",
        0
      ]
    },
    "class_type": "SaveImageWebsocket",
    "_meta": {
      "title": "保存图像（网络接口）"
    }
  },
  "13": {
    "inputs": {
      "model_name": "2xNomosUni_compact_multijpg.pth"
    },
    "class_type": "UpscaleModelLoader",
    "_meta": {
      "title": "加载放大模型"
    }
  },
  "14": {
    "inputs": {
      "upscale_model": [
        "13",
        0
      ],
      "image": [
        "8",
        0
      ]
    },
    "class_type": "ImageUpscaleWithModel",
    "_meta": {
      "title": "使用模型放大图像"
    }
  },
  "35": {
    "inputs": {
      "vae_name": "xlVAEC_g9.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "加载VAE"
    }
  },
  "45": {
    "inputs": {
      "lora_name": "dmd2_sdxl_4step_lora_fp16.safetensors",
      "strength_model": 1,
      "model": [
        "48",
        0
      ]
    },
    "class_type": "LoraLoaderModelOnly",
    "_meta": {
      "title": "LoRA加载器（仅模型）"
    }
  },
  "46": {
    "inputs": {
      "lora_name": "anime-detailer-xl.safetensors",
      "strength_model": 0.4,
      "model": [
        "51",
        0
      ]
    },
    "class_type": "LoraLoaderModelOnly",
    "_meta": {
      "title": "LoRA加载器（仅模型）"
    }
  },
  "48": {
    "inputs": {
      "lora_name": "sdxl_lightning_8step_lora.safetensors",
      "strength_model": 0.32,
      "model": [
        "4",
        0
      ]
    },
    "class_type": "LoraLoaderModelOnly",
    "_meta": {
      "title": "LoRA加载器（仅模型）"
    }
  },
  "49": {
    "inputs": {
      "device": "cuda:0",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "OverrideCLIPDevice",
    "_meta": {
      "title": "Force/Set CLIP Device"
    }
  },
  "50": {
    "inputs": {
      "lora_name": "EasyFix.safetensors",
      "strength_model": -1,
      "strength_clip": -1,
      "model": [
        "46",
        0
      ],
      "clip": [
        "49",
        0
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "加载LoRA"
    }
  },
  "51": {
    "inputs": {
      "lora_name": "Fixhands_anime_bdsqlsz_V1.safetensors",
      "strength_model": 0.72,
      "model": [
        "45",
        0
      ]
    },
    "class_type": "LoraLoaderModelOnly",
    "_meta": {
      "title": "LoRA加载器（仅模型）"
    }
  }
}
'''

# Load API configuration from environment variables
load_dotenv()
COMFYUI_IP = os.getenv("COMFYUI_IP")
COMFYUI_PORT = os.getenv("COMFYUI_PORT")

server_address = f"{COMFYUI_IP}:{COMFYUI_PORT}"
client_id = str(uuid.uuid4())

async def queue_prompt(prompt):
    """
    异步发送HTTP POST请求，提交prompt，并返回JSON格式的响应
    """
    p = {"prompt": prompt, "client_id": client_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://{server_address}/prompt", json=p) as resp:
            return await resp.json()

async def get_images(ws, prompt):
    """
    异步从WebSocket中读取数据，直至收到提示执行完成的信息，然后提取图像二进制数据
    """
    # 提交 prompt 并获得对应的 prompt_id
    prompt_response = await queue_prompt(prompt)
    prompt_id = prompt_response['prompt_id']
    
    output_images = {}
    current_node = ""
    
    while True:
        msg = await ws.receive()
        if msg.type == aiohttp.WSMsgType.TEXT:
            message = json.loads(msg.data)
            if message.get('type') == 'executing':
                data = message.get('data', {})
                if data.get('prompt_id') == prompt_id:
                    if data.get('node') is None:
                        break  # 执行结束
                    else:
                        current_node = data.get('node')
        elif msg.type == aiohttp.WSMsgType.BINARY:
            # 只处理当前节点为 '11' 时返回的二进制图像数据
            if current_node == '11':
                images_output = output_images.get(current_node, [])
                # 假设实际图片数据从索引8开始（可能为协议头部字节）
                images_output.append(msg.data[8:])
                output_images[current_node] = images_output
        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
            break

    return output_images

async def t2i(prompt, res):
    """
    异步构造请求，连接WebSocket，接收生成图像数据并保存为本地文件，返回保存的文件路径
    """
    # 加载预定义的JSON模板
    req = json.loads(str(prompt_text), strict=False)
    # 设置文本描述
    req["6"]["inputs"]["text"] = str(prompt).strip().rstrip(",") + ", anime source, score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, (very awa, masterpiece,best quality,ultra_detailed,highres,absurdres:1.2), year 2022, year 2023, year 2024, newest"
    
    # 设置图片宽高（假设res格式为 "宽*高"）
    width, height = str(res).split("*")
    req["5"]["inputs"]["width"] = width
    req["5"]["inputs"]["height"] = height

    # 为采样节点设定随机种子
    seed = random.randint(0, 999999999999999)
    req["3"]["inputs"]["seed"] = seed

    ws_url = f"ws://{server_address}/ws?clientId={client_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url, max_msg_size=32 * 1024 * 1024) as ws:
            images = await get_images(ws, req)

    # 保存获取到的图像
    for node_id, image_list in images.items():
        for image_data in image_list:
            image = Image.open(io.BytesIO(image_data))
            # 保存图片到 tmp 目录下，文件名以种子值命名
            width, height = image.size

            # 计算缩放比例
            if width > 2560 or height > 2560:
                # 计算缩放比例，保持宽高比
                ratio = min(2560 / width, 2560 / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
            else:
                # 如果图像尺寸已经小于等于2560px，则不调整
                new_width, new_height = width, height

            # 使用Lanczos算法调整图像大小
            image = image.resize((new_width, new_height), Image.LANCZOS)
            image.save(f'tmp/{seed}.jpg', quality=95, subsampling=0)

    return f'tmp/{seed}.jpg'

async def main():
    result_path = await t2i("1girl, \nkarutamo, \n\na digital illustration by the artist karutamo, known for their distinctive style. The central figure in the artwork is a young woman with long brown hair tied into twin ponytails and striking blue eyes. She has a slight on her cheeks and appears to be blushing slightly as she looks directly at the viewer. \n\nswimsuit under clothes, collarbone, swimsuit, long sleeves, solo, smile, bare shoulders, off shoulder, school swimsuit, cleavage, one-piece swimsuit, :d, high quality school swimsuit, sitting, looking at viewer, shiny skin, brown hair, thighs, sidelocks, ponytail, breasts, blush, long hair, competition swimsuit, large breasts, covered navel, blue one-piece swimsuit, open mouth, blue eyes, hair between eyes, jacket,\n\nbest quality, very aesthetic, nsfw", "896*1152")
    print("Saved image to:", result_path)

if __name__ == '__main__':
    asyncio.run(main())