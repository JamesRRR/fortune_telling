from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # 启用CORS以允许跨域请求

# 配置OpenAI API密钥
openai.api_key = 'your-api-key-here'  # 替换为您的OpenAI API密钥

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # 调用OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个友好的助手。"},
                {"role": "user", "content": user_message}
            ]
        )

        # 获取助手的回复
        assistant_response = response.choices[0].message.content

        return jsonify({
            'response': assistant_response
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 