# 电子丁真（接入NewBing聊天模式和用MockingBird训练的丁真语音模型的聊天机器人）
## 准备工作
### python环境：
建议使用python 3.9版本，其他版本是否可行未经测试。注意勾选配置环境变量。
### 安装依赖：
在文件所在目录打开cmd或终端，输入`pip install -r requirements`(确保你的python安装时自带pip，否则请先安装pip)。如果这一步有错误，请根据pip的报错，缺什么就`pip install 什么`，需要什么版本就`pip install xx==哪个版本`。
### 准备魔法：
准备一个代理工具或VPN（推荐使用Clash）。在这一步你可能还需要配置你的Clash，见下。
导入Cookie：准备一个开通了newbing聊天模式的微软账号。在Edge浏览器或谷歌浏览器的扩展商店里面搜索Cookie-Editor安装之后打开它，点击Export，选择Export as JSON.然后回到项目目录，打开bingAI-cookies.json，粘贴获取的cookie.
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
4.经测试本程序可以解决部分由于微软监管**撤回**信息的问题。在此客户端，应该被**撤回**的消仍然会被保留（但微软有概率直接让Bing闭嘴，直接塞一句"My Mistakes..."（不是输出到一半撤回，而是直接弹个这个出来）这是极小概率事件，我测试也就只遇到过一次）。  
5.对于强制切断对话，这取决于咒语的解限水平（这个丁真咒语经过我的测试好像没被掐断过）。
## 设置魔法（Clash为例）
### 设置代理规则：
可以直接开全局模式（但这样访问国内网站不便），也可以自行配置：先确认服务商的配置文件中是否有bing.com的代理，右键单击配置文件，选择编辑，然后查看其中是否有`'DOMAIN-SUFFIX,bing.com,微软服务'`或类似字段，若没有请添加；然后在规则模式下，找到bing.com走的代理服务（如：微软服务），确保其不是DIRECT（直连）。若其为DIRECT，请选择一个节点，或者直接选“节点选择”。
### 配置TUN模式：
在主页点击“服务模式-管理”（Service Mode），安装服务管理，其有两个安装方法（schtasks和winsw）选一个安装，不行就安装另一个或者重复几次，直到绿色地球亮起，然后打开TUN模式。
## 常见错误
**声明：我只是一个刚高考完的学生，编程只是我的课外兴趣，一些问题我不能很好解决。** 可以在issue里讨论，如果有我知道解决方案的，我会来回答。更多的常见错误，参见[EgdeGPT issue](https://github.com/acheong08/EdgeGPT/issues)或[MockingBird issue](https://github.com/babysor/MockingBird/issues)  
1.Exception: Authentication failed:可能原因：cookie配置不正确，或者没有加入等候名单。解决方案：更新Cookie或按照准备工作正确配置Cookie，或用一个能访问新必应的微软账号。  
2.httpx.TooManyRedirects: Exceeded maximum allowed redirects:可能原因：代理规则配置有误，或者程序代码中的proxy代理不正确。解决方案：如果代理工具开启了系统代理，可在设置-网络和Internet-代理中查看代理服务器地址和端口，填入其中，如："http://xxx.x.x.x:port"。  
3.websockets.exceptions.InvalidStatusCode: server rejected WebSocket connection: HTTP 200:可能原因：代理工具未正确开启TUN模式。若排除了以上原因可以多刷新几次试试。  
4.asyncio.exceptions.TimeoutError:解决方案：在`python\Lib\site-packages\websockets\legacy\client.py`的442行和444行，右键编辑，改：`open_timeout: Optional[float] = 30,#10`和`ping_timeout: Optional[float] = 30,#20`即可（我是这么解决的）
