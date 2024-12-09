from .grok_vision_node import GrokVisionNode
import os
import json

# API密钥存储路径
API_KEY_FILE = os.path.join(os.path.dirname(__file__), "api_key.json")

# 加载API密钥
def load_api_key():
    try:
        if os.path.exists(API_KEY_FILE):
            with open(API_KEY_FILE, "r") as f:
                data = json.load(f)
                return data.get("api_key", "")
    except Exception:
        pass
    return ""

# 保存API密钥
def save_api_key(api_key):
    try:
        with open(API_KEY_FILE, "w") as f:
            json.dump({"api_key": api_key}, f)
        return True
    except Exception:
        return False

NODE_CLASS_MAPPINGS = {
    "GrokVisionNode": GrokVisionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GrokVisionNode": "GrokVision图像反推提示词"
} 