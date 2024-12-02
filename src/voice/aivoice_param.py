# %%
"""
デフォルトで、喜び、怒り、悲しみ、驚きの4つの音声に対応しています。
各感情値を0.0~1.0の範囲で変更することで調整が可能です。
"""
happy = {
    "PresetName": "紲星 あかり",
    "Volume": 1.1,
    "Speed": 1.2,
    "Pitch": 1.3,
    "PitchRange": 1.4,
    "MiddlePause": 155,
    "LongPause": 375,
    "Styles": [
        {"Name": "J", "Value": 0.5},
        {"Name": "A", "Value": 0},
        {"Name": "S", "Value": 0}
    ]
}
sad = {
    "PresetName": "紲星 あかり",
    "Volume": 1.1,
    "Speed": 1.0,
    "Pitch": 1.1,
    "PitchRange": 1.4,
    "MiddlePause": 155,
    "LongPause": 375,
    "Styles": [
        {"Name": "J", "Value": 0},
        {"Name": "A", "Value": 0},
        {"Name": "S", "Value": 0.5}
    ]
}
angry = {
    "PresetName": "紲星 あかり",
    "Volume": 1.1,
    "Speed": 1.3,
    "Pitch": 1.3,
    "PitchRange": 1.4,
    "MiddlePause": 155,
    "LongPause": 375,
    "Styles": [
        {"Name": "J", "Value": 0},
        {"Name": "A", "Value": 0.5},
        {"Name": "S", "Value": 0}
    ]
}
surprise = {
    "PresetName": "紲星 あかり",
    "Volume": 1.2,
    "Speed": 1.4,
    "Pitch": 1.4,
    "PitchRange": 1.4,
    "MiddlePause": 155,
    "LongPause": 375,
    "Styles": [
        {"Name": "J", "Value": 0},
        {"Name": "A", "Value": 0},
        {"Name": "S", "Value": 0}
    ]
}
neutral = {
    "PresetName": "紲星 あかり",
    "Volume": 1.2,
    "Speed": 1.2,
    "Pitch": 1.3,
    "PitchRange": 1.4,
    "MiddlePause": 155,
    "LongPause": 375,
    "Styles": [
        {"Name": "J", "Value": 0},
        {"Name": "A", "Value": 0},
        {"Name": "S", "Value": 0}
    ]
}
def aivoice_param(emotion):
    if emotion == "happy":
        return happy
    elif emotion == "sad":
        return sad
    elif emotion == "angry":
        return angry
    elif emotion == "surprise":
        return surprise
    else:
        return neutral