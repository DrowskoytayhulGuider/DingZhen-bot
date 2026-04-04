# 电子丁真（接入DeepSeek-V3.2和用MockingBird训练的丁真语音模型的聊天机器人，原使用NewBing聊天模式）
<img width="916" height="938" alt="image" src="https://github.com/user-attachments/assets/79443757-74d7-42d3-9434-001b4b9043f8" />

还是没有当年用NewBing那味啊，当年随便一聊都很抽象😭
## 准备工作
### python环境：
建议使用python 3.10版本，其他版本是否可行未经测试。注意勾选配置环境变量。
### 安装依赖：
在文件所在目录打开cmd或终端，输入`pip install -r requirements`(确保你的python安装时自带pip，否则请先安装pip)。如果这一步有错误，请根据pip的报错，缺什么就`pip install 什么`，需要什么版本就`pip install xx==哪个版本`。
下载对应的语音模型文件（合成器(synthesizer)、编码器(encoder)、声码器(vocoder)，通过网盘分享的文件：models
链接: https://pan.baidu.com/s/1WlaBbpAFPRX3n3G5LjuzGw?pwd=aays 提取码: aays）
### 开始聊天：
自己到DeepSeek官网去申请API，将生成的API-key复制到根目录的DeepSeek-API.txt中（没有就新建），打开DingZhen.py或DingZhen_cmd.py即可开始聊天。
## 使用方法
### GUI用户
进入程序以后。丁真的回复可能会比较慢，请耐心等待。若对话结束想开始新对话，请点击“重置”。如果你不想让丁真说话，因为这样会使本来就长的等待时间变得更长，你可以点击“雪豹闭嘴”，你又想打开的话就点击“纯纯出声”；如果你不想看到丁真说话的视频（因为这也会很慢很慢，而且效果不佳），请点击“关闭对话”。语音识别使用vosk的小型中文语音识别模型，识别准确度有限。想要更好的免费语音识别服务可使用谷歌（需要科学上网）。
### 命令行用户
进入程序之后，请耐心等待加载完成后（1min左右），就可聊天。但回复仍然较慢。输入`!exit`即可退出。
## 电子xx
玩够了电子丁真？试试把它设置成别的人物，比如“赛博蔡徐坤”“电子孙笑川”“AI猫娘”或者复活“Sydeny”😭。
### 第一步：
编辑人物设定，在对话界面中点击“编辑提示文本”，让AI扮演你想要的角色。
### 第二步：
导入或者训练语音模型：可以在网上找.pt的TTS语音模型（Github上MockingBird项目中有一些）导入`synthesizer\saved_models`中或者自己用语料和MockingBird训练TTS模型，然后在对话界面中点击选择语音模型，选择对应的模型即可。详见：[MockingBird](https://github.com/babysor/MockingBird/blob/main/README-CN.md).
### 第三步（可选）：
进main中的代码，修改与丁真有关的字符串。
