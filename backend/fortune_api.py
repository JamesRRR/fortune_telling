from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv("/Users/bingyanren/Documents/llm/fortune telling/.env")

app = Flask(__name__)
CORS(app)  # 启用CORS以允许跨域请求

# 从环境变量获取API密钥
openai.api_key = os.getenv('OPENAI_API_KEY')

# 系统提示词
SYSTEM_PROMPT = """你是一个专业的算命师，擅长解答人们关于未来、运势、情感等方面的问题。
请用温暖、积极的语气回答，给出详细的解释和建议。
回答要体现专业性，可以适当引用一些命理概念。
答案要保持积极向上，即使遇到不太好的预测也要给出改善的建议。
请用中文回答。"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400

        # 调用OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8  # 增加一些随机性
        )

        # 获取助手的回复
        assistant_response = response.choices[0].message.content

        return jsonify({
            'response': assistant_response
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)