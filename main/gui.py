import queue
import re
import threading
import time

import cv2
import pyperclip
import speech_recognition as sr
import wx
import wx.media
from openai import OpenAI

from main.voice import DingZhen

with open("DeepSeek_API.txt", "r", encoding="utf-8") as file:
    api_key = file.read()
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=api_key
)
map = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九",
       "-": "负", "+": "加", "咯": "lo", "咳": "壳", "⁓": "~"}
message = []
content = ""

class MessageBlock(wx.StaticText):
    def __init__(self, parent, msg, bgColor: wx.Colour, txtColor: wx.Colour):
        super().__init__(parent, label=msg + "\n\n")
        # 让StaticText能够通过字数先确定文本框大小
        self.msg = msg
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.bgColor = bgColor
        self.txtColor = txtColor
        self.SetFont(font=wx.Font(10, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_MAX,
                                  wx.FONTWEIGHT_MAX, False, "宋体"))

    def OnPaint(self, event):
        paint = wx.PaintDC(self)
        paint.SetBackground(wx.Brush(wx.Colour(240, 240, 240)))
        paint.Clear()
        gc = wx.GraphicsContext.Create(paint)
        if gc:
            w, h = self.GetSize()
            path = gc.CreatePath()
            gc.SetFont(wx.Font(10, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_BOLD, False, "黑体"), self.txtColor)
            line_height = gc.GetTextExtent("人")[1]
            gc.SetBrush(wx.Brush(self.bgColor))
            gc.DrawRoundedRectangle(0, 0, w, h - line_height + 2, 5)

            # gc.FillPath(path)
            th = gc.GetTextExtent(self.msg)[1]
            gc.DrawText(self.msg, 2, (h - line_height - th) / 2 + 2)


def reply_text_handler(rep) -> str:
    rep = re.sub(r"[^\u0000-\uffff]+?", "，", rep)
    rep = re.sub(r"（[\u0000-\uffff]*?）", "，", rep)
    rep = re.sub(r"\([\u0000-\uffff]*?\)", "，", rep)
    rep = re.sub(r"\[[\u0000-\uffff]*?]", "，", rep)
    rep = re.sub(r"【[\u0000-\uffff]*?】", "，", rep)
    rep = re.sub(r"<[\u0000-\uffff]*?>", "，", rep)
    rep = re.sub(r"[《,》]", "", rep)
    rep = re.sub(r"\{[\u0000-\uffff]*?}", "，", rep)
    rep = re.sub(r"，+", "，", rep)
    rep = re.sub(r"\.{2,}", "，", rep)
    rep = "".join([rep[i] if rep[i] not in map else map[rep[i]] for i in range(len(rep))])
    return rep


class GUI(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "电子丁真    by周故意太湖给他", size=(750, 700))
        panel = wx.Panel(self)
        icon = wx.Icon('main/icon/dz.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.is_shutup = False
        self.default_text = "info: "
        self.info_label = wx.StaticText(panel, label=self.default_text, size=(700, 50))
        self.send_text = wx.TextCtrl(panel, size=(600, 40), style=wx.TE_MULTILINE)
        self.send_button = wx.BitmapButton(panel, bitmap=wx.Image("main/icon/send.ico").ConvertToBitmap())
        self.voice_button = wx.BitmapButton(panel, bitmap=wx.Image("main/icon/voice.ico").ConvertToBitmap())
        self.video_viewer = wx.StaticBitmap(panel)
        # self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.play_video_stream, self.timer)
        # self.send_button.Disable()
        self.EnableMaximizeButton(False)
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(self.send_text, flag=wx.ALIGN_LEFT | wx.ALL, border=0)
        box1.Add(self.send_button, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        box1.Add(self.voice_button, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.scroller = wx.ScrolledWindow(panel, size=(600, 700))  # 添加self.scroller容器到panel上
        self.scroller.SetScrollbars(60, 60, 1000, 600)
        self.scroller.SetScrollRate(0, 20)
        self.reply_panel = wx.Panel(self.scroller, size=(600, 0))
        self.reply_texts: list = []
        self.box7 = wx.BoxSizer(wx.VERTICAL)
        self.reply_panel.SetSizer(self.box7)
        self.load_models_button = wx.Button(panel, label="选择语音模型")
        self.edit_prompt_button = wx.Button(panel, label="编辑提示文本")
        self.replay_button = wx.Button(panel, label="回放")
        self.reset_button = wx.Button(panel, label="重置")
        self.anime_switch = wx.Button(panel, label="关闭动画")
        self.shutup_button = wx.Button(panel, label="雪豹闭嘴")
        self.copy_button = wx.Button(panel, label="复制对话")
        # self.reset_button.Disable()
        self.about_button = wx.Button(panel, label="注意事项")
        # self.replay_button.Disable()
        self.box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.box2.Add(self.scroller, flag=wx.ALIGN_LEFT | wx.ALL, border=0)
        # self.is_running = True
        box4 = wx.BoxSizer(wx.VERTICAL)
        box4.Add(self.replay_button, flag=wx.ALIGN_CENTRE | wx.ALL, border=15)
        box4.Add(self.reset_button, flag=wx.ALIGN_CENTRE | wx.ALL, border=15)
        box4.Add(self.anime_switch, flag=wx.ALIGN_CENTRE | wx.ALL, border=15)
        box4.Add(self.shutup_button, flag=wx.ALIGN_CENTRE | wx.ALL, border=15)
        box4.Add(self.copy_button, flag=wx.ALIGN_CENTRE | wx.ALL, border=15)
        box4.Add(self.about_button, flag=wx.ALIGN_CENTRE | wx.ALL, border=15)
        self.box2.Add(box4, wx.ALL, border=15)
        box3 = wx.BoxSizer(wx.VERTICAL)
        box5 = wx.BoxSizer(wx.HORIZONTAL)
        image = wx.Image("main/res/dsdz.jpg").ConvertToBitmap()
        bmp = wx.StaticBitmap(panel, bitmap=image)
        box5.Add(bmp, flag=wx.ALIGN_LEFT | wx.ALL, border=15)
        dz_text = wx.StaticText(panel, label="接入DeepSeek-R1的聊天机器人")
        box6 = wx.BoxSizer(wx.VERTICAL)
        box6.Add(dz_text, flag=wx.ALIGN_LEFT | wx.ALL, border=15)
        box6.Add(self.load_models_button, 1, flag=wx.ALIGN_LEFT | wx.ALL, border=15)
        box6.Add(self.edit_prompt_button, 1, flag=wx.ALIGN_LEFT | wx.ALL, border=15)
        box5.Add(box6, flag=wx.ALIGN_LEFT | wx.ALL, border=15)
        box5.Add(self.video_viewer, flag=wx.ALIGN_LEFT | wx.ALL, border=15)
        box3.Add(box5, flag=wx.ALIGN_LEFT | wx.ALL, border=0)
        box3.Add(self.info_label, flag=wx.ALIGN_LEFT | wx.ALL, border=0)
        box3.Add(box1, flag=wx.ALIGN_LEFT | wx.ALL, border=0)
        box3.Add(self.box2, flag=wx.EXPAND | wx.ALL, border=0)
        panel.SetSizer(box3)
        # self.load_models_button.Bind(wx.EVT_BUTTON, self.load_models_button_click)
        self.send_button.Bind(wx.EVT_BUTTON, self.send_button_click)
        self.voice_button.Bind(wx.EVT_BUTTON, self.voice_button_click)
        self.replay_button.Bind(wx.EVT_BUTTON, self.replay_button_click)
        self.about_button.Bind(wx.EVT_BUTTON, self.about_button_click)
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset_button_click)
        self.shutup_button.Bind(wx.EVT_BUTTON, self.shutup_button_click)
        self.copy_button.Bind(wx.EVT_BUTTON, self.copy_button_click)
        self.anime_switch.Bind(wx.EVT_BUTTON, self.switch_anime)
        self.edit_prompt_button.Bind(wx.EVT_BUTTON, self.edit_prompt_button_click)
        self.load_models_button.Bind(wx.EVT_BUTTON, self.load_models_button_click)
        # self.before_queue = queue.Queue()
        self.get_queue = queue.Queue()
        self.handle_queue = queue.Queue()
        self.speak_queue = queue.Queue()
        self.video_queue = queue.Queue()
        self.is_anime = True
        # self.before_thread = threading.Thread(target=self.do_before_get, args=(self.before_queue, self.get_queue))
        self.get_thread = threading.Thread(target=self.do_get_from_ds, args=(self.get_queue, self.handle_queue))
        self.handle_thread = threading.Thread(target=self.do_handle_ds, args=(self.handle_queue, self.speak_queue))
        self.speak_thread = threading.Thread(target=self.do_speak_ds, args=(self.speak_queue,))
        self.video_thread = threading.Thread(target=self.play_video_stream, args=(self.video_queue,))
        # self.before_thread.start()
        self.get_thread.start()
        self.handle_thread.start()
        self.speak_thread.start()
        self.video_thread.start()
        try:
            self.dz = DingZhen()
        except Exception as e:
            self.info_label.SetLabelText(self.default_text + f"运异丁真，鉴定为：没模擎亡源声的出声\n{e}")
        self.info_label.SetLabelText(self.default_text + f"请在下方文本框中输入文字。")
        self.Center()

    def switch_anime(self, event):
        if self.is_anime:
            self.anime_switch.SetLabelText("开启动画")
        else:
            self.anime_switch.SetLabelText("关闭动画")
        self.is_anime = not self.is_anime

    def play_video_stream(self, video_queue: queue.Queue):
        while threading.main_thread().is_alive():
            cap = video_queue.get()
            while True:
                ret, frame = cap.read()
                if not ret:
                    cap.release()
                    break
                channel = frame.shape[2]
                if channel == 3:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                elif channel == 4:
                    frame = frame[:, :, 3]
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                scale = 0.18
                frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
                height, width, _ = frame.shape
                image = wx.ImageFromBuffer(width, height, frame.tobytes())
                bitmap = wx.BitmapFromImage(image)
                self.video_viewer.SetBitmap(bitmap)
                time.sleep(0.024)

    def send_button_click(self, event):
        self.get_reply()

    def copy_button_click(self, event):
        conversation = ""
        last_role = ""
        for i in message:
            if i["role"] == "user":
                conversation += "你："
            elif i["role"] == "assistant":
                conversation += "丁真："
            if i["role"] != "system":
                conversation += i["content"]
                conversation += "\n"
            last_role = i["role"]
        if content != "" and last_role == "user":
            conversation += "丁真：" + content + "\n"
        pyperclip.copy(conversation)
        self.info_label.SetLabelText(self.default_text + "已将对话内容复制到粘贴板。")

    def load_models_button_click(self, event):
        with wx.FileDialog(self, "选择语音模型路径", wildcard="*.pt", style=wx.FD_OPEN) as file:
            if file.ShowModal() == wx.ID_CANCEL:
                return
            path = file.GetPath()
            self.dz.synthesizer_path = str(path)
            try:
                self.dz.init_synthesizer()
            except Exception as e:
                self.info_label.SetLabelText(self.default_text + f"运异丁真，鉴定为：没模擎亡源声的出声\n{e}")
            # print(path)

    def edit_prompt_button_click(self, event):
        EditPromptDialog(self).Show()

    def do_get_from_ds(self, get_queue: queue.Queue, handle_queue: queue.Queue):
        while threading.main_thread().is_alive():
            rep = ""
            think = ""
            sign = get_queue.get()
            self.reset_button.Disable()
            self.replay_button.Disable()
            self.send_button.Disable()
            try:
                response = client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=sign,
                    temperature=1.1,
                    top_p=0.9,
                    max_tokens=4096 * 2,
                    stream=False
                )
                print(response.choices[0].message.content)
                # if response.choices[0].message.content.find("<think>") and response.choices[0].message.content.find(
                #         "</think>"):
                #     msg = response.choices[0].message.content.split("</think>\n")
                #     think = msg[0].split("<think>\n")[1]
                #     rep = msg[1]
                # el
                if len(response.choices[0].message.content) != 0:
                    get_rep = response.choices[0].message.content.split("\n")
                    think = "".join(get_rep[0:len(get_rep) - 1])
                    rep = re.sub(r"[\u0000-\uffff]*规则[\u0000-\uffff]*?。", "", get_rep[len(get_rep) - 1])
            except Exception as e:
                self.info_label.SetLabelText(self.default_text + f"运异丁真，鉴定为：珠脑过载\n{e}\n正在重新连接...")
                # t = self.reply_texts.pop()
                # self.box7.Detach(t)
                get_queue.put(sign)
                print(e)
                continue
            print(think)
            handle_queue.put((rep, think))
            time.sleep(1)

    def handle_renew(self, reply):
        # self.reply_texts.append(wx.StaticText(self.reply_panel, label=reply))
        self.reply_texts.append(MessageBlock(self.reply_panel, msg=reply,
                                             txtColor=wx.Colour(255, 255, 255),
                                             bgColor=wx.Colour(0, 0, 255)))
        print("blue:", len(self.reply_texts) - 1)
        # self.reply_texts[len(self.reply_texts) - 1].SetBackgroundColour("blue")
        # self.reply_texts[len(self.reply_texts) - 1].SetForegroundColour("white")
        self.box7.Add(self.reply_texts[len(self.reply_texts) - 1], flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        self.reply_panel.Fit()
        self.info_label.SetLabelText(self.default_text + "完成！")
        if not self.is_shutup:
            self.replay_button.Enable()
        self.reset_button.Enable()
        self.send_button.Enable()

    def do_handle_ds(self, handle_queue: queue.Queue, speak_queue: queue.Queue):
        global content
        while threading.main_thread().is_alive():
            rep, think = handle_queue.get()
            content = rep
            rep = push_enter(rep)
            wx.CallAfter(self.handle_renew, rep)
            rep1 = reply_text_handler(content)
            if not self.is_shutup:
                speak_queue.put(rep1)
            time.sleep(1)

    def do_speak_ds(self, speak_queue: queue.Queue):
        while threading.main_thread().is_alive():
            rep = speak_queue.get()
            try:
                if rep != "":
                    self.dz.synthesize_vocode(rep)
                    if self.is_anime:
                        self.dz.synthesize_video()
                if self.is_anime:
                    self.video_queue.put(cv2.VideoCapture("final.mp4"))
                self.dz.speak()
            except Exception as e:
                self.info_label.SetLabelText(self.default_text + f"运异丁真，鉴定为：没模擎亡源声的出声\n{e}")
            time.sleep(1)

    def before_get_renew(self, prompt):
        self.reply_texts.append(MessageBlock(self.reply_panel, msg=prompt,
                                             txtColor=wx.Colour(0, 0, 0),
                                             bgColor=wx.Colour(255, 255, 255)))
        print("white", len(self.reply_texts) - 1)
        self.box7.Add(self.reply_texts[len(self.reply_texts) - 1], flag=wx.ALIGN_RIGHT | wx.RIGHT, border=30)
        self.reply_panel.Fit()
        self.info_label.SetLabelText(self.default_text + "妈妈生的...")

    def get_reply(self):
        global content
        with open("init_prompt.txt", "r", encoding="utf-8") as f:
            init_prompt = f.read()
        prompt = self.send_text.GetValue()
        question = push_enter(prompt)
        wx.CallAfter(self.before_get_renew, question)
        if len(content) != 0:
            message.append({"role": "assistant", "content": content})
            content = ""
        else:
            message.append({"role": "system", "content": init_prompt})
        message.append({"role": "user", "content": prompt})
        self.get_queue.put(message)

    def replay_button_click(self, event):
        self.speak_queue.put("")

    def about_button_click(self, event):
        msg = '项目名称：电子丁真\
        \n作者：周故意太湖给他\
        \n简介：这是一款接入了DeepSeek-R1的API和MockingBird实时语音克隆模型的丁真风味聊天机器人。\
        \n特别鸣谢：babysor，他提供了TTS模型训练程序，其中我引用了MockingBird中的部分代码。'
        msg_box = wx.MessageDialog(None, msg, "注意事项")
        msg_box.ShowModal()

    def reset_button_click(self, event):
        self.reset()

    def reset(self):
        for text in self.reply_texts:
            text.Destroy()
        self.reply_texts.clear()
        global message, content
        message = []
        content = ""
        self.info_label.SetLabelText(f"{self.default_text}明白了，我已经抹去了过去，专注于现在。我们现在应该聊些什么？")

    def shutup_button_click(self, event):
        if not self.is_shutup:
            self.is_shutup = True
            self.replay_button.Disable()
            self.shutup_button.SetLabelText("纯纯出声")
        else:
            self.is_shutup = False
            self.replay_button.Enable()
            self.shutup_button.SetLabelText("雪豹闭嘴")

    def voice_button_click(self, event):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.info_label.SetLabelText(self.default_text + "请说话...")
                audio = r.listen(source)
                self.info_label.SetLabelText(self.default_text + "识别中...")
                text = eval(r.recognize_vosk(audio))["text"]
                text = re.sub(" ", "", text)
                self.send_text.SetValue(text)
                self.info_label.SetLabelText(self.default_text + "完成！")
        except Exception as e:
            self.info_label.SetLabelText(self.default_text + f"语噎丁真，鉴定为：出声啊，你\n{e}")


class EditPromptDialog(wx.Dialog):
    def __init__(self, parent: GUI):
        super().__init__(parent, title="编写提示词")
        panel = wx.Panel(self)
        self.edit_area = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(300, 200))
        with open("init_prompt.txt", "r", encoding="utf-8") as f:
            init_prompt = f.read()
        self.edit_area.SetLabelText(init_prompt)
        ok_button = wx.Button(panel, label="确定")
        cancel_button = wx.Button(panel, label="取消")
        ok_button.Bind(wx.EVT_BUTTON, self.ok_button_click)
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_button_click)
        box = wx.BoxSizer(wx.VERTICAL)
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.edit_area, 1, flag=wx.EXPAND | wx.ALL, border=5)
        box1.Add(ok_button, border=10)
        box1.Add(cancel_button, border=10)
        box.Add(box1, 0, flag=wx.BOTTOM | wx.ALIGN_CENTRE | wx.TOP, border=10)
        panel.SetSizer(box)
        self.parent = parent

    def ok_button_click(self, even):
        with open("init_prompt.txt", "w", encoding="utf-8") as f:
            f.write(self.edit_area.GetValue())
        self.parent.info_label.SetLabelText(self.parent.default_text + "提示词修改完成，重置聊天以载入新的设定。")
        self.Close()

    def cancel_button_click(self, even):
        self.Close()


def push_enter(text) -> str:
    content_list = [text[i] if (i + 1) % 20 != 0 else "\n" + text[i] for i in range(len(text))]
    return "".join(content_list)
