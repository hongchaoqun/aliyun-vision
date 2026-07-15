#!/usr/bin/env python3
"""
调用阿里云百炼视觉模型识别图片内容。
支持本地图片路径或公网 URL。
"""

import argparse
import base64
import os
import sys
import json
import urllib.request
import urllib.error
import mimetypes

def get_image_url(image_path):
    """如果是本地文件则转换为 Base64 Data URL，否则直接返回 URL"""
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return image_path
    
    if not os.path.exists(image_path):
        print(f"错误: 找不到本地文件 '{image_path}'", file=sys.stderr)
        sys.exit(1)
        
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith("image/"):
        mime_type = "image/jpeg"
        
    with open(image_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")
        
    return f"data:{mime_type};base64,{b64_data}"

def main():
    parser = argparse.ArgumentParser(description="调用阿里云视觉模型识别图片")
    parser.add_argument("--image", required=True, help="图片本地路径或公网 URL")
    parser.add_argument("--prompt", default="请详细描述这张图片的内容", help="提示词 (默认: 请详细描述这张图片的内容)")
    parser.add_argument("--model", default="qwen-vl-plus", help="模型名称 (默认: qwen-vl-plus)")
    parser.add_argument("--api-key", help="阿里云百炼 API Key (如未设置环境变量，可通过此参数临时传入)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误: 未提供 API Key。请设置环境变量 DASHSCOPE_API_KEY 或通过 --api-key 参数传入。", file=sys.stderr)
        sys.exit(1)

    # 默认使用阿里云百炼 OpenAI 兼容接口
    base_url = os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
    
    image_url = get_image_url(args.image)
    
    payload = {
        "model": args.model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": args.prompt}
                ]
            }
        ]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        base_url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            print(content)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API 请求失败 (HTTP {e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
