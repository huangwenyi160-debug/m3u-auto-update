import requests
import os

# 固定配置，不要修改
BASE_URL = "https://woshinibaba.tzh911.qzz.io"
M3U_URL = f"{BASE_URL}/playlist.m3u"
OUTPUT_FILE = "live.m3u"

def fetch_m3u(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Referer": BASE_URL
        }
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"❌ 抓取失败: {str(e)}")
        return ""

# 1. 抓取源
content = fetch_m3u(M3U_URL)
if not content:
    print("❌ 未获取到M3U内容，任务终止")
    exit(1)

# 2. 去重+格式校验
lines = content.splitlines()
valid_lines = []
seen = set()

# 强制保留#EXTM3U头
if not lines[0].strip().startswith("#EXTM3U"):
    valid_lines.append("#EXTM3U")

for line in lines:
    stripped = line.strip()
    if stripped.startswith(("#EXTINF", "http", "#EXTM3U")) and stripped not in seen:
        seen.add(stripped)
        valid_lines.append(line)

# 3. 写入文件
final_content = "\n".join(valid_lines)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"✅ 成功生成 {OUTPUT_FILE}，共 {len(valid_lines)-1} 条有效频道")
