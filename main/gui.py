###################################################################################
#作者：周故意太湖给他
#简介：一款接入了EdgeGPT(newbing)和MockingBird实时语音克隆模型的丁真风味聊天机器人。
#鸣谢：acheong08、babysor
###################################################################################
import wx
from main.voice import DingZhen
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import asyncio, json
import speech_recognition as sr
class GUI(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"电子丁真    by周故意太湖给他",(500,200), (750,700))
        panel = wx.Panel(self)
        icon = wx.Icon('main/icon/dz.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.chat_times = 1
        self.is_AI_loaded = False
        self.is_models_loaded = False
        self.is_shutup = False
        self.default_text = "info:"
        self.load_models_button = wx.Button(panel, label = "加载丁真嘴巴")
        self.load_bing_button = wx.Button(panel,label = "加载丁真脑壳")
        self.info_label = wx.StaticText(panel,label = self.default_text,size = (700,50))
        self.send_text = wx.TextCtrl(panel,size = (600,20))
        self.send_button = wx.BitmapButton(panel,bitmap = wx.Image("main/icon/send.ico").ConvertToBitmap())
        self.voice_button = wx.BitmapButton(panel,bitmap = wx.Image("main/icon/voice.ico").ConvertToBitmap())
        self.send_button.Disable()
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(self.send_text,flag = wx.ALIGN_LEFT|wx.ALL,border = 0)
        box1.Add(self.send_button,flag = wx.ALIGN_LEFT|wx.ALL,border = 5)
        box1.Add(self.voice_button,flag = wx.ALIGN_LEFT|wx.ALL,border = 5)
        self.scroller = wx.ScrolledWindow(panel,size = (600,700))#添加self.scroller容器到panel上
        self.scroller.SetScrollbars(60,60,1000,600)
        self.scroller.SetScrollRate(0,20)
        self.reply_panel = wx.Panel(self.scroller,size = (600,0))
        self.reply_texts:list = []
        self.box7 = wx.BoxSizer(wx.VERTICAL)
        self.reply_panel.SetSizer(self.box7)
        self.replay_button = wx.Button(panel,label = "回放")
        self.reset_button = wx.Button(panel,label = "重置")
        self.shutup_button = wx.Button(panel,label = "雪豹闭嘴")
        self.reset_button.Disable()
        self.about_button = wx.Button(panel,label = "注意事项")
        self.replay_button.Disable()
        self.box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.box2.Add(self.scroller,flag = wx.ALIGN_LEFT|wx.ALL,border = 0)
        box4 = wx.BoxSizer(wx.VERTICAL)
        box4.Add(self.reset_button,flag = wx.ALIGN_CENTRE|wx.ALL,border = 15)
        box4.Add(self.replay_button,flag = wx.ALIGN_CENTRE|wx.ALL,border = 15)
        box4.Add(self.shutup_button,flag = wx.ALIGN_CENTRE|wx.ALL,border = 15)
        box4.Add(self.about_button,flag = wx.ALIGN_CENTRE|wx.ALL,border = 15)
        self.box2.Add(box4,wx.ALL,border = 15)
        box3 = wx.BoxSizer(wx.VERTICAL)
        box5 = wx.BoxSizer(wx.HORIZONTAL)
        image = wx.Image("main/res/dz.jpg").ConvertToBitmap()
        bmp = wx.StaticBitmap(panel,bitmap = image)
        box5.Add(bmp,flag = wx.ALIGN_LEFT|wx.ALL,border = 15)
        dz_text = wx.StaticText(panel,label = "引应丁真：\n鉴定为：纯纯的必様")
        box6 = wx.BoxSizer(wx.VERTICAL)
        box6.Add(dz_text,flag = wx.ALIGN_LEFT|wx.ALL,border = 15)
        box6.Add(self.load_models_button,1,flag = wx.ALIGN_LEFT|wx.ALL,border = 15)
        box6.Add(self.load_bing_button,1,flag = wx.ALIGN_LEFT|wx.ALL,border = 15)
        box5.Add(box6,flag = wx.ALIGN_LEFT|wx.ALL,border = 15)
        box3.Add(box5,flag = wx.ALIGN_LEFT|wx.ALL,border = 0)
        box3.Add(self.info_label,flag = wx.ALIGN_LEFT|wx.ALL,border = 0)
        box3.Add(box1,flag = wx.ALIGN_LEFT|wx.ALL,border = 0)
        box3.Add(self.box2,flag = wx.EXPAND|wx.ALL,border = 0)
        panel.SetSizer(box3)
        #添加按钮点击事件
        self.load_models_button.Bind(wx.EVT_BUTTON,self.load_models_button_click)
        self.load_bing_button.Bind(wx.EVT_BUTTON,self.load_bing_button_click)
        self.send_button.Bind(wx.EVT_BUTTON,self.send_button_click)
        self.voice_button.Bind(wx.EVT_BUTTON,self.voice_button_click)
        self.replay_button.Bind(wx.EVT_BUTTON,self.replay_button_click)
        self.about_button.Bind(wx.EVT_BUTTON,self.about_button_click)
        self.reset_button.Bind(wx.EVT_BUTTON,self.reset_button_click)
        self.shutup_button.Bind(wx.EVT_BUTTON,self.shutup_button_click)
    def load_models_button_click(self,event):
        self.info_label.SetLabelText(self.default_text + "正在加载语音模型，请稍后...")
        try:
            self.dz = DingZhen()
            self.info_label.SetLabelText(self.default_text + "完成！")
            self.is_models_loaded = True
            if self.is_AI_loaded and self.is_models_loaded:
                self.send_button.Enable()
                self.replay_button.Enable()
                self.reset_button.Enable()
        except Exception as e:
            self.info_label.SetLabelText(self.default_text + f"运异丁真，鉴定为：没模擎亡源声的出声\n{e}")
            print(e)
    def load_bing_button_click(self,event):
        asyncio.run(self.load_AI())
    async def load_AI(self):
        self.info_label.SetLabelText(self.default_text + "正在加载BingAI，请稍后...")
        try:
            init_prompt = ""
            with open("init_prompt.txt","r",encoding = "utf-8") as f:
                init_prompt = f.read()
            cookies = json.loads(open("./bingAI-cookies.json", encoding="utf-8").read())
            self.bot = await Chatbot.create(proxy = "http://127.0.0.1:7890",cookies=cookies) #此处添加代理
            response = await self.bot.ask(prompt=init_prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
            self.is_AI_loaded = True
            if self.is_AI_loaded and self.is_models_loaded:
                self.send_button.Enable()
                self.replay_button.Enable()
                self.reset_button.Enable()
            self.reply_texts.append(wx.StaticText(self.reply_panel,label = f'{response["text"]}\n{self.chat_times}共{response["max_messages"]}'))
            self.reply_texts[self.chat_times - 1].SetBackgroundColour("white")
            self.box7.Add(self.reply_texts[self.chat_times - 1],flag = wx.ALIGN_LEFT|wx.ALL,border = 5)
            self.reply_panel.Fit()
            self.info_label.SetLabelText(self.default_text + "完成！")
            self.load_bing_button.Disable()
            if not self.is_shutup:
                self.dz.synthesize_vocode(response["text"])
                self.dz.speak()
        except Exception as e:
            self.info_label.SetLabelText(self.default_text + f"运异丁真，鉴定为：纯纯的没有大脑\n{e}")
            print(e)
    def send_button_click(self,event):
        asyncio.run(self.get_reply())
    async def get_reply(self):
        prompt = push_enter(self.send_text.GetValue())
        self.reply_texts.append(wx.StaticText(self.reply_panel,label = prompt))
        self.reply_texts[self.chat_times * 2 - 1].SetBackgroundColour("purple")
        self.reply_texts[self.chat_times * 2 - 1].SetForegroundColour("white")
        self.box7.Add(self.reply_texts[self.chat_times * 2 - 1],flag = wx.ALIGN_RIGHT|wx.RIGHT,border = 30)
        self.reply_panel.Fit()
        self.info_label.SetLabelText(self.default_text + "妈妈生的...")
        try:
            response = await self.bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
            self.chat_times += 1
            speak_words = response["text"]
            response["text"] = push_enter(speak_words)
            self.reply_texts.append(wx.StaticText(self.reply_panel,label = f'{response["text"]}\n{self.chat_times}共{response["max_messages"]}'))
            self.reply_texts[2 * self.chat_times - 2].SetBackgroundColour("white")
            self.box7.Add(self.reply_texts[self.chat_times * 2 - 2],flag = wx.ALIGN_LEFT|wx.ALL,border = 5)
            self.reply_panel.Fit()
            self.info_label.SetLabelText(self.default_text + "完成！")
            if not self.is_shutup:
                self.dz.synthesize_vocode(speak_words)
                self.dz.speak()
        except Exception as e:
            self.info_label.SetLabelText(self.default_text + f"运异丁真，鉴定为：珠脑过载\n{e}")
            self.reply_texts[self.chat_times * 2 - 1].Destroy()
            del self.reply_texts[self.chat_times * 2 - 1]
            print(e)
    def replay_button_click(self,event):
        self.dz.speak()
    def about_button_click(self,event):
        msg = '项目名称：电子丁真\
        \n作者：周故意太湖给他\
        \n简介：这是一款接入了new bing的API(EdgeGPT)和MockingBird实时语音克隆模型的丁真风味聊天机器人。\
        \n特别鸣谢：acheong08、babysor，他们提供了本程序所需的API和模型训练程序，其中我引用了MockingBird程序中的部分代码。\
        \n提醒：1、千万不要尝试让丁真生成图片（本程序没有接入生成图片的接口），或说与图片生成有关的提示语，比如“看看...”“展示...”“...是什么样的”，可能的后果包括但不限于：无限的真人验证、询问后不再有回复。\
        \n2、若加载bingAI时报错与“CAPTCHA”有关，请在www.bing.com/chat中登录你的账号并完成真人验证。\
        \n3、本程序仅供学习交流娱乐使用，严禁用于攻击、诋毁、恶意中伤他人。\
        \n4、未尽事宜，见诸README.md'
        msg_box = wx.MessageDialog(None,msg,"注意事项")
        msg_box.ShowModal()
    def reset_button_click(self,event):
        asyncio.run(self.reset())
    async def reset(self):
        for text in self.reply_texts:
            text.Destroy()
        self.reply_texts.clear()
        await self.bot.close()
        self.send_button.Disable()
        self.replay_button.Disable()
        self.reset_button.Disable()
        self.is_AI_loaded = False
        self.chat_times = 1
        self.info_label.SetLabelText(f"{self.default_text}重置成功！点击“加载丁真脑壳”以开始新聊天")
        self.load_bing_button.Enable()
    def shutup_button_click(self,event):
        if not self.is_shutup:
            self.is_shutup = True
            self.replay_button.Disable()
            self.shutup_button.SetLabelText("纯纯出声")
        else:
            self.is_shutup = False
            if self.is_AI_loaded and self.is_models_loaded:
                self.replay_button.Enable()
            self.shutup_button.SetLabelText("雪豹闭嘴")
    def voice_button_click(self,event):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.info_label.SetLabelText(self.default_text + "请说话...")
                audio = r.listen(source)
                self.info_label.SetLabelText(self.default_text + "识别中...")
                self.send_text.SetValue(r.recognize_google(audio,language = "zh-CN"))
                self.info_label.SetLabelText(self.default_text + "完成！")
        except Exception as e:
            self.info_label.SetLabelText(self.default_text + f"语噎丁真，鉴定为：出声啊，你\n{e}")
def push_enter(text) -> str:
    char_list = list(text)
    for i in range(1,int(len(char_list) / 20) + 1):
                char_list.insert(i * 20 + i - 1 ,"\n")
    return ''.join(char_list).strip()

