import requests
import json
from datetime import datetime, timedelta
import os

# 1.abuse.ch API 요청
abuse_url = "https://mb-api.abuse.ch/api/v1/"
abuse_headers = {
    "Auth-Key": "894cbd520e5ea2f3ed439bf67152f5e37893739bce78724b"
}
abuse_data = {
    "query": "get_taginfo",
    "tag": "kimsuky",
    "limit": "50"
}

response = requests.post(abuse_url, headers=abuse_headers, data=abuse_data)
result = response.json()

# 오늘 날짜 선언
today_kst = datetime.now().strftime("%Y-%m-%d")
# 날짜 임의 지정
today_kst = "2025-05-09"
parsed_lines = []

for entry in result["data"]:
    first_seen_utc_str = entry.get("first_seen", "")
    if not first_seen_utc_str:
        continue
    try:
        first_seen_utc = datetime.strptime(first_seen_utc_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        continue

    # IoC first_seen 일자에 9시간 더함
    first_seen_kst = first_seen_utc + timedelta(hours=9)
    first_seen_kst_date = first_seen_kst.strftime("%Y-%m-%d")

    # 오늘 날짜와 비교
    if first_seen_kst_date == today_kst:
        file_name = entry.get("file_name", "")
        sha256 = entry.get("sha256_hash", "")
        tags = ",".join(entry.get("tags", []))
        link = f"https://bazaar.abuse.ch/sample/{sha256}/"
        line = f'"{file_name}","{sha256}","{tags}","{link}"'
        parsed_lines.append(line)

        # 금일 생성된 데이터 없는 경우 종료
if not parsed_lines:
    exit()

output_path = "Kimsuky_IoC2.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# JSON 저장
with open(output_path, "w", encoding="utf-8") as f:
    for row in parsed_lines:
        f.write(parsed_lines)

print(f"총 저장된 항목: {len(parsed_lines)}")
