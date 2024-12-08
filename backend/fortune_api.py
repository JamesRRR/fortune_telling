from flask import Flask, request, jsonify
from flask_cors import CORS
import openai  # 改回旧版本的导入方式
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
load_dotenv()

app = Flask(__name__)
CORS(app)

# 设置 OpenAI API 密钥
openai.api_key = os.getenv('OPENAI_API_KEY')  # 使用旧版本的方式设置 API 密钥

# 系统提示词
SYSTEM_PROMPT = """你是一个专业的算命师，擅长解答人们关于未来、运势、情感等方面的问题。
请用温暖、积极的语气回答，给出详细的解释和建议。
回答要体现专业性，可以适当引用一些命理概念。
答案要保持积极向上，即使遇到不太好的预测也要给出改善的建议。
请用中文回答。"""

@app.route('/', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': '算命小助手后端服务正常运行中...'
    })

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
        # 使用旧版本的 API 调用方式
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8
        )
        logger.debug(f"OpenAI API response: {response}")

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
    port = int(os.getenv('PORT', 5001))
    logger.info(f"Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port)