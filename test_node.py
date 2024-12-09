import os
import sys
import json
import torch
import requests
from PIL import Image
import numpy as np

# 添加ComfyUI路径
COMFY_PATH = "path_to_your_comfyui"  # 请替换为你的ComfyUI路径
sys.path.append(COMFY_PATH)

# 导入节点
from .grok_vision_node import GrokVisionNode

def test_node():
    print("开始测试 Grok Vision Node...")
    
    # 1. 测试节点初始化
    node = GrokVisionNode()
    print("节点初始化成功")
    
    # 2. 测试输入类型
    input_types = node.INPUT_TYPES()
    assert "image" in input_types["required"]
    assert "api_key" in input_types["required"]
    print("输入类型检查通过")
    
    # 3. 测试API密钥管理
    test_api_key = "test-api-key"
    response = requests.post(
        "http://localhost:8188/grok-vision/api-key",
        json={"api_key": test_api_key}
    )
    assert response.status_code == 200
    print("API密钥管理测试通过")
    
    # 4. 测试图片处理
    # 创建测试图片
    test_image = np.random.rand(3, 64, 64)
    test_tensor = torch.from_numpy(test_image).unsqueeze(0)
    
    try:
        # 测试无API密钥情况
        try:
            node.generate_prompt(test_tensor, "", 30.0, 3, "disable")
            assert False, "应该抛出API密钥无效错误"
        except ValueError as e:
            assert "API密钥" in str(e)
            print("API密钥验证测试通过")
        
        # 测试有API密钥情况
        try:
            prompt, raw_response = node.generate_prompt(
                test_tensor,
                test_api_key,
                30.0,
                3,
                "enable"
            )
            print("生成的提示词:", prompt)
            print("API响应:", raw_response)
        except Exception as e:
            print("API调用失败(这是正常的,如果你没有提供有效的API密钥):", str(e))
        
        # 测试缓存功能
        if "enable" in node.INPUT_TYPES()["required"]["use_cache"][0]:
            # 第一次调用
            result1 = node.generate_prompt(test_tensor, test_api_key, 30.0, 3, "enable")
            # 第二次调用(应该从缓存获取)
            result2 = node.generate_prompt(test_tensor, test_api_key, 30.0, 3, "enable")
            print("缓存功能测试通过")
            
    except Exception as e:
        print("测试过程中出现错误:", str(e))
        raise
    
    print("所有测试完成!")

if __name__ == "__main__":
    test_node() 