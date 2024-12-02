#%%
import configparser
from dotenv import load_dotenv
import anthropic
import os
import random

class ClaudeAdapter:

    load_dotenv()
    config = configparser.ConfigParser()
    config.read('config.txt')
    call_attempt_limit  = int(config.get('CONFIG', 'call_attempt_limit ', fallback=5))

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key = os.getenv('CLAUDE_API_KEY')
        )
    
    def claude_chat(self, claude_model, prompt, temperature=1):
        for i in range(self.call_attempt_limit):
            try:
                message = self.client.messages.create(
                    model=claude_model,
                    max_tokens=400, # 出力上限（4096まで）
                    temperature=temperature, # 0.0-1.0
                    system=prompt,
                    messages=[
                        {
                            "role": "user",
                            "content":"_"
                        }
                    ]
                )
                text = message.content[0].text
                return text
            except Exception as error:
                print(f"claude呼び出し時にエラーが発生しました:{error}")
                if i == self.call_attempt_limit - 1:
                    return None  # エラー時はNoneを返す
                continue

    def claude_streaming_chat(self, claude_model, prompt, temperature=1):
        for i in range(self.call_attempt_limit):
            try:
                with self.client.messages.stream(
                    model=claude_model,
                    max_tokens=400, # 出力上限（4096まで）
                    temperature=temperature, # 0.0-1.0
                    system=prompt,
                    messages=[
                        {
                            "role": "user",
                            "content":"_"
                        }
                    ]
                ) as stream:
                    for text in stream.text_stream:
                        yield text
                return # 正常終了時
            except Exception as error:
                print(f"claude呼び出し時にエラーが発生しました:{error}")
                if i == self.call_attempt_limit - 1:
                    return None # エラー終了時

    def openai_chat_random_temperature(self, prompt):
        temperature = round(random.uniform(0.7, 0.9), 2)
        system_prompt = [{"role": "system", "content": prompt}]
        for i in range(self.call_attempt_limit):
            try:
                response = self.client.chat.completions.create(
                    messages=system_prompt,
                    model=self.openai_model,
                    temperature=temperature
                )
                text = response.choices[0].message.content
                return text
            except Exception as error:
                print(f"GPT呼び出し時にエラーが発生しました:{error}")
                if i == self.call_attempt_limit - 1:
                    return None  # エラー時はNoneを返す
                continue
    

if __name__ == "__main__":
    ca = ClaudeAdapter()
    result = ca.claude_chat("何を言われてもこんにちはといってください")
    print(result)

# %%
