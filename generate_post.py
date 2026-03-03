import anthropic
import requests
import os
import random
import tweepy

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
X_API_KEY = os.environ["X_API_KEY"]
X_API_SECRET = os.environ["X_API_SECRET"]
X_ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]

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
    "content": f"📢 **今日のXポスト**\n\n```\n{full_post}\n```\n\n✅ Xに自動投稿しました！"
}
response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
print(f"Discord送信: {response.status_code}")

# Xに自動投稿
x_client = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET
)
x_response = x_client.create_tweet(text=full_post)
print(f"X投稿成功: {x_response.data['id']}")
