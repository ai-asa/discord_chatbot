# %%
import requests
import io
import soundfile
from .play_sound import PlaySound 

class StyleBertVITS2_Adapter:
    URL = "http://127.0.0.1:5000/"
    def __init__(self):
        pass

    def _create_request_query(self,text:str,model_id:int) -> bytes:
        item_data = {
            "text":text,
            "model_id":model_id,
            "encoding":"utf-8",
            "language":"JP"
        }
        response = requests.get(self.URL + 'voice', params=item_data)
        return response.content
    
    def get_voice_data(self, text:str, model_id:int):
        audio_bytes = self._create_request_query(text,model_id)
        audio_stream = io.BytesIO(audio_bytes)
        data, sample_rate = soundfile.read(audio_stream)
        return data,sample_rate
    
if __name__ == "__main__":
    sb = StyleBertVITS2_Adapter()
    text = "こんにちはー"
    model_id = 4
    data, rate = sb.get_voice_data(text,model_id)
    play_sound = PlaySound("スピーカー")
    play_sound.play_sound(data,rate)

# %%
