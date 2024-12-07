import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 初始化客户端
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 测试调用
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say hello!"}]
)

print(response.choices[0].message.content) 