# Remiball

蕾米球QQbot

基于Onebot协议编写 

底层暂时使用OICQ，外接python的nonebot2机器人管理

## 如何运行

①安装好OICQ并登陆账号

②安装好nonebot2的依赖，并在该目录下执行nb run

注意nonebot2的反向ws监听地址要与OICQ的上报地址一致

### 文件介绍

.env.dev

里面是bot的各种设置，其中超级用户的设置由于代码原因不在这里

bot.py

主程序，不建议动，主要是加载插件啥的，加载方式为加载下面的plugins.json文件

plugins.json

里面为要加载的插件，因为nonebot2的奇妙加载机制，我只能把插件一个个写在这里并保持其目录的相对路径

awesome_bot/plugins/

里面为各种我写的插件