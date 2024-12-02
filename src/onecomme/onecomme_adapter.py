# %%
import configparser
from dotenv import load_dotenv
import json
import websocket
import multiprocessing
import os
import time
import logging
load_dotenv()

class OnecommeAdapter:
    config_file_path = 'config.txt'
    config = configparser.ConfigParser()
    config.read(config_file_path, encoding='utf-8')
    comment_id = config.get('ONECOMME', 'comment_id')
    def __init__(self):
        self.WS_URL = os.getenv('onecomme_WS_URL')

    def on_open(self):
        pass

    def on_message(self, queue_data, msg):
        try:
            data = json.loads(msg)
        except json.JSONDecodeError as e:
            logging.info(f"JSON decode error: {e}")
            return
        event_type = data.get("type")

        if event_type == "comments":
            comments = data.get("data", {}).get("comments", [])
            if comments:
                for item in comments:
                    comment_data = item.get("data", {})
                    service_id = item.get("id","")
                    if not service_id == self.comment_id:
                        listener = comment_data.get("displayName", "")
                        comment = comment_data.get("comment", "")
                        queue_data.put((listener,comment))
                        logging.info(f"Listener, Comment: {listener}, {comment}")
                        break
            else:
                logging.info("None")

    def on_error(self, error):
        logging.info(f"Error: {error}")

    def on_close(self):
        logging.info("Connection closed")

    def run_websocket(self, queue_data):
        # logger setting
        logging.basicConfig(filename='./log/websocket.log',
                            level=logging.INFO, 
                            format='%(asctime)s - %(message)s')
        # websocket setting
        ws = websocket.WebSocketApp(self.WS_URL + "/sub",
                                            on_open=lambda ws:self.on_open(),
                                            on_message=lambda ws,msg:self.on_message(queue_data,msg),
                                            on_error=lambda ws,error:self.on_error(error),
                                            on_close=lambda ws:self.on_close())
        ws.run_forever()

config_file_path = 'config.txt'
config = configparser.ConfigParser()
config.read(config_file_path, encoding='utf-8')
get_comment_timeout  = int(config.get('ONECOMME', 'get_comment_timeout',fallback=5))
def collect_queue(queue):
    items = []
    try:
        items.append(queue.get(timeout=get_comment_timeout))
        while not queue.empty():
            try:
                item = queue.get_nowait()
                items.append(item)
            except queue.Empty:
                break
    except:
        pass
    return items

def subprocess_onecomme(queue_data):
    oc = OnecommeAdapter()
    oc.run_websocket(queue_data)

if __name__ == "__main__":
    queue_data = multiprocessing.Queue()
    p = multiprocessing.Process(target=subprocess_onecomme,args=(queue_data,))
    p.start()
    #run_subprocess(queue_data)
    while True:
        data_list = collect_queue(queue_data)
        data = data_list[0] if data_list else print("No comment")
        if data:
            print(data)
        time.sleep(5)
"""
わんコメの取得データ形式
{'type': 'comments', 
 'data': {'comments': [
     {'id': '17467e04-13a6-4654-b3ca-97960d57ccaa', 
      'service': 'youtube', 
      'name': 'Youtube',
      'url': 'https://youtube.com/live/nr2zMMol8AI?feature=share', 
      'color': {'r': 72, 'g': 89, 'b': 255}, 
      'data': {'id': 'yt-ChwKGkNJaWctdUQ0NW9NREZVVEJ3Z1FkT0k4QVF3', 
               'liveId': 'nr2zMMol8AI', 
               'userId': 'yt-UC-t97bQRf_Sz9G6wgHleZxg', 
               'name': 'ASA | dtmchannel', 
               'profileImage': 'https://yt4.ggpht.com/xLi8X48x0GxJ3ro8PZXqIE9nRVxNwLhG4op6uoHzmUxrOBIhtscCwZNc6TBFpuGohtiA-zYA3A=s32-c-k-c0x00ffffff-no-rj', 
               'badges': [{'label': 'OWNER', 'url': ''}], 
               'isOwner': True, 
               'isModerator': False, 
               'isMember': False, 
               'autoModerated': False, 
               'hasGift': False, 
               'comment': 'こん', 
               'timestamp': '2024-01-18T12:31:48.701Z', 
               'displayName': 'ASA | dtmchannel', 
               'originalProfileImage': 'https://yt4.ggpht.com/xLi8X48x0GxJ3ro8PZXqIE9nRVxNwLhG4op6uoHzmUxrOBIhtscCwZNc6TBFpuGohtiA-zYA3A=s32-c-k-c0x00ffffff-no-rj'}, 
               'meta': {'no': 4, 'tc': 4, 'interval': 259620}}
               ], 
               'userNameMap': {}, 
               'options': {'skipSpeech': False, 'init': False}}}
"""
# %%
