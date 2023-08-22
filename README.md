# 电子丁真（接入NewBing聊天模式和用MockingBird训练的丁真语音模型的聊天机器人）
**整活有风险，封号需谨慎**  
如遇无法正常访问新必应的情况，请尝试**更换节点**或者**注册新号**。推荐用**小号**体验。  
效果图：  
![Snipaste_2023-07-21_12-03-09](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/88df24de-3b0f-4a1b-944d-a8dabfcde698)  
真的可以防止撤回(Preserved the message from being deleted)：
![Snipaste_2023-07-21_12-05-18](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/32780c4a-dd60-46c1-b824-016194dda159)
## 准备工作
### python环境：
建议使用python 3.9版本，其他版本是否可行未经测试。注意勾选配置环境变量。
![Snipaste_2023-07-22_19-53-21](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/5eb51501-9c34-4edc-8822-f0e59081da9d)
![Snipaste_2023-07-22_19-54-22](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/cdf686ab-d507-4abb-8d0a-63481436ae11)
### 安装依赖：
在文件所在目录打开cmd或终端，输入`pip install -r requirements`(确保你的python安装时自带pip，否则请先安装pip)。报错说版本冲突的话大体可以不管。
![Snipaste_2023-07-22_20-07-55](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/a82e114b-64d7-428e-971d-ec2bb261cbcf)
### 导入TTS模型：
下载地址[百度网盘](https://pan.baidu.com/s/1YOeEZ3IHTyP7cXWKuVf28A?pwd=DZZZ)，提取码：DZZZ。文件大小500MB，没有特殊手段或氪金的话一个小时左右下完。下载完成之后，请将其剪切粘贴到项目文件目录下的`synthesizer/saved_models`目录下。以后也许我会训练更多的模型放在这里以供下载。
![Snipaste_2023-07-22_20-17-05](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/4b440f3f-aac8-44d0-8309-9f92ea7f2e02)
### 准备魔法：
准备一个代理工具或VPN（推荐使用[Clash](https://github.com/Fndroid/clash_for_windows_pkg/releases)，找个机场购买或使用免费服务）。在这一步你可能还需要配置你的Clash，见下。
### 导入Cookie：
准备一个开通了newbing聊天模式的微软账号。登录到你的newbing聊天模式，在Edge浏览器或谷歌浏览器的扩展商店里面搜索Cookie-Editor安装之后在聊天页面下打开它，点击Export，选择Export as JSON.然后回到项目目录，打开bingAI-cookies.json，粘贴获取的cookie.
![Snipaste_2023-07-22_20-19-18](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/2f77a25f-f726-4382-8e87-f2d04c041946)
![Snipaste_2023-07-22_20-19-45](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/388f0f98-131b-40f9-a9c5-1ab23b00355d)
![Snipaste_2023-07-22_20-25-10](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/b2c6af14-cbdc-44b5-91e6-bf0e7018c9be)
![Snipaste_2023-07-22_20-26-56](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/a0373c92-ad1e-4851-81c8-c8eee55efd67)
![Snipaste_2023-07-22_20-30-04](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/440fc641-9098-400d-9332-42917cf982fd)
### 开始聊天：
打开DingZhen.py或DingZhen_cmd.py即可开始聊天。
## 使用方法
### GUI用户
进入程序以后，请先点击“加载丁真嘴巴”和“加载丁真大脑”，待加载均完成之后（其中加载“大脑”时间可能较长，一分钟左右，请耐心等待），然后点击**注意事项**，仔细阅读**注意事项**后便可开始聊天。丁真的回复可能会比较慢（但比前一步快得多。NewBing是什么德性我就不多说了吧），请耐心等待。若对话结束想开始新对话，请点击“重置”，然后点击“加载丁真大脑”。如果你不想让丁真发出声音，因为这样会使本来就长的等待时间变得更长，你可以点击“雪豹闭嘴”，你又想打开的话就点击“纯纯出声”。语音识别使用的谷歌语音识别，这个是开放的，无需注册准备API_Key，可直接使用，但识别速度超慢，不推荐使用。
### 命令行用户
进入程序之后，请耐心等待加载完成后（1min左右），就可聊天。但回复仍然较慢（NewBing回复本来就慢）。输入`!exit`即可退出。
## 电子xx
玩够了电子丁真？试试把它设置成别的人物，比如“赛博蔡徐坤”“电子孙笑川”“AI猫娘”“Sydeny”甚至Bing本身，抑或是你自己身边的人。
### 第一步：
编辑人物设定（就是NewBing吧里常见的咒语），可以用ROT13编码编辑（推荐）。可以自己在贴吧或其他地方找或者自己编写：找一个ROT13编码转换网站，用`init_prompt.text`中的模板咒语，在其中解码后修改，再编码为ROT13即可。别忘了粘贴回`init_prompt.text`覆盖掉原来的咒语。
### 第二步：
导入或者训练语音模型：可以在网上找.pt的TTS语音模型（Github上MockingBird项目中有一些）导入`synthesizer\saved_models`中或者自己用语料和MockingBird训练TTS模型。详见：[MockingBird](https://github.com/babysor/MockingBird/blob/main/README-CN.md).
### 第三步（可选）：
进main中的代码，修改与丁真有关的字符串。
## 注意事项
1.千万不要尝试让丁真生成图片（本程序没有接入生成图片的接口），或说与图片生成有关的提示语，比如“看看...”“展示...”“...是什么样的”，可能的后果包括但不限于：无限的真人验证、询问后不再有回复。  
2.当加载Bing时出现CAPTCHA有关的错误时，请在[新必应聊天模式](https://www.bing.com/chat)中登录你的账号，然后随便问一个问题，在弹出来的人机验证中完成验证。  
3.由于新必应有每轮聊天三十句限制，所以这个程序也有此限制。  
4.经测试本程序可以解决部分由于微软监管**撤回**信息的问题。在此客户端，应该被**撤回**的消息仍然会被保留。但保留撤回的次数过多之后，微软可能会让bing不撤回直接弹出`Hmm...let's try a differnet topic. Sorry about that. What else is on your mind?`，此种情况暂无法解决（疑似微软最近加强限制）。  
5.对于强制切断对话，这取决于咒语的解限水平和微软的限制（最近疑似增强）。
## 设置魔法（Clash为例）
### 设置代理模式：
可以直接开全局模式（但这样访问国内网站不便），也可以自行配置：先确认服务商的配置文件中是否有bing.com的代理，右键单击配置文件，选择编辑，然后查看其中是否有`'DOMAIN-SUFFIX,bing.com,微软服务'`或类似字段，若没有请添加（一般都有，这步可跳过）；然后在规则模式下，找到bing.com走的代理服务（如：微软服务），确保其不是DIRECT（直连）。若其为DIRECT，请选择一个节点，或者直接选“节点选择”。  
推荐直接开全局，用完就关了还是很方便：
![Snipaste_2023-07-22_20-32-58](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/31cec25a-7a5b-4729-b1a6-023d2ef09055)  
若你非要开规则：
![Snipaste_2023-07-22_20-38-12](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/bb5ce2d5-b5e7-452d-ac98-955d9888a9a1)
### 配置TUN模式：
在主页点击“服务模式-管理”（Service Mode），安装服务管理，其有两个安装方法（schtasks和winsw）选一个安装，不行就安装另一个或者重复几次，直到绿色地球亮起，然后打开TUN模式。
![Snipaste_2023-07-22_20-38-38](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/bc86c597-7dfe-479f-88d4-e792a22b2227)
![Snipaste_2023-07-22_20-39-48](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/97959211-2d10-4e76-925e-fd2d40ccc492)
![Snipaste_2023-07-22_20-40-56](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/022c103e-00de-4278-bf4e-cb17a375df99)
## 常见错误
**声明：我只是一个刚高考完的学生，编程只是我的课外兴趣，一些问题我不能很好解决。** 可以在issue里讨论，如果有我知道解决方案的，我会来回答。更多的常见错误，参见[EgdeGPT issue](https://github.com/acheong08/EdgeGPT/issues)或[MockingBird issue](https://github.com/babysor/MockingBird/issues)  
* CaptchaChallenge: User needs to solve CAPTCHA to continue.可能原因：没有通过真人验证。解决方案：账号登录NewBing后，随便发一句话，在弹出来的验证窗口中完成验证。
![Snipaste_2023-07-24_20-02-45](https://github.com/DrowskoytayhulGuider/DingZhen-bot/assets/77562801/e1c263e6-9cd9-42d2-8506-af5b92a34a18)
* Exception: Authentication failed:可能原因：cookie配置不正确，或者没有加入等候名单。解决方案：更新Cookie或按照准备工作正确配置Cookie，或用一个能访问新必应的微软账号。
* httpx.TooManyRedirects: Exceeded maximum allowed redirects:可能原因：代理规则配置有误，或者程序代码中的proxy代理不正确。解决方案：如果代理工具开启了系统代理，可在设置-网络和Internet-代理中查看代理服务器地址和端口，填入其中，如："http://xxx.x.x.x:port"。
* websockets.exceptions.InvalidStatusCode: server rejected WebSocket connection: HTTP 200:可能原因：代理工具未正确开启TUN模式。若排除了以上原因可以多刷新几次试试。
* asyncio.exceptions.TimeoutError:解决方案：在`python\Lib\site-packages\websockets\legacy\client.py`的442行和444行，右键编辑，改：`open_timeout: Optional[float] = 30,#10`和`ping_timeout: Optional[float] = 30,#20`即可（我是这么解决的）
* 若遇见“Info:运异丁真，鉴定为：珠脑过载”，别担心，这个问题很简单，反复点击“发送”重试即可。
