from src.ltm.index_controller import IndexController
from src.prompt.get_openai_prompt import GetOpenaiPrompt
from src.chat.openai_adapter import OpenaiAdapter
from src.chat.claude_adapter import ClaudeAdapter
from dotenv import load_dotenv
import pandas as pd
import configparser
import logging
import re

load_dotenv()

class DiscordChatBot:
    config_file_path = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file_path, encoding='utf-8')
    historys_limit = int(config.get('INDEX', 'historys_limit',fallback=4))
    aituber_name = config.get('CONFIG', 'aituber_name',fallback='test_name')
    theme_q_csv_path = config.get('INDEX', 'theme_q_csv_path', fallback='./data/qtheme.csv')
    theme_r_csv_path = config.get('INDEX', 'theme_r_csv_path', fallback='./data/rtheme.csv')
    theme_c_csv_path = config.get('INDEX', 'theme_c_csv_path', fallback='./data/ctheme.csv')
    theme_o_csv_path = config.get('INDEX', 'theme_o_csv_path', fallback='./data/otheme.csv')
    meta_csv_path = config.get('INDEX', 'meta_csv_path', fallback='./data/meta.csv')
    action_csv_path = config.get('INDEX', 'action_csv_path', fallback='./data/action.csv')
    ic = IndexController()
    op = GetOpenaiPrompt()
    oa = OpenaiAdapter()
    ca = ClaudeAdapter()
    conversations = "まだ会話履歴はありません"
    conversations_list = []
    # indexの読み込み
    theme_q_df = pd.read_csv(theme_q_csv_path, encoding='utf-8-sig')
    theme_r_df = pd.read_csv(theme_r_csv_path, encoding='utf-8-sig')
    theme_c_df = pd.read_csv(theme_c_csv_path, encoding='utf-8-sig')
    theme_o_df = pd.read_csv(theme_o_csv_path, encoding='utf-8-sig')
    meta_df = pd.read_csv(meta_csv_path, encoding='utf-8-sig')
    action_df = pd.read_csv(action_csv_path, encoding='utf-8-sig')
    theme_text_q = '\n'.join(theme_q_df.apply(lambda x: f"{x['num']}. {x['theme']}", axis=1))
    theme_text_r = '\n'.join(theme_r_df.apply(lambda x: f"{x['num']}. {x['theme']}", axis=1))
    theme_text_c = '\n'.join(theme_c_df.apply(lambda x: f"{x['num']}. {x['theme']}", axis=1))
    theme_text_o = '\n'.join(theme_o_df.apply(lambda x: f"{x['num']}. {x['theme']}", axis=1))
    example_text_q = '\n'.join(theme_q_df.apply(lambda x: f"{x['example1']} : {x['num']}\n{x['example2']} : {x['num']}\n{x['example3']} : {x['num']}", axis=1))
    example_text_r = '\n'.join(theme_r_df.apply(lambda x: f"{x['example1']} : {x['num']}\n{x['example2']} : {x['num']}\n{x['example3']} : {x['num']}", axis=1))
    example_text_c = '\n'.join(theme_c_df.apply(lambda x: f"{x['example1']} : {x['num']}\n{x['example2']} : {x['num']}\n{x['example3']} : {x['num']}", axis=1))
    example_text_o = '\n'.join(theme_o_df.apply(lambda x: f"{x['example1']} : {x['num']}\n{x['example2']} : {x['num']}\n{x['example3']} : {x['num']}", axis=1))

    def __init__(self,flag_judg_send,flag_judg_receive,flag_type_send,flag_type_receive,flag_meme_send,flag_meme_receive,flag_theme_send,flag_theme_receive,flag_chara_send,flag_chara_receive,flag_log) -> None:
        self.flag_judg_send = flag_judg_send
        self.flag_judg_receive = flag_judg_receive
        self.flag_type_send = flag_type_send
        self.flag_type_receive = flag_type_receive
        self.flag_meme_send = flag_meme_send
        self.flag_meme_receive = flag_meme_receive
        self.flag_theme_send = flag_theme_send
        self.flag_theme_receive = flag_theme_receive
        self.flag_chara_send = flag_chara_send
        self.flag_chara_receive = flag_chara_receive
        self.flag_log = flag_log

    def _update_historys(self,tolker,comment):
        text = f"{tolker}: {comment}"
        self.conversations_list.append(text)
        self.conversations_list = self.conversations_list[-self.historys_limit:]
        self.conversations = "\n".join(self.conversations_list)
        pass

    def main_system(self,listener,comment):
        self.flag_log.put("comment:"+listener + ': ' + comment)
        # 処理：自分宛てのテキストかどうかを判断する
        self.flag_judg_send.put(listener + ': ' + comment)
        self.flag_type_send.put(comment)
        judg = self.flag_judg_receive.get()
        theme_type = self.flag_type_receive.get()
        print("【 test log 】judg:",judg)
        print("【 test log 】type:",theme_type)
        if judg != 1 or not (1 <= theme_type <= 5):
            # False
            self._update_historys(listener,comment)
            self.flag_theme_send.put(("pass",judg))
            return None
        else:
            # True
            # 処理：meme,theme,charaを取得
            self.flag_meme_send.put(comment)
            self.flag_theme_send.put((listener + ': ' + comment,judg))
            self.flag_chara_send.put(listener + ': ' + comment)
            result_meme = self.flag_meme_receive.get()
            result_theme = self.flag_theme_receive.get()
            result_chara = self.flag_chara_receive.get()
            print("【 test log 】result_chara:",result_chara)

            if result_meme[0] != 0:
                # meme判定の場合
                result_theme = result_meme
            # 処理：metaを取得
            # themeの結果からDBを検索してメタ認知を呼び出す
            meta_list = self.meta_df[(self.meta_df['type'] == theme_type) & (self.meta_df['theme'] == result_theme[0])]['meta'].tolist()
            meta_num_list = []
            i=0
            for meta in meta_list:
                i += 1
                meta_num_list.append(str(i) + '. ' + meta)
            meta_text = "\n".join(meta_num_list)
            self.flag_log.put("meta_text:"+meta_text)
            # 取得したテキストをシステムプロンプトに変換する
            meta_prompt = self.op.get_meta_prompt(result_chara,self.conversations,listener + ': ' + comment,result_theme[1],meta_text)
            print("【 test log 】meta_prompt:",meta_prompt)
            #meta_result = self.oa.openai_chat(meta_prompt)
            meta_result = self.ca.claude_chat(meta_prompt)
            print("【 test log 】meta_result:",meta_result)
            self.flag_log.put("meta_result:"+meta_result)
            # 結果を校正
            meta_match = re.search(r'\d+', meta_result)
            meta_num = int(meta_match.group(0))
            meta_selected = self.meta_df[(self.meta_df['type'] == theme_type) & (self.meta_df['theme'] == result_theme[0]) & (self.meta_df['num'] == meta_num)]['meta'].values[0]
            print("【 test log 】meta_selected:",meta_selected)
            # 処理：actionを取得
            # metaの結果からDBを検索してアクションを呼び出す
            action = self.action_df[(self.action_df['type'] == theme_type) & (self.action_df['theme'] == result_theme[0]) & (self.action_df['meta'] == meta_num)]['action'].tolist()
            action_text = "\n".join(action)
            self.flag_log.put("action_text:"+action_text)
            print("【 test log 】action_text:",action_text)
            # 取得したテキストをシステムプロンプトに変換する
            preOut_prompt = self.op.get_preOut_prompt(result_chara,self.conversations,listener + ': ' + comment,meta_selected,action_text)
            print("【 test log 】preOut_prompt:",preOut_prompt)
            #preOut_result = self.oa.openai_chat(preOut_prompt)
            preOut_result = self.ca.claude_chat(preOut_prompt)
            # テキストの校正
            preOut_result = preOut_result.replace("aiアサクサ:","")
            print("【 test log 】preOut_result:",preOut_result)
            self.flag_log.put("preOut_result:"+preOut_result)

            # 会話履歴の更新
            self._update_historys(listener,comment)
            self._update_historys(self.aituber_name,preOut_result)
            
            """
            # 処理：reviseOutputを取得
            # preOutの結果をシステムプロンプトに変換する
            reviseOutput_prompt = self.op.get_reviseOutput_prompt(result_chara,self.conversations,listener + ': ' + comment,meta_selected,preOut_result)
            print("【 test log 】reviseOutput_prompt:",reviseOutput_prompt)
            reviseOutput_result = self.oa.openai_chat(reviseOutput_prompt)
            print("【 test log 】reviseOutput_result:",reviseOutput_result)
            self.flag_log.put("reviseOutput_result:"+reviseOutput_result)

            # 会話履歴の更新
            self._update_historys(listener,comment)
            self._update_historys(self.aituber_name,reviseOutput_result)
            return reviseOutput_result
            """
            return preOut_result


    def subprocces_1(self,flag_judg_send,flag_judg_receive,flag_meme_send,flag_meme_receive,flag_log):
        logging.basicConfig(filename='./log/subprocces1.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        try:
            while True:
                # 初期化
                judg_result = None
                result = None
                meme_result = None
                # flag_judgの取得
                comment = flag_judg_send.get()
                judg_prompt = self.op.get_judg_prompt(self.conversations,comment)
                logging.info("judg_prompt: %s", judg_prompt)
                #judg_result = self.oa.openai_chat(judg_prompt)
                judg_result = self.ca.claude_chat(judg_prompt)
                logging.info("judg_result: %s", judg_result)
                flag_log.put("judg_result:"+judg_result)
                # テキストを校正
                if "1" in judg_result:
                    result = 1
                else:
                    result = 0
                # 結果の送信
                flag_judg_receive.put(result)
                
                # 次に進むかを判断する
                if result == 0:
                    continue
                elif result == 1:
                    # memeの取得
                    comment = flag_meme_send.get()
                    # meme情報RAG取得
                    meme_text,meme_dict = self.ic.search_index("meme_index",comment)
                    flag_log.put("meme_text:"+meme_text)
                    # 取得したテキストをシステムプロンプトに変換する
                    meme_prompt = self.op.get_meme_prompt(comment,meme_text)
                    logging.info("meme_prompt: %s", meme_prompt)
                    #meme_result = self.oa.openai_chat(meme_prompt)
                    meme_result = self.ca.claude_chat(meme_prompt)
                    logging.info("meme_result: %s", meme_result)
                    flag_log.put("meme_result:"+meme_result)
                    # 結果の校正と送信
                    match = re.search(r'\d+', meme_result)
                    if not match:
                        flag_meme_receive.put([0,None])
                    else:
                        meme_num = int(match.group(0))
                        flag_meme_receive.put([meme_num,meme_dict[meme_num]])
        except Exception as e:
            # エラーをログに記録
            logging.error("An error occurred in subprocess_1: %s", e)

    def subprocces_2(self,flag_type_send,flag_type_receive,flag_theme_send,flag_theme_receive,flag_log):
        logging.basicConfig(filename='./log/subprocces2.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        try:
            while True:
                # 初期化
                type_num  = None
                judg = None
                # flag_typeの取得
                comment = flag_type_send.get()
                type_prompt = self.op.get_type_prompt(comment)
                logging.info("type_prompt: %s", type_prompt)
                flag_log.put("type_prompt:"+type_prompt)
                #type_result = self.oa.openai_chat(type_prompt)
                type_result = self.ca.claude_chat(type_prompt)
                logging.info("type_result: %s", type_result)
                flag_log.put("type_result:"+str(type_result))
                # 結果の校正と送信
                match = re.search(r'\d+', type_result)
                if not match:
                    flag_type_receive.put(0)
                    type_num = 0
                else:
                    type_num = int(match.group(0))
                    flag_type_receive.put(type_num)

                # flag_themeの取得
                comment,judg = flag_theme_send.get()
                # 次に進むかを判断する
                if judg == 0:
                    continue
                elif judg == 1:
                    theme_text = ""
                    example_text = ""
                    theme_df = None
                    if type_num == 1:
                        theme_text = self.theme_text_q
                        example_text = self.example_text_q
                        theme_df = self.theme_q_df
                    elif type_num == 2:
                        theme_text = self.theme_text_o
                        example_text = self.example_text_o
                        theme_df = self.theme_o_df
                    elif type_num == 3:
                        theme_text = self.theme_text_r
                        example_text = self.example_text_r
                        theme_df = self.theme_r_df
                    else:
                        theme_text = self.theme_text_c
                        example_text = self.example_text_c
                        theme_df = self.theme_c_df
                    theme_prompt = self.op.get_theme_prompt(comment,theme_text,example_text)
                    flag_log.put("theme_text:"+theme_text)
                    flag_log.put("example_text:"+example_text)
                    logging.info("theme_prompt: %s", theme_prompt)
                    #theme_result = self.oa.openai_chat(theme_prompt)
                    theme_result = self.ca.claude_chat(theme_prompt)
                    logging.info("theme_result: %s", theme_result)
                    flag_log.put("theme_result:"+theme_result)
                    # 結果の校正と送信
                    match = re.search(r'\d+', theme_result)
                    if not match:
                        flag_theme_receive.put([0,None])
                    else:
                        theme_num = int(match.group(0))
                        # dataframeから値の取得
                        theme = theme_df[theme_df['num'] == theme_num]['theme'].values[0]
                        flag_theme_receive.put([theme_num,theme])
        except Exception as e:
            # エラーをログに記録
            logging.error("An error occurred in subprocess_2: %s", e)

    def subprocces_3(self,flag_chara_send,flag_chara_receive,flag_log):
        logging.basicConfig(filename='./log/subprocces3.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        try:
            while True:
                # 初期化
                chara_text = None
                # flag_themeの取得
                comment = flag_chara_send.get()
                # chara情報RAG取得
                chara_text = self.ic.search_index("chara_index",comment)
                flag_log.put("chara_text:"+chara_text)
                chara_prompt = self.op.get_chara_prompt(comment,chara_text)
                logging.info("chara_prompt: %s", chara_prompt)
                #chara_result = self.oa.openai_chat(chara_prompt)
                chara_result = self.ca.claude_chat(chara_prompt)
                logging.info("chara_result: %s", chara_result)
                flag_log.put("chara_result:"+chara_result)
                # 結果の送信
                flag_chara_receive.put(chara_result)
        except Exception as e:
            # エラーをログに記録
            logging.error("An error occurred in subprocess_3: %s", e)