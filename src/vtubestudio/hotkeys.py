"""
デフォルトで、笑い、悲しい、泣き、ショック、怒り、無表情の6つの表情に対応しています。
使用するモデルごとに、対応するキーバインドアクションのID(hotkey ID)を調べ、書き換えてください。
"""
# "Expressions" = "Hotkey ID"
happy = "a2849a4cf765439e89ca6fefe8da2bcf"
sad = "c251b4196247462a90fcb473c14e174b"
cry = "340a461443174cacb25ae1bb4dfb1cde"
surprise = "8917de5fe5ca490b978019c63d79b600"
angry = "db49baf9659843108a20279ab54c81a8"
neutral = "418776cec0594558bd36914fcb27db27"

def get_hotkeyId(expressions):
    if expressions == "happy":
        return happy
    elif expressions == "sad":
        return sad
    elif expressions == "cry":
        return cry
    elif expressions == "surprise":
        return surprise
    elif expressions == "angry":
        return angry
    else:
        return neutral