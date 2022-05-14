from .._gb import *
import os

open_cmd = on_command("启用", aliases={"开启"}, permission=OWNER, priority=3)
open_cmd2 = on_command("启用组", aliases={"开启组"}, permission=ADMIN, priority=3)
ban = on_command("禁用", aliases={"关闭"}, permission=OWNER, priority=3)
ban2 = on_command("禁用组", aliases={"关闭组"}, permission=ADMIN, priority=3)
allcmd = on_command("命令列表", aliases={"指令列表"}, permission=ADMIN, priority=3)
allcmds = on_command("所有命令列表", aliases={"所有指令列表"}, permission=SUPERUSER, priority=3)
cmdcheck = on_command("命令检测", aliases={"指令检测"}, permission=SUPERUSER, priority=3)
all_help = on_command("帮助", aliases={"help"}, priority=6)



help_list= con.help_list

datax = con.datax
data = datax.data

work_id = 0




@open_cmd.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args in con.command_list:
        gid = get_gid(event)
        if not gid in data:
            data[gid] = []
        if args in data[gid]:
            await con.send(bot, event, "该命令已经启用")
        else:
            await add(gid, args)
            await con.send(bot, event, "启用成功")
    else:
        await con.send(bot, event, "不存在该指令")
    await open_cmd.finish()

@open_cmd2.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args == 'all':
        gid = get_gid(event)
        if not gid in data:
            data[gid] = []
        for arg in con.command_lists:
            for i in con.command_lists[arg]:
                if not i in data[gid]:
                    await add(gid, i)
        await con.send(bot, event, '全部指令启用成功')
        await open_cmd2.finish()
    if args in con.command_lists:
        gid = get_gid(event)
        if not gid in data:
            data[gid] = []
        for i in con.command_lists[args]:
            if not i in data[gid]:
                await add(gid, i)
        await con.send(bot, event, '全部启用成功')
    else:
        await con.send(bot, event, "不存在该指令组")
    await open_cmd2.finish()

@ban.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args in con.command_list:
        gid = get_gid(event)
        if gid in data:
            if args in data[gid]:
                await delete(gid, args)
                await con.send(bot, event, "禁用成功")
            else:
                await con.send(bot, event, "该命令未启用")
        else:
            await con.send(bot, event, "该群聊未启用任何指令")
    else:
        await con.send(bot, event, "不存在该指令")
    await ban.finish()

@ban2.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args == 'all':
        gid = get_gid(event)
        for arg in con.command_lists:
            for i in con.command_lists[arg]:
                if i in data[gid]:
                    await delete(gid, i)
        await con.send(bot, event, '全部指令禁用成功')
        await ban2.finish()
    if args in con.command_lists:
        gid = get_gid(event)
        if gid in data:
            for i in con.command_lists[args]:
                if i in data[gid]:
                    await delete(gid, i)
            await con.send(bot, event, "全部禁用成功")
        else:
            await con.send(bot, event, "该群聊未启用任何指令")
    else:
        await con.send(bot, event, "不存在该指令组")
    await ban2.finish()

@allcmd.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    gid = get_gid(event)
    if gid in data:
        mystr = "本群聊启用的所有指令如下："
        for i in data[gid]:
            mystr = mystr + '\n' + i
        await con.send(bot, event, mystr)
    else:
        await con.send(bot, event, "该群聊未启用任何指令")
    await allcmd.finish()

@allcmds.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    flag = False
    mystr = "该机器人目前可用指令如下："
    for i in con.command_list:
        mystr = mystr + '\n' + i
        flag = True
    if flag:
        await con.send(bot, event, mystr)
    else:
        await con.send(bot, event, "该机器人未启用任何指令")
    await allcmds.finish()

@cmdcheck.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    tot = 0
    for j in data:
        err = []
        for i in data[j]:
            if not i in con.command_list:
                tot += 1
                err.append(i)
        for i in err:
            data[j].remove(i)
    if tot > 0:
        await datax.output()
    await con.send(bot, event, "共清除%d条无用指令" % tot)
    await cmdcheck.finish()

@all_help.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    mystr = '未找到相关模块的帮助'
    if args:
        for i in con.help_list:
            if i == args:
                mystr = con.help_list[i]['state']
                break
            elif 'ow' in con.help_list[i]:
                flag = False
                for j in con.help_list[i]['ow']:
                    if j == args:
                        flag = True
                        mystr = con.help_list[i]['state']
                        break
                if flag:
                    break
        await con.send(bot, event, mystr)
    else:
        await con.send(bot, event, """
蕾米球目前支持的模块有：

基础功能
好感度系统(货币系统)
模拟抽卡系统

输入 !帮助<模块> 来查询进一步帮助
部分查询到无法使用的功能可能是没有在本群开启（默认不开
群主和管理员都有开启和关闭功能的权限
<>不用输入
""".strip())
    await all_help.finish()

con.addhelp('基础功能', """
基础功能有：

roll	:掷骰子
早安晚安	:提供统计及禁言服务
扭蛋		:随机抽群友
随机图	:发送随机图片
帮你选择	:帮你选择
小游戏	:某些小游戏
蕾米语  	:参考某常用编码自创语言
点歌		:网易云点歌
留言		:给开发者留言
bilibili:b站相关
坑		:查看待填的坑

输入 !帮助 <命令> 来查询进一步帮助
<>不用输入
""".strip())

async def del_msg(bot: Bot, message_id):
    await bot.call_api("delete_msg", message_id=message_id)

def get_gid(event: Event):
    if event.message_type == 'group':
        return str(event.group_id)
    else:
        if event.sub_type == 'friend':
            return '19260817'  # 好友消息
        else:
            return '60481729'  # 群临时会话

def restart():
    path2 = os.path.abspath(os.path.dirname(__file__))
    dirr = os.path.join(path2, "test.txt")
    if os.path.exists(dirr):
        os.remove(dirr)
    else:
        with open(dirr, mode="w", encoding="utf-8") as f:
            f.write("test")


async def add(gid: str, func: str):
    if not gid in data:
        data[gid]=[]
    data[gid].append(func)
    await datax.output()

async def delete(gid: str, func: str):
    data[gid].remove(func)
    await datax.output()