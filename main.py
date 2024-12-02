# %%
from main_system import DiscordChatBot
from src.discord.discord_bot_server import start_discord_bot
import traceback
import multiprocessing
import logging

if __name__ == "__main__":
    flag_discord_comment_send = multiprocessing.Queue()
    flag_discord_comment_receive = multiprocessing.Queue()
    flag_judg_send = multiprocessing.Queue()
    flag_judg_receive = multiprocessing.Queue()
    flag_type_send = multiprocessing.Queue()
    flag_type_receive = multiprocessing.Queue()
    flag_meme_send = multiprocessing.Queue()
    flag_meme_receive = multiprocessing.Queue()
    flag_theme_send = multiprocessing.Queue()
    flag_theme_receive = multiprocessing.Queue()
    flag_chara_send = multiprocessing.Queue()
    flag_chara_receive = multiprocessing.Queue()
    flag_log = multiprocessing.Queue()
    db = DiscordChatBot(flag_judg_send,flag_judg_receive,flag_type_send,flag_type_receive,flag_meme_send,flag_meme_receive,flag_theme_send,flag_theme_receive,flag_chara_send,flag_chara_receive,flag_log)
    p1 = multiprocessing.Process(target=db.subprocces_1,args=(flag_judg_send,flag_judg_receive,flag_meme_send,flag_meme_receive,flag_log))
    p2 = multiprocessing.Process(target=db.subprocces_2,args=(flag_type_send,flag_type_receive,flag_theme_send,flag_theme_receive,flag_log))
    p3 = multiprocessing.Process(target=db.subprocces_3,args=(flag_chara_send,flag_chara_receive,flag_log))
    p4 = multiprocessing.Process(target=start_discord_bot,args=(flag_discord_comment_send,flag_discord_comment_receive))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    logging.basicConfig(filename='./log/processlog.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    result = True
    while result == True:
        try:
            listener,comment = flag_discord_comment_receive.get()
            print("【 log 】コメントを受信しました")
            response = db.main_system(listener,comment)
            print("response:", response)
            while not flag_log.empty():
                log = flag_log.get()
                logging.info(log)
            if response:
                flag_discord_comment_send.put(response)
            else:
                flag_discord_comment_send.put(0)
            pass
        except Exception as e:
            print("エラーが発生しました")
            print(traceback.format_exc())
            print(e)
            logging.error("An error occurred in main_procces: %s", e)
            break
# %%
