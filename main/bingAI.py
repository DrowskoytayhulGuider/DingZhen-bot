#coding:gbk
###################################################################################
#���ߣ��ܹ���̫������
#��飺һ�������EdgeGPT(newbing)��MockingBirdʵʱ������¡ģ�͵Ķ����ζ��������ˡ�
#��л��acheong08��babysor
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
        cookies = json.loads(open("./bingAI-cookies.json", encoding="utf-8").read()) # ���ܻ���� cookie ѡ��
        bot = await Chatbot.create(proxy = "http://127.0.0.1:7890",cookies=cookies) #�˴���Ӵ���
        dz = DingZhen()
        times = 1
        response = await bot.ask(prompt=init_prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
        result = response["text"]
        dz.synthesize_vocode(result)
        print(f"����˵��{result}\n{times} of {response['max_messages']}")
        while times != response['max_messages']:
            prompt = input("��˵��")
            if prompt == '!exit':
                break
            response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
            result = response["text"]
            dz.synthesize_vocode(result)
            times += 1
            print(f"����˵��{result}\n{times} of {response['max_messages']}")
        await bot.close()
    def __init__(self):
        asyncio.run(self.main())