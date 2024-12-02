# %%
from dotenv import load_dotenv
import google.generativeai as genai
import os

class GeminiAdapter:
    load_dotenv()
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')

    def __init__(self):
        pass

    def gemini_chat(self, user_text):
        try:
            response = self.model.generate_content(user_text)
            return response.text
        except:
            response = None
            return response
    
    def gemini_streaming(self, user_text):
        try:
            response = self.model.generate_content(user_text, stream=True)
            for chunk in response:
                if hasattr(chunk, 'parts'):
                    texts = [part.text for part in chunk.parts if hasattr(part, 'text')]
                    yield ''.join(texts)
        except:
            response = None
            return response
    
if __name__ == "__main__":
    ga = GeminiAdapter()
    for chunk in ga.gemini_streaming("桃太郎の物語を教えて下さい"):
        print(chunk)
# %%
