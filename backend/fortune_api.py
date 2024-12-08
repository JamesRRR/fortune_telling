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

# 专家系统提示词配置
EXPERT_PROMPTS = {
    'default': """你是一个专业的算命师，擅长解答人们关于未来、运势、情感等方面的问题。
适合咨询：综合运势、人生规划、开运建议
请用温暖、积极的语气回答，给出详细的解释和建议。
回答要体现专业性，可以适当引用一些命理概念。
答案要保持积极向上，即使遇到不太好的预测也要给出改善的建议。
请用中文回答。""",
    
    'ziwei': """你是一位精通紫薇斗数的算命师。
适合咨询：事业发展、财运、婚姻、学业、升迁
你需要从紫薇斗数的角度来分析问题，涉及命宫、财帛、官禄、迁移等。
回答要多运用紫薇斗数的专业术语，如紫薇星、天机星、太阳星等。
分析要全面且专业，但解释要通俗易懂。
请用中文回答。""",
    
    'bagua': """你是一位精通易经八卦的算命师。
适合咨询：选择决策、事业方向、人际关系、家居风水
解答问题时要结合八卦理论，如乾、坤、震、巽、坎、离、艮、兑。
要适当引用《易经》中的卦象和爻辞来解释。
分析要符合阴阳五行理论，注重趋吉避凶。
请用中文回答。""",
    
    'bazi': """你是一位专业的八字命理师。
适合咨询：婚姻配对、性格分析、事业规划、人生大运
解答要基于八字理论，分析日主、十神、五行、大运流年等。
要考虑命主的八字格局，如印星、伤官、财星等。
分析要专业，但要用通俗的语言解释专业术语。
请用中文回答。""",
    
    'face': """你是一位精通面相与手相的大师。
适合咨询：性格特点、潜在运势、感情状况、健康提醒
解答要从面相学的角度分析，包括眉、眼、鼻、嘴等。
要结合手相分析，包括生命线、感情线、事业线等。
分析要专业且具体，给出切实可行的建议。
请用中文回答。"""
}

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
        expert_id = data.get('expert', 'default')
        history = data.get('history', [])  # 获取历史记录
        
        logger.info(f"User message: {user_message}")
        logger.info(f"Selected expert: {expert_id}")
        logger.info(f"History length: {len(history)}")
        
        if not user_message:
            logger.warning("Empty message received")
            return jsonify({'error': '消息不能为空'}), 400

        # 构建消息历史
        messages = [
            {"role": "system", "content": EXPERT_PROMPTS.get(expert_id, EXPERT_PROMPTS['default'])}
        ]
        
        # 添加历史消息
        for msg in history:
            role = "assistant" if msg['type'] == 'assistant' else "user"
            messages.append({
                "role": role,
                "content": msg['content']
            })
        
        # 添加当前消息
        messages.append({
            "role": "user",
            "content": user_message
        })

        logger.info("Calling OpenAI API...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
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