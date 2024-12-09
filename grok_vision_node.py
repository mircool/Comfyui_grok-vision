import os
import json
import torch
import numpy as np
from PIL import Image
import time
from openai import OpenAI
import base64
from io import BytesIO
import re

class GrokVisionNode:
    """
    使用Grok Vision API分析图片并生成Stable Diffusion提示词的节点
    """
    def __init__(self):
        self.api_key = None
        self.processor = None
        self.model = None
        self.last_call_time = 0
        self.cache = {}
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图片": ("IMAGE",),
                "API密钥": ("STRING", {"default": "", "multiline": False}),
            },
            "optional": {
                "超时时间": ("INT", {"default": 30, "min": 1, "max": 300}),
                "重试次数": ("INT", {"default": 3, "min": 1, "max": 10}),
                "使用缓存": (["enable", "disable"], {"default": "enable"}),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("英文提示词", "中文提示词", "原始响应")
    FUNCTION = "generate_prompt"
    CATEGORY = "image/text"

    def generate_prompt(self, 图片, API密钥, 超时时间=30, 重试次数=3, 使用缓存="enable"):
        if not API密钥:
            raise ValueError("请提供有效的x.ai API密钥")
            
        self.api_key = API密钥
        
        # 将ComfyUI的tensor转换为PIL Image
        if isinstance(图片, torch.Tensor):
            image = 图片.cpu().numpy()
            image = Image.fromarray((image[0] * 255).astype(np.uint8))
        
        # 压缩图片
        max_size = (1024, 1024)  # 最大尺寸
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 如果图片是RGBA模式，转换为RGB
        if image.mode == 'RGBA':
            image = image.convert('RGB')
            
        # 生成图片hash用于缓存
        import hashlib
        img_hash = hashlib.md5(image.tobytes()).hexdigest()
        
        # 检查缓存
        if 使用缓存 == "enable" and img_hash in self.cache:
            return self.cache[img_hash]
        
        # 将图片转换为base64
        buffered = BytesIO()
        # 使用较低的JPEG质量来减小文件大小
        image.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # 检查base64大小
        if len(img_str) > 20 * 1024 * 1024:  # 如果大于20MB
            # 继续压缩直到小于20MB
            quality = 85
            while len(img_str) > 20 * 1024 * 1024 and quality > 5:
                quality -= 10
                buffered = BytesIO()
                image.save(buffered, format="JPEG", quality=quality)
                img_str = base64.b64encode(buffered.getvalue()).decode()

        # 创建OpenAI客户端
        client = OpenAI(
            api_key=API密钥,
            base_url="https://api.x.ai/v1",
        )

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_str}",
                            "detail": "high",
                        },
                    },
                    {
                        "type": "text",
                        "text": "Respond with exactly two lines separated by a newline. For each line, provide a comprehensive Stable Diffusion prompt that includes detailed descriptions of:\n- Main subject and pose\n- Clothing and accessories\n- Facial features and expressions\n- Background and environment\n- Art style and quality (e.g. lighting, detail level, resolution)\n- Additional artistic elements\n\n1. English prompt (without any prefix)\n2. Chinese prompt (without any prefix)",
                    },
                ],
            },
        ]

        # 实现重试机制
        for attempt in range(重试次数):
            try:
                # 检查API调用频率
                current_time = time.time()
                if current_time - self.last_call_time < 1.0:  # 限制每秒最多一次调用
                    time.sleep(1.0 - (current_time - self.last_call_time))

                response = client.chat.completions.create(
                    model="grok-vision-beta",
                    messages=messages,
                    temperature=0.01,
                    timeout=超时时间
                )
                
                self.last_call_time = time.time()
                
                content = response.choices[0].message.content
                # 分割英文和中文提示词并清理
                lines = [line for line in content.split('\n') if line.strip()]
                prompt_en = re.sub(r'^.*?:', '', lines[0]).strip() if lines else ""
                prompt_cn = re.sub(r'^.*?:', '', lines[1]).strip() if len(lines) > 1 else ""
                
                raw_response = json.dumps(response.model_dump(), ensure_ascii=False, indent=2)
                
                # 更新缓存
                if 使用缓存 == "enable":
                    self.cache[img_hash] = (prompt_en, prompt_cn, raw_response)
                
                return prompt_en, prompt_cn, raw_response
                    
            except Exception as e:
                if attempt < 重试次数 - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                else:
                    raise Exception(f"API请求失败: {str(e)}")
        
        raise Exception("达到最大重试次数")
