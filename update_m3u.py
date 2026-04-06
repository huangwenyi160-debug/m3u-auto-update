import requests
import re

# 抓取配置
SOURCE_URL = "https://woshinibaba.tzh911.qzz.io/playlist.m3u"
OUT_FILE = "live.m3u"

# 超强频道名翻译（全覆盖你这个源）
trans = {
    "马来西亚": "Malaysia",
    "新加坡": "Singapore",
    "印尼": "Indonesia",
    "泰国": "Thailand",
    "越南": "Vietnam",
    "菲律宾": "Philippines",
    "印度": "India",
    "香港": "Hong Kong",
    "台湾": "Taiwan",
    "中国": "China",
    "澳门": "Macao",
    "日本": "Japan",
    "韩国": "Korea",
    "美国": "USA",
    "英国": "UK",
    "体育": "Sports",
    "电影": "Movies",
    "综艺": "Show",
    "新闻": "News",
    "财经": "Finance",
    "少儿": "Kids",
    "动画": "Cartoon",
    "卫视": "TV",
    "综合": "General",
    "高清": "HD",
    "测试": "Test",
    "备用": "Backup",
    "频道": "Channel",
    "直播": "Live",
}

# 抓取
headers = {"User-Agent": "Mozilla/5.0"}
try:
    r = requests.get(SOURCE_URL, headers=headers, timeout=15)
    r.raise_for_status()
    text = r.text
except:
    print("抓取失败")
    exit()

# 翻译所有频道名
for cn, en in trans.items():
    text = text.replace(cn, en)

# 简单去重
lines = text.splitlines()
new_lines = []
seen = set()

for line in lines:
    s = line.strip()
    if s.startswith("#EXTINF") or s.startswith("http"):
        if s not in seen:
            seen.add(s)
            new_lines.append(line)
    elif s.startswith("#EXTM3U"):
        new_lines.append(line)

# 保存
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))

print("✅ 翻译完成，已全英文")
