#coding:gbk
###################################################################################
#作者：周故意太湖给他
#简介：一款接入了EdgeGPT(newbing)和MockingBird实时语音克隆模型的丁真风味聊天机器人。
#鸣谢：acheong08、babysor
#CommandLine Client
###################################################################################
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from main.voice import DingZhen
from main.gui import GUI
import wx

class BingDingZhen:
    async def main(self):
        init_prompt = ""
        with open("init_prompt.txt","r",encoding = "utf-8") as f:
            init_prompt = f.read()
        cookies = json.loads(open("./bingAI-cookies.json", encoding="utf-8").read()) # 可能会忽略 cookie 选项
        bot = await Chatbot.create(proxy = "http://127.0.0.1:7890",cookies=cookies) #此处添加代理
        dz = DingZhen()
        times = 1
        response = await bot.ask(prompt=init_prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
        result = response["text"]
        dz.synthesize_vocode(result)
        print(f"丁真说：{result}\n{times} of {response['max_messages']}")
        while times != response['max_messages']:
            prompt = input("你说：")
            if prompt == '!exit':
                break
            response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
            result = response["text"]
            dz.synthesize_vocode(result)
            times += 1
            print(f"丁真说：{result}\n{times} of {response['max_messages']}")
        await bot.close()
    def __init__(self):
        asyncio.run(self.main())