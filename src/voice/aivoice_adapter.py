# %%
import win32com.client
import time
import json

class AIVoiceAPI:
    def __init__(self):
        self.tts_control = win32com.client.Dispatch("AI.Talk.Editor.Api.TtsControl")
        hosts = self._get_available_hosts()
        self._initialize_api(hosts[0])
        self._connect_to_host()

    def _get_available_hosts(self):
        return self.tts_control.GetAvailableHostNames()

    def _initialize_api(self, host_name):
        self.tts_control.Initialize(host_name)

    def _connect_to_host(self):
        if self.tts_control.Status == "NotRunning":
            self.tts_control.StartHost()
        self.tts_control.Connect()

    def get_text(self):
        return self.tts_control.Text

    def set_text(self, text):
        self.tts_control.Text = text

    def play_and_wait(self):
        self.tts_control.Play()
        while self.tts_control.Status == 3:#3は音声再生中のステ
            time.sleep(1)

    def stop_text(self):
        self.tts_control.Stop()

    def save_audio_to_file(self, path):
        self.tts_control.SaveAudioToFile(path)

    def get_voice_preset(self, preset_name):
        json_preset = self.tts_control.GetVoicePreset(preset_name)
        return json.loads(json_preset)

    def set_voice_preset(self, preset_json):
        json_str = json.dumps(preset_json)
        self.tts_control.SetVoicePreset(json_str)

    def apply_voice_preset(self, preset_name):
        preset_json = self.get_voice_preset(preset_name)
        self.set_voice_preset(preset_json)

    def disconnect(self):
        self.tts_control.Disconnect()
    
    def play_voice(self,text,preset):
        self.set_voice_preset(preset)
        self.set_text(text)
        self.play_and_wait()

"""
# 使用例
api = AIVoiceAPI()
hosts = api._get_available_hosts()
preset_json = {
    "PresetName": "紲星 あかり",
    "Volume": 1.1,
    "Speed": 1.2,
    "Pitch": 1.3,
    "PitchRange": 1.4,
    "MiddlePause": 155,
    "LongPause": 375,
    "Styles": [
        {"Name": "J", "Value": 0.75},
        {"Name": "A", "Value": 0.5}  # 怒りを少し表現
    ]
}
if hosts:
    api.initialize_api(hosts[0])
    api.connect_to_host()
    api.set_text("こんにちは、これはテストです。")
    api.play_and_wait()
    api.set_voice_preset(preset_json)
    api.set_text("こんにちは、これはテストです。")
    api.play_and_wait()
    api.disconnect()
"""
# %%
