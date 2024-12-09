# ComfyUI Grok Vision Node
## GrokVision图像反推提示词

这是一个用于 ComfyUI 的自定义节点，它使用 x.ai 的 Grok Vision 模型来分析图片并生成 Stable Diffusion 提示词。

## 功能特点

- 支持中英文双语提示词生成
- 自动图片压缩以适应API限制
- 内置缓存机制提高效率
- 支持自动重试和超时设置
- 详细的错误提示

## 系统要求

- Python 3.8+
- ComfyUI 最新版本
- 依赖包版本要求：
  - openai >= 1.0.0
  - pillow >= 10.0.0
  - torch >= 2.0.0

## 安装方法

1. 确保你已经安装了 ComfyUI
2. 克隆或下载此仓库到 ComfyUI 的 `custom_nodes` 目录：
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/mircool/Comfyui_grok-vision.git
```
3. 安装依赖：
```bash
pip install openai>=1.0.0 pillow>=10.0.0
```

## 获取 API 密钥

1. 访问 [x.ai](https://x.ai) 官网
2. 注册/登录您的账户
3. 在控制台中创建新的 API 密钥
4. 复制 API 密钥并妥善保存

注意：请勿泄露您的 API 密钥，建议设置环境变量或使用配置文件存储。

## 使用方法

1. 启动 ComfyUI
2. 在节点列表中找到 "Grok Vision" 节点（位于 image/text 分类下）
3. 将节点添加到你的工作流程中
4. 连接图片输入和设置必要的参数
5. 运行工作流程获取生成的提示词

### 使用示例

以下是一个完整的工作流程示例：

1. 加载图片：
   - 使用 "Load Image" 节点加载您的图片

2. 连接到 Grok Vision：
   - 将图片输出连接到 Grok Vision 节点的图片输入
   - 设置您的 API 密钥
   - 可选：调整超时时间和重试次数

3. 使用生成的提示词：
   - 将英文或中文提示词输出连接到 SDXL 节点
   - 或将提示词保存到文本文件

### 示例输出

输入图片：
[图片示例]

生成的提示词：
```
英文：A serene landscape photograph of a misty mountain range at sunrise, golden light filtering through clouds, pine trees in the foreground, high resolution, dramatic lighting, atmospheric, professional photography

中文：日出时分的山脉风景照片，金色阳光透过云层，前景是松树，高分辨率，戏剧性的光线，有氛围感，专业摄影
```

## 参数说明

### 必需参数
- **图片**：要分析的输入图片
- **API密钥**：你的 x.ai API 密钥

### 可选参数
- **超时时间**：API 请求超时时间（默认：30秒，范围：1-300秒）
- **重试次数**：失败时的重试次数（默认：3次，范围：1-10次）
- **使用缓存**：是否启用结果缓存（选项：enable/disable，默认：enable）

### 输出
- **英文提示词**：生成的英文 Stable Diffusion 提示词
- **中文提示词**：生成的中文 Stable Diffusion 提示词
- **原始响应**：API 的完整 JSON 响应

## 性能和限制

- **API 调用限制**：
  - 每秒最多 1 次请求
  - 每月请求次数取决于您的 API 套餐

- **图片限制**：
  - 最大文件大小：20MB
  - 支持格式：JPEG, PNG
  - 自动压缩：大于限制时自动压缩

- **缓存性能**：
  - 内存缓存：仅在当前会话有效
  - 缓存大小：无限制，但建议定期重启以清理内存

## 错误代码说明

| 错误代码 | 说明 | 解决方案 |
|---------|------|---------|
| 401 | API密钥无效 | 检查API密钥是否正确 |
| 403 | 没有访问权限 | 确认API密钥权限设置 |
| 413 | 请求实体过大 | 压缩图片后重试 |
| 429 | 请求过于频繁 | 等待一段时间后重试 |
| 500 | 服务器错误 | 联系x.ai支持 |

## 注意事项

1. 请确保你有有效的 x.ai API 密钥
2. 图片会自动压缩以符合 API 的大小限制
3. 建议在批量处理时启用缓存以提高效率
4. API 调用有频率限制，请注意使用频率

## 常见问题

1. **API密钥错误**
   - 确保你的 API 密钥正确且有效
   - 检查 API 密钥是否有足够的配额

2. **图片大小问题**
   - 节点会自动压缩大图片
   - 如果仍有问题，建议预先将图片压缩到合适大小

3. **缓存相关**
   - 缓存仅在当前会话有效
   - 重启 ComfyUI 后缓存会清空

4. **性能优化**
   - 使用合适大小的图片
   - 启用缓存避免重复请求
   - 批量处理时注意请求频率

## 更新日志

### v1.0.0
- 初始发布
- 支持中英文提示词生成
- 添加缓存功能
- 添加自动重试机制
- 添加图片压缩功能


## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

- 感谢 x.ai 提供的 Grok Vision API
- 感谢 ComfyUI 社区的支持

## 联系方式

如有问题或建议，请通过以下方式联系：

- [GitHub Issues](https://github.com/mircool/Comfyui_grok-vision/issues)
