import re

from openai import OpenAI
from main.voice import DingZhen
dz = DingZhen()
with open("DeepSeek_API.txt", "r", encoding="utf-8") as file:
    api_key = file.read()
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
    # api_key="sk-9c7d229fc5474c5a9332063387569e64", base_url="https://api.deepseek.com"
)
map = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九",
       "-": "负", "⁓": "~"}
with open("init_prompt.txt", "r", encoding="utf-8") as f:
    init_prompt = f.read()
message = [
    {"role": "system", "content": init_prompt}]
content = ""
f = False
while True:
    question = ''
    if not f:
        question = input()
        message.append({"role": "assistant", "content": content})
        message.append({"role": "user", "content": question})
    if question == "-1":
        break
    completion = None
    rep = ""
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            # model="deepseek-reasoner",
            messages=message,
            temperature=1.1,
            top_p=0.9,
            max_tokens=4096 * 2,
            stream=False
        )
        if completion.choices[0].message.content.find("<think>") and completion.choices[0].message.content.find(
                "</think>"):
            msg = completion.choices[0].message.content.split("</think>\n")
            think = msg[0].split("<think>\n")[1]
            rep = msg[1]
        elif len(completion.choices[0].message.content) != 0:
            get_rep = completion.choices[0].message.content.split("\n")
            think = "".join(get_rep[0:len(get_rep) - 1])
            rep = re.sub(r"[\u0000-\uffff]*规则[\u0000-\uffff]*?。", "", get_rep[len(get_rep) - 1])
    except Exception as e:
        print("连接中断，正在尝试重连...")
        f = True
        continue
    f = False
    content = rep
    print(rep)
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
    dz.synthesize_vocode(rep)
    dz.speak()

