import itchat
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import random
import re
import requests
from openai import OpenAI


# 阿里云接口
# "set DASHSCOPE_API_KEY=sk-6870bf6315904a358da8a0860c357c0d"
def call_with_messages(text):
    messages = [{'role': 'system', 'content': '帮忙回复女朋友消息的机器人。'},
                {'role': 'user', 'content': "女朋友对我说：{}。我该怎么幽默风趣的回复她。只返回一句对她说的话".format(text)}]
    gen = Generation()
    response = gen.call(Generation.Models.qwen_v1, enable_search=True, messages=messages, seed=random.randint(1, 99999), result_format='message',
                        # set the result is message format.
                        )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (response.request_id, response.status_code, response.code, response.message))
    try:
        if response.status_code == HTTPStatus.OK:
            res_text = response.output.choices[0].message.content
            my_list = re.findall(r'“([^“]*)”', res_text)
            if len(my_list) > 0:
                res_text = my_list[0]
            else:
                res_text = "我没想好怎么说"
        else:
            res_text = "我布吉岛该怎么说"
    except Exception as e:
        print(e)
        res_text = "我出了点问题"
    return res_text


message = [{"role": "user", "content": "你是一个哄女朋友很厉害的人，能找各种机会逗她开心，你称呼她为静静，接下来你会收到一些日常聊天的话，请你用合适的措辞进行回复。"}]
flag = False


def qqPilot(text):
    api_key = \
        "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmhjSEFpT2lKd1pYSnpiMjVoYkMxdGFXeHZjR1Z1WnlJc0ltTnlaV0YwWlY5aGRDSTZNVFk1TkRBNE9UTXpOU3dpYjNKbklqb2k2SVctNks2djVZV3M1WS00TC1XdGtPV0ZyT1dQdU9lN2hPZTdoeV9vaGI3b3JxX292NURva0tYbHJaRGxoYXpsajdndlZFVkhMZVd1b3VhSXQtYWNqZVdLb2VtRHFDX21pSkRwZzcza3VwSG1tYnJtbkkwdjVicVU1NVNvNUxxbjVaT0I1NkNVNVktUjVMaXQ1Yi1ETC1pX2tPaVFwZVc4Z09XUGtlZTdoQ0lzSW05M2JtVnlJam9pYldsc2IzQmxibWNpZlEuTkd5dDBVNjJXSmw4bUdSUnN1RDZNTW5mMktMM1ZNYm13MXFyTnNuVkdIWQ=="
    try:
        message.append({"role": "user", "content": text})
        response = requests.post("https://api-qpilot.woa.com/v1/chat/completions", headers={'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(api_key)},
                                 json={"stream": False, "model": "gpt-4", "messages": message, })
        res_text = response.json()["choices"][0]["message"]["content"]
        message.append({"role": "assistant", "content": res_text})
    except Exception as e:
        print(e)
        res_text = ""
    return res_text


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
