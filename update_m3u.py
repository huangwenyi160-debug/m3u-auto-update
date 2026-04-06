import requests
import os
import re

# 配置
BASE_URL = "https://woshinibaba.tzh911.qzz.io"
M3U_URL = f"{BASE_URL}/playlist.m3u"
OUTPUT_FILE = "live.m3u"

# 自动翻译频道名称（中文 → 英文）
def translate_channel_name(name):
    translations = {
        "中国": "China",
        "香港": "HongKong",
        "台湾": "Taiwan",
        "澳门": "Macau",
        "马来西亚": "Malaysia",
        "新加坡": "Singapore",
        "印尼": "Indonesia",
        "印度": "India",
        "泰国": "Thailand",
        "英国": "UK",
        "美国": "USA",
        "日本": "Japan",
        "韩国": "Korea",
        "体育": "Sports",
        "电影": "Movies",
        "综艺": "Entertainment",
        "新闻": "News",
        "财经": "Finance",
        "少儿": "Kids",
        "动画": "Cartoon",
        "综合": "General",
        "卫视": "TV",
        "直播": "Live",
        "频道": "Channel",
        "高清": "HD",
        "备用": "Backup",
        "测试": "Test"
    }

    for ch, en in translations.items():
        name = name.replace(ch, en)
    
    return name

# 抓取 M3U
def fetch_m3u(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": BASE_URL
        }
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.text
    except:
        return ""

# 开始处理
content = fetch_m3u(M3U_URL)
if not content:
    exit(1)

lines = content.splitlines()
new_lines = ["#EXTM3U"]
seen = set()

for line in lines:
    stripped = line.strip()
    if not stripped:
        continue

    # 翻译频道名
    if stripped.startswith("#EXTINF"):
        # 提取名称
        match = re.search(r'#EXTINF:-1,(.*)', stripped)
        if match:
            original_name = match.group(1)
            en_name = translate_channel_name(original_name)
            line = line.replace(original_name, en_name)

    # 去重
    if stripped.startswith(("#EXTINF", "http")):
        if stripped not in seen:
            seen.add(stripped)
            new_lines.append(line)

# 保存
final_content = "\n".join(new_lines)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"✅ 翻译完成！已生成英文频道版 live.m3u")
