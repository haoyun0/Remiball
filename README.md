# Remiball

蕾米球QQbot

基于Onebot协议编写 

底层暂时使用OICQ，外接python的nonebot2机器人管理

## 如何运行

①安装好OICQ并登陆账号

②安装好nonebot2的依赖，并在该目录下执行nb run

注意nonebot2的反向ws监听地址要与OICQ的上报地址一致



重点事项：

nonebot2的cqhttp的适配器adapters并不适配oicq

oicq上报事件中的message_id和font不和传统cqhttp一样为int

而是为str，会导致nonebot2无法handle_event

解决方法，把其event类的对应两个属性改为str类型

具体为找到:Python39\Lib\site-packages\nonebot\adapters\cqhttp里面的event.py文件

将class MessageEvent(Event):类

里面的message_id和font属性改为str

这样就能正常接受消息了

### 文件介绍

.env.dev

里面是bot的各种设置，其中超级用户的设置由于代码原因不在这里

bot.py

主程序，不建议动，主要是加载插件啥的，加载方式为加载下面的plugins.json文件

plugins.json

里面为要加载的插件，因为nonebot2的奇妙加载机制，我只能把插件一个个写在这里并保持其目录的相对路径

awesome_bot/plugins/

里面为各种我写的插件