# %%
from src.ltm.index_controller import IndexController
import configparser
import pandas as pd

config_file_path = 'config.txt'
config = configparser.ConfigParser()
config.read(config_file_path, encoding='utf-8')
init_chara_csv_path = config.get('INDEX', 'init_chara_csv_path', fallback='./data/chara.csv')
meme_csv_path = config.get('INDEX', 'meme_csv_path', fallback='./data/meme.csv')
chara_df = pd.read_csv(init_chara_csv_path, encoding='utf-8-sig')
meme_df = pd.read_csv(meme_csv_path, encoding='utf-8-sig')
ic = IndexController()

if __name__ == "__main__":
    # dataframeをパース
    for index, row in chara_df.iterrows():
        ic.add_index("chara_index",row['q'],a=row['a'])
    for index, row in meme_df.iterrows():
        ic.add_index("meme_index",row['theme'],num=row['num'])
    ic.save_index()


# %%
