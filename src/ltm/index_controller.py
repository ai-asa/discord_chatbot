# %%

"""
ここではindex_controllerを呼び出して、
csvからメタデータ付きデータベースの作成を行うスクリプトを作成する。

index名を指定し、a,q,metadata(リスト)を渡すと、indexにデータを追加する関数
csv名を指定すると、データをパースして順番にindexにデータを追加する関数
"""

import configparser
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.schema import Document
import pandas as pd
import logging
import os

class IndexController:
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    config_file_path = 'config.txt'
    config = configparser.ConfigParser()
    config.read(config_file_path, encoding='utf-8')
    chara_csv_path = config.get('INDEX', 'chara_csv_path', fallback='./data/index/chara.csv')
    chara_index_path = config.get('INDEX','chara_index_path', fallback='./data/index/')
    meme_index_path = config.get('INDEX','meme_index_path', fallback='./data/index/')
    k_limit = int(config.get('INDEX','k_limit', fallback=5))
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,model="text-embedding-3-large",deployment="text-embedding-3-large")

    def __init__(self) -> None:
        # indexの読み込み
        try:
            self.meme_index = FAISS.load_local(self.meme_index_path, self.embeddings)
        except Exception as e:
            print(f"meme_indexの読み込み中にエラーが発生しました: {e}")
            self.meme_index = None
        try:
            self.chara_index = FAISS.load_local(self.chara_index_path, self.embeddings)
        except Exception as e:
            print(f"chara_indexの読み込み中にエラーが発生しました: {e}")
            self.chara_index = None
        # csvの読み込み
        try:
            self.chara_df = pd.read_csv(self.chara_csv_path, encoding='utf-8-sig')
        except:
            print("作成済みのchara_dfがありません。")
            self.chara_df = pd.DataFrame()
        pass

    def add_index(self,index_name,q,a="",num="") -> bool:

        if index_name == "meme_index":
            meme_q_doc = [Document(page_content=q,metadata=dict(num=num))]
            if self.meme_index:
                self.meme_index.add_documents(meme_q_doc)
            else:
                self.meme_index = FAISS.from_documents(
                    meme_q_doc,
                    self.embeddings,
                    )
            pass
        elif index_name == "chara_index":
            num = ""
            if self.chara_index:
                ids = self.chara_index.index_to_docstore_id
                num = str(len(ids) + 1)
                chara_q_doc = [Document(page_content=q,metadata=dict(num=num))]
                self.chara_index.add_documents(chara_q_doc)
            else:
                num = "1"
                chara_q_doc = [Document(page_content=q,metadata=dict(num=num))]
                self.chara_index = FAISS.from_documents(
                    chara_q_doc,
                    self.embeddings,
                    )
            chara_a_doc = pd.DataFrame({
                    'num':[num],
                    'answer':[a]
                    })
            self.chara_df = pd.concat([self.chara_df,chara_a_doc])
            pass

    def search_index(self,index_name,query):
        logging.basicConfig(filename='./log/indexprocces.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        try:
            if index_name == "meme_index":
                docs = self.meme_index.similarity_search_with_relevance_scores(query,k=self.k_limit)
                search_list = []
                search_dict = []
                search_result = ""
                for document in docs:
                    # documentのtextを抽出する
                    text = document[0].page_content
                    # documentの番号を取得する
                    num = int(document[0].metadata['num']
                                    )                # リストに追加
                    text = str(num) + ". " + text
                    part = {num:text}
                    search_list.append(text)
                    search_dict.append(part)
                # 結合して出力
                search_result = "\n".join(search_list)
                result = (search_result,search_dict)
                return result
            if index_name == "chara_index":
                docs = self.chara_index.similarity_search_with_relevance_scores(query,k=self.k_limit)
                logging.info("docs: %s", docs)
                search_list = []
                search_result = ""
                for document in docs:
                    logging.info("document: %s", document)
                    # documentのtextを抽出する
                    text = document[0].page_content
                    logging.info("text: %s", text)
                    # documentの番号を取得する
                    num = int(document[0].metadata['num'])
                    logging.info("num: %s", num)
                    # dataframeから情報を取得
                    answer = self.chara_df[self.chara_df['num'] == num]['answer'].values[0]
                    logging.info("answer: %s", answer)
                    # リストに追加
                    text = text + ": " + answer
                    search_list.append(text)
                # 結合して出力
                result = "\n".join(search_list)
                logging.info("result: %s", result)
                return result
        except Exception as e:
            # エラーをログに記録
            logging.error("An error occurred in search_index: %s", e)

    def save_index(self):
        self.meme_index.save_local(self.meme_index_path)
        self.chara_index.save_local(self.chara_index_path)
        self.chara_df.to_csv(self.chara_csv_path,encoding='utf-8-sig', index=False)

    def _delete_index(self,id_list) -> None:
        for id in id_list:
            self.q_index.delete([id])
            self.a_df = self.a_df[self.a_df['id'] != id]
        pass

if __name__ == "__main__":
    ic = IndexController()
    q_text = "question"
    a_text = "answer"
    lis_name = "ASA"
    query = "q"
    ic.create_index(lis_name,q_text,a_text,option="history")
    historys,summarys,old_historys,old_summarys = ic.search_lis_index(query,lis_name)


# %%
