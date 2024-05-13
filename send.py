import itchat
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import random
import re
import requests
from openai import OpenAI
from collections import deque


class FixedSizeQueue:
    def __init__(self, size):
        self.head_data = None
        self.size = size
        self.data = deque(maxlen=size)

    def head(self, item):
        self.head_data = item

    def push(self, item):
        if len(self.data) < self.size:
            self.data.append(item)
        else:
            # 如果队列已满，移除最旧的元素，并添加新的元素
            self.data.popleft()
            self.data.append(item)

    def pop(self):
        if len(self.data) > 0:
            return self.data.popleft()
        return None

    def get_queue(self):
        # 将固定元素添加到队列的开头
        mylist = list(self.data)
        mylist.insert(0, self.head_data)
        return mylist
        


fixed_queue = FixedSizeQueue(10)
fixed_queue.head(
    {"role": "system", "content": "你的名字叫小乐，是一个哄女朋友很厉害的人，能找各种机会逗她开心，你称呼她为静静，接下来你会收到一些日常聊天的话，请你用合适的措辞进行回复，回答尽量精简，控制在100字内。"})


def deepseek(text):
    fixed_queue.push({"role": "user", "content": text})
    try:
        client = OpenAI(api_key="sk-cde770386d204a6f937dceb20e47504d", base_url="https://api.deepseek.com")
        response = client.chat.completions.create(model="deepseek-chat", messages=fixed_queue.get_queue())
        res_text = response.choices[0].message.content
        fixed_queue.push({"role": "assistant", "content": res_text[:100]})
    except Exception as e:
        # print(e)
        itchat.send('deepseek发生报错了：' + str(e), toUserName="filehelper")
        res_text = ""
    return res_text


itchat.auto_login(hotReload=True,enableCmdQR=2)
jj = itchat.search_friends(name="Jing")[0] if len(itchat.search_friends(name="Jing")) > 0 else {}
liubai = itchat.search_friends(name="留白")[0] if len(itchat.search_friends(name="留白")) > 0 else {}
print(jj)
obj_list = [jj, liubai]
user_name_list = []
for obj in obj_list:
    if obj.get("UserName"):
        user_name_list.append(obj.get("UserName"))
flag = False


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    global flag
    text = msg.get("Text", "")
    # 文件管理助手
    if msg["ToUserName"] == "filehelper":
        if text == "s":
            flag = True
            itchat.send('开启机器人成功', toUserName="filehelper")
            return
        elif text == "e":
            flag = False
            itchat.send('关闭机器人成功', toUserName="filehelper")
            return
    if not flag:
        return
    if msg["FromUserName"] == jj.get("UserName"):
        if text == "开启":
            flag = True
            return "哈喽，小乐来咯"
        elif text == "关闭":
            flag = False
            return "好的，小乐先走咯"
        else:
            text = deepseek(text)
            if text != "":
                return text
    return


itchat.send('呼叫静静，我是机器人2号，你现在可以找我聊天了', toUserName="filehelper")
itchat.run()
# if __name__ == "__main__":
#     print(deepseek("你好呀"))
#     print(deepseek("今天好累呀"))
#     print(deepseek("今天在下雨"))
#     print(deepseek("不知道明天还会不会下"))
#     print(deepseek("这是第五句了"))
#     print(fixed_queue.get_queue())

#     print(deepseek("再说一句，看看效果"))
#     print(fixed_queue.get_queue())
