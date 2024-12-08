from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import traceback

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv("/Users/bingyanren/Documents/llm/fortune telling/.env")
logger.info(f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')[:8]}...")

app = Flask(__name__)
CORS(app)

# 初始化OpenAI客户端
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 系统提示词
SYSTEM_PROMPT = """你是一个专业的算命师，擅长解答人们关于未来、运势、情感等方面的问题。
请用温暖、积极的语气回答，给出详细的解释和建议。
回答要体现专业性，可以适当引用一些命理概念。
答案要保持积极向上，即使遇到不太好的预测也要给出改善的建议。
请用中文回答。"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        logger.info("Received chat request")
        data = request.get_json()
        logger.debug(f"Request data: {data}")
        
        user_message = data.get('message', '')
        logger.info(f"User message: {user_message}")
        
        if not user_message:
            logger.warning("Empty message received")
            return jsonify({'error': '消息不能为空'}), 400

        logger.info("Calling OpenAI API...")
        # 使用新的API调用方式
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8
        )
        logger.debug(f"OpenAI API response: {response}")

        # 获取助手的回复
        assistant_response = response.choices[0].message.content
        logger.info(f"Assistant response: {assistant_response[:100]}...")

        return jsonify({
            'response': assistant_response
        })

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': '服务器内部错误',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=5001, debug=True)