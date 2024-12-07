import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 OpenAI 客户端
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat(message, history):
    try:
        print(f"Received message: {message}")
        print(f"History: {history}")
        
        # 系统提示信息
        system_message = """You are a helpful assistant for chinese fortune telling. 
        Give elaborated answers, explain what you think will happen, no less than 10 sentences. 
        You answer should be mostly optimistic, do not give too much negative guesses. 
        Always try to answer the question. If you don't know the answer, guess one based on popularity. 
        Give your answer in Chinese."""
        
        # 构建消息历史
        messages = [{"role": "system", "content": system_message}]
        
        # 添加历史消息
        if history:
            for human, assistant in history:
                messages.append({"role": "user", "content": human})
                messages.append({"role": "assistant", "content": assistant})
        
        # 添加当前消息
        messages.append({"role": "user", "content": message})
        
        print("Sending to OpenAI:", messages)
        
        # 调用API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content.strip()
        print(f"OpenAI response: {reply}")
        
        return reply
        
    except Exception as e:
        print(f"Error in chat function: {str(e)}")
        raise e

# 创建 Gradio 界面
demo = gr.ChatInterface(
    chat,
    title="算命小助手",
    description="欢迎来到算命小助手！请告诉我您想知道些什么？",
    examples=["我今年的运势如何？", "我的事业发展会怎么样？", "我和现任的感情会如何发展？"],
    theme="soft"
)

# 启动服务
if __name__ == "__main__":
    demo.launch(share=True)  # share=True 会创建一个公共URL

</```rewritten_file>