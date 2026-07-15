---
name: aliyun-vision
description: 识别和分析图片内容。当用户提供图片（本地路径或URL）并要求描述、识别物体、提取文字、解答图片中的问题或进行视觉问答时使用此技能。依赖阿里云百炼视觉模型（Qwen-VL）。
---

# 阿里云视觉模型识别

调用阿里云百炼视觉理解模型（如 Qwen-VL）分析图片内容。

## 前置条件

需要阿里云百炼 API Key。
- **推荐方式**：设置环境变量 `DASHSCOPE_API_KEY`。获取方式：访问 [阿里云百炼控制台](https://bailian.console.aliyun.com/) 获取。
- **临时方式**：如果用户未配置环境变量，可以请用户在对话中临时提供 API Key，并通过 `--api-key` 参数传入脚本。

## 使用方法

通过 `exec` 工具运行 `scripts/recognize_image.py` 脚本：

```bash
python scripts/recognize_image.py --image <图片路径或URL> [--prompt <提示词>] [--model <模型名称>]
```

**注意**：由于运行环境可能没有将 `python` 加入 PATH，如果 `python` 命令失败，请尝试使用 `py` 命令或 Python 的绝对路径。

### 参数说明

- `--image` (必填)：图片的本地绝对路径或公网 URL。
- `--prompt` (可选)：对图片的提问或指令。默认为 "请详细描述这张图片的内容"。
- `--model` (可选)：使用的模型名称。默认为 `qwen-vl-plus`。其他可选模型：`qwen-vl-max`、`qwen3.7-plus` 等。
- `--api-key` (可选)：阿里云百炼 API Key。如果未设置环境变量 `DASHSCOPE_API_KEY`，则必须提供此参数。

### 示例

**1. 描述本地图片**
```bash
python scripts/recognize_image.py --image "C:\Users\test\Desktop\photo.jpg"
```

**2. 识别图片中的文字**
```bash
python scripts/recognize_image.py --image "https://example.com/receipt.png" --prompt "请提取图片中的所有文字内容"
```

**3. 解答图片中的问题**
```bash
python scripts/recognize_image.py --image "C:\math_problem.png" --prompt "请分步骤解答图中的数学题" --model qwen-vl-max
```

## 工作流

1. 确认用户提供了图片路径或 URL。如果是相对路径，转换为绝对路径。
2. 确认用户的具体需求（如：描述内容、提取文字、解答问题），将其作为 `--prompt` 参数。
3. **检查 API Key**：
   - 优先使用环境变量。如果已知未配置，或首次执行脚本报错提示缺少 API Key，请向用户询问。
   - 用户临时提供后，通过 `--api-key` 参数传入脚本重新执行。
   - **安全提示**：提醒用户 API Key 是敏感信息，建议配置到系统环境变量中以避免每次手动输入。
4. 执行脚本并等待输出。
5. 将脚本的标准输出结果整理后回复给用户。如果脚本报错（如找不到文件），向用户解释错误原因。

## 限制

- 本地图片大小不超过 10MB。
- 支持的图片格式：JPEG, PNG, BMP, WEBP, TIFF, HEIC。
- 如果图片分辨率极高，模型会自动缩放，可能丢失微小细节。
