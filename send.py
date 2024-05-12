import itchat
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import random
import re
import requests
from openai import OpenAI


deepseekMessage = [{"role": "system", "content": "你是一个哄女朋友很厉害的人，能找各种机会逗她开心，你称呼她为静静，接下来你会收到一些日常聊天的话，请你用合适的措辞进行回复。"}]


def deepseek(text):
    deepseekMessage = [{"role": "system", "content": "你是一个哄女朋友很厉害的人，能找各种机会逗她开心，你称呼她为静静，接下来你会收到一些日常聊天的话，请你用合适的措辞进行回复。"},
                       {"role": "user", "content": text}]
    try:
        client = OpenAI(api_key="sk-cde770386d204a6f937dceb20e47504d", base_url="https://api.deepseek.com")
        response = client.chat.completions.create(model="deepseek-chat", messages=deepseekMessage)
        res_text = response.choices[0].message.content  # deepseekMessage.append({"role": "assistant", "content": res_text})
    except Exception as e:
        itchat.send('deepseek发生报错了：' + str(e), toUserName=user_name_list[1])
        res_text = ""
    return res_text


itchat.auto_login(hotReload=True)
obj_list = [itchat.search_friends(name="Jing")[0] if len(itchat.search_friends(name="Jing")) > 0 else {},
            itchat.search_friends(name="留白")[0] if len(itchat.search_friends(name="留白")) > 0 else {}]
user_name_list = []
for obj in obj_list:
    if obj.get("UserName"):
        user_name_list.append(obj.get("UserName"))


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    global flag
    text = msg.get("Text", "")
    # 文件管理助手
    if msg["ToUserName"] == "filehelper":
        if text == "sr":
            flag = True
            itchat.send('开启机器人成功', toUserName=user_name_list[1])
            return
        elif text == "er":
            flag = False
            itchat.send('关闭机器人成功', toUserName=user_name_list[1])
            return
    if not flag:
        return
    if msg["FromUserName"] in user_name_list:
        text = deepseek(text)
        print("问题为：", msg.get("Text", ""))
        print("响应为：", text)
        if text != "":
            return text
    return


@itchat.msg_register(itchat.content.PICTURE)
def pic_reply(msg):
    if msg["ToUserName"] == "filehelper":
        msg.download(msg.fileName)
        typeSymbol = {itchat.content.PICTURE: 'img', itchat.content.VIDEO: 'vid', }.get(msg.type, 'fil')
        print('@%s@%s' % (typeSymbol, msg.fileName))
        return '@%s@%s' % (typeSymbol, msg.fileName)


itchat.send('呼叫静静，我是机器人2号，你现在可以找我聊天了', toUserName=user_name_list[0])
itchat.run()
