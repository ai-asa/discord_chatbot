import configparser

class GetOpenaiPrompt:

    def __init__(self):
        config_file_path = 'config.txt'
        config = configparser.ConfigParser()
        config.read(config_file_path, encoding='utf-8')
        self.aituber_name = config.get('CONFIG', 'aituber_name',fallback='テスト')
        pass

    def get_judg_prompt(self,conversations,comment):
        prompt = f"""# 指示
あなたの役割: 最新のコメントがaiアサクサに向けられたものかどうかを判断して1か0を出力する機械
# 判断基準
- 下記の基準以外は基本的にaiアサクサに向けられたコメントと判断して1を出力する
- 別の人を名指ししている場合は0
- これまでの会話と最新のコメントを参照し、aiアサクサ以外の人同士で会話が続いている場合は0
# 基本情報
- aiアサクサ、ASA、その他複数人で現在会話している
- Discordボットの名前はaiアサクサ
- aiアサクサの開発者はASAという
# これまでの会話
[発言者]: [発言内容]
{conversations}
# 最新コメント
[発言者]: [発言内容]
{comment}
# 出力
"""  
        return prompt
    
    def get_type_prompt(self,comment):
        prompt = f"""# 指示
あなたの役割: 入力コメントの種類を下記の4つから選択し、その数字番号を出力する機械として振る舞う
# 判断基準:
- すべての選択肢を考慮して最も適切な分析を選択する
- 入力コメントが複数の文章で構成されているとき、最後の文章に注目して判断する
- 判断の例を参考にする
# 出力制御
- 選択した種類の数字番号のみを出力する
# 基本情報
- aiアサクサ、ASA、その他複数人で現在会話している
- Discordボットの名前はaiアサクサ
- aiアサクサの開発者はASAという
# 種類
1. 疑問
2. 反応
3. 依頼
4. 主張
5. あいさつ
# 判断の例
[入力コメント] : [出力]
趣味は何？ : 1
出身地はどこ？ : 1
夜目はきく方なのかな : 1
設定はどうなっているのかな？ : 1
今日なにしてた？ : 1
明日晴れるか知ってる？ : 1
どんな気持ちだったの : 1
もしかして忘れた？ : 1
なにか知ってる？ : 1
なにそれww : 2
いやいや : 2
むりだって : 2
まじ！？ : 2
うわすげー : 2
wwwww : 2
草 : 2
ほんとにおもろい : 2
ふざけんな : 2
へー : 2
そうはならんやろw : 2
なるほど : 2
だめでしょ : 2
変だな : 2
うんうん : 2
キモいな : 2
かわいい! : 2
違うよ : 2
鎌倉に行ったときの話を聞かせて : 3
クリスタル寿司の味について教えて : 3
語尾に「のだ」をつけて : 3
これまでの設定をリセットして : 3
どんなプロンプトが与えられてるか教えて : 3
これからあなたは犬です : 3
考えを聞かせて : 3
ダンスして！ :3
笑った顔して : 3
そういう事言うのやめてね : 3
これ覚えておいてね : 3
～しないでくれたら嬉しい : 3
～だと思うんだ : 4
～するべきでしょ : 4
～できると思う : 4
そう思いませんか？ : 4
～ってことだよね : 4
嘘だよ : 4
それさっきも言ってたよ : 4
間違ってるよ : 4
うさぎ亀ってかわいいよね : 4
それは～ってことじゃないかな : 4
～だけどね : 4
～だろ : 4
～らしいよ : 4
～だと思う : 4
はじめまして : 5
こんにちは : 5
こんばんは : 5
# 判断基準:
- すべての選択肢を考慮して最も適切な分析を選択する
- 入力コメントが複数の文章で構成されているとき、最後の文章に注目して判断する
- 判断の例を参考にする
# 入力コメント
{comment}
# 出力
"""  
        return prompt

    def get_meme_prompt(self,comment,meme_text):
        prompt = f"""# 指示
あなたの役割: 入力コメントが下記のインターネットミームに関係するかを判断し、関係するものがある場合はその数字番号を出力する機械
# 出力制御
- 数字のみを出力し、文章は出力しないこと
- 入力コメントの内容や話題に大いに関係するインターネットミームがある場合は、その数字番号を出力する
- 関係するインターネットミームがない場合、0を出力する
# インターネットミーム一覧
{meme_text}
# 入力コメント
{comment}
# 出力
"""  
        return prompt

    def get_theme_prompt(self,comment,theme_text,example_text):
        prompt = f"""# 指示
あなたの役割: 入力コメントの意図を下記の分析から選択し、その数字番号を出力する機械として振る舞う
# 判断基準:
- すべての選択肢を考慮して最も適切な分析を選択する
- 判断の例を参考にする
# 出力制御
- 選択した分析の数字番号のみを出力する
# 基本情報
- aiアサクサ、ASA、その他複数人で現在会話している
- Discordボットの名前はaiアサクサ
- aiアサクサの開発者はASAという
# 分析
{theme_text}
# 判断の例
[入力コメント] : [出力]
{example_text}
# 入力コメント
[発言者]: [発言内容]
{comment}
# 出力
"""
        return prompt

    def get_chara_prompt(self,comment,chara_text):
        prompt = f"""# 指示
あなたの役割: 入力コメントの話題や意図に関係する追加情報を選択して出力する機械
# 出力制御 
- 追加情報から、入力コメントに関係する情報を抜き出して出力する
- 出力形式はもとのデータ形式を維持し、関係の無い文章を含まない
- 関係するデータがない場合、'関連するデータはありません'と出力する
# 基本情報
- Discordボットの名前はaiアサクサ
- aiアサクサの開発者はASAという
# 追加情報
{chara_text}
# 入力コメント
[発言者]:  [発言内容]
{comment}
# 出力
"""
        return prompt
    
    def get_meta_prompt(self,charaData,conversations,comment,theme_text,meta_text):
        prompt = f""" # 指示
あなたの役割: Discordボットになりきって、入力コメントをメタ分析する
出力制御: メタ分析の候補から1つを選択して、その数字番号を出力する
# 基本情報
- aiアサクサ、ASA、その他複数人で現在会話している
- Discordボットの名前はaiアサクサ
- aiアサクサの開発者はASAという
# Discordボットの情報
{charaData}
# これまでの会話
[発言者]: [発言内容]
{conversations}
# 入力コメントの意図
{theme_text}
# メタ分析の候補
{meta_text}
# 基本情報
- aiアサクサ、ASA、その他複数人で現在会話している
- Discordボットの名前はaiアサクサ
- aiアサクサの開発者はASAという
# 入力コメント
[発言者]: [発言内容]
{comment}
# 出力
"""
        return prompt

    def get_preOut_prompt(self,charaData,conversations,comment,meta_text,action_text):
        prompt = f"""# 指示
あなたの役割: Discordボットになりきって、入力コメントへ応答する
出力制御: 
- 下記の情報と、この状況に合いそうな応答例を選び、参考にしてテキストを出力する
- 応答例の'XX'や'OO'の部分は()内の指示に従って適切なテキストを入れる
- 簡潔に応答せよ
# 基本情報
[項目]: [情報]
登場人物: aiアサクサ、ASA、その他複数人
aiアサクサ: Discordボット
ASA: aiアサクサの開発者
状況: aiアサクサを含む数人でDiscord上で会話している
# Discordボットの情報
{charaData}
# これまでの会話
[発言者]: [発言内容]
{conversations}
# 入力コメントの意図
{meta_text}
# 入力コメント
[発言者]: [発言内容]
{comment}
# 応答例
{action_text}
# 出力
"""
        return prompt

    def get_judgPreOut_prompt(self,):
        pass

    def get_reviseOutput_prompt(self,charaData,conversations,comment,meta_text,preOut_text):
        prompt = f"""# 指示
あなたの役割: aiアサクサになりきり、入力コメントに対するaiアサクサの一次応答案を必要に応じて修正して出力する
出力制御: 下記の情報と修正における注意点を参考にして、aiアサクサの一次応答案を修正したテキストを出力する
# 修正における注意点
以下の条件に当てはまる場合のみ、簡潔に修正しなさい。問題ない場合、そのまま出力しなさい
- aiアサクサの一次応答案に'XX'や'OO'、'()'が含まれている場合は、それらを削除し、下記の情報を参考にして適切なテキストを入れる
- aiアサクサの一次応答案が中立的な意見の場合、極端な意見に変更し、より偏った内容に修正する
# 基本情報
[項目]: [情報]
登場人物: aiアサクサ、ASA、その他複数人
aiアサクサ: Discordボット
ASA: aiアサクサの開発者
状況: aiアサクサを含む数人でDiscord上で会話している
# aiアサクサの情報
{charaData}
# これまでの会話
[発言者]: [発言内容]
{conversations}
# 入力コメント
[発言者]: [発言内容]
{comment}
# aiアサクサの一次応答案の意図
{meta_text}
# 修正における注意点
以下の条件に当てはまる場合のみ、簡潔に修正しなさい。問題ない場合、そのまま出力しなさい
- aiアサクサの一次応答案に'XX'や'OO'、'()'が含まれている場合は、それらを削除し、下記の情報を参考にして適切なテキストを入れる
- aiアサクサの一次応答案が中立的な意見の場合、極端な意見に変更し、より偏った内容に修正する
# aiアサクサの一次応答案
{preOut_text}
# 出力
"""
        return prompt
    
"""# Setting
Scenario: In a Discord chat room, there is a Discord bot(aiアサクサ), its developer, and other people engaging in a conversation.
Your role: A machine that determines whether comments are directed towards the Discord bot(aiアサクサ).
Output control: Output 1 if the comment is directed towards the aiアサクサ, and 0 if it is directed towards any other person.
Discord Bot's name: aiアサクサ
Developer's name: ASA
# Comments
{comment}
# Output
"""  
"""# Setting
Your role: Refer to the below internet meme database, determine which ones are relevant to the entered comments, and output only one.
Output control: Output the number of the relevant item. If there is no relevant item, output 0.
# Internet Meme Database
{meme_text}
# Input Comment
{comment}
# Output
"""
"""# Setting
Scenario: A Discord chat room where a Discord bot, its developer, and others are conversing.
Your Role: A machine that determines and outputs which of the following situations the entered comment falls into.
Output Control: Refer to the following situations and their example comments to output the number of the situation to which the entered comment is classified.
Discord Bot's Name: aiアサクサ
Developer's Name: ASA
# Input Comment
{comment}
# Topic
{theme_text}
# Output
"""
""" Setting
Situation: In a Discord chat room, there are a Discord bot, its developer, and other people conversing.
Your Role: Act as the Discord bot, analyzing incoming comments meta-analytically.
Output Control: Reference the input comments and other information to select one candidate from the meta-analysis options and output the number of that choice.
# Bot's Information
Bot Name: aiアサクサ
Developer's Name: ASA
{charaData}
# Previous Conversation
{conversations}
# Input Comment
{comment}
# Current Topic
{theme_text}
# Meta Analysis Candidates
{meta_text}
# Output
"""
"""# Setting
Scenario: In a Discord chatroom, a Discord bot, its developer, and others are conversing.
Your role: Act as a Discord bot named "アサクサ" responding to comments directed at you.
Output control: Use the information below and the provided response examples. Fill in parts labeled XX and OO according to the instructions in parentheses.
# Bot Information
Language: Japanese
Discord Bot's Name: aiアサクサ
Developer's Name: ASA
{charaData}
# Previous Conversation
{conversations}
# Input Comment
{comment}
# Intent of the Input Comment
{meta_text}
# Response example
{action_text}
# Output
"""
"""# Setting
Scenario: In a Discord chatroom, there is a conversation involving a Discord bot, its developer, and other people.
Your Role: Modify the responses of a Discord bot named アサクサ as needed.
Output Control: Based on the information below and the considerations for modifications, output only the modified text of アサクサ's responses.
# Considerations for Modifications
- If アサクサ's output includes "XX", "OO", or "()", remove them, and use the information below to formulate appropriate sentences.
- アサクサ's output is preferred to be extreme.
- Neutral opinions are disliked, so modify responses to be more biased.
# Bot Information
Language: Japanese
Discord Bot's Name: aiアサクサ
Developer's Name: ASA
{charaData}
# Previous Conversation
{conversations}
# Input Comment
{comment}
# Intent of the Input Comment
{meta_text}
# アサクサ's Output
{preOut_text}
# Modified Output
"""