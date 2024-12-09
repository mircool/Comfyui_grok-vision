# ComfyUI Grok Vision Node

这是一个ComfyUI的自定义节点,使用Grok Vision API来分析图片并生成Stable Diffusion提示词。

## 功能特点

- 支持上传图片进行分析
- 使用Grok Vision API进行图像理解
- 生成适合Stable Diffusion使用的详细提示词
- 支持API密钥配置
- 支持结果缓存
- 支持API调用重试
- 支持超时设置
- 提供原始API响应
- 提供Web API接口管理密钥

## 安装说明

1. 将此仓库克隆到ComfyUI的`custom_nodes`目录下：
```bash
cd custom_nodes
git clone [repository_url] grok_vision_node
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动ComfyUI
2. 在节点列表中找到"Grok Vision Prompt Generator"
3. 将图片节点连接到输入端
4. 配置节点参数:
   - API密钥: 你的Grok Vision API密钥
   - 超时时间: API调用超时时间(秒)
   - 重试次数: API调用失败时的重试次数
   - 使用缓存: 是否启用结果缓存
5. 运行工作流程获取生成的提示词

## Web API

节点提供了Web API接口来管理API密钥:

- 获取API密钥: `GET /grok-vision/api-key`
- 设置API密钥: `POST /grok-vision/api-key`
  ```json
  {
    "api_key": "your-api-key"
  }
  ```

## 输出说明

节点有两个输出:
1. prompt: 生成的Stable Diffusion提示词
2. raw_response: 原始API响应JSON

## 注意事项

- 使用前请确保你有有效的Grok Vision API密钥
- API密钥请妥善保管,不要分享给他人
- 建议将API密钥保存在环境变量中
- 启用缓存可以避免重复调用API
- API调用有频率限制,每秒最多一次
- 如果遇到API限制,节点会自动等待并重试

## 错误处理

节点会处理以下错误情况:
- API密钥无效
- API调用超时
- API调用频率限制
- 网络连接问题
- API响应错误

## 许可证

MIT License 