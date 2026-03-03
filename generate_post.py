import anthropic
import requests
import os
import random

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# ポストのテーマをランダムに選択
themes = [
    "転職・キャリアの後悔と気づき",
    "お金・投資の後悔と気づき",
    "人間関係の後悔と気づき",
    "結婚・恋愛の後悔と気づき",
    "学び・スキルの後悔と気づき",
    "健康・生活習慣の後悔と気づき",
    "起業・副業の後悔と気づき",
]

theme = random.choice(themes)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": f"""
あなたはXで「人生選択データベース」というアカウントを運営しています。
テーマ「{theme}」で今日の定期ポストを1つ作ってください。

条件：
- 140文字以内
- データ・ランキング・問いかけのいずれかの形式
- ハッシュタグ2つ（#人生選択 #後悔から学ぶ）
- URLは含めない（別途追加するので）
- 共感を呼ぶ内容

ポスト本文だけ出力してください。説明不要。
"""
        }
    ]
)

post_text = message.content[0].text.strip()
full_post = f"{post_text}\n\nhttps://anotokinokoe.github.io/anotokinokoe/?v=3"

# Discordに送信
payload = {
    "content": f"📢 **今日のXポスト**\n\n```\n{full_post}\n```\n\n⬆️ これをコピーしてXに投稿してください！"
}

response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
print(f"Discord送信: {response.status_code}")
