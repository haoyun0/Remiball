from .._gb import *

remind = on_command("坑", rule=Check_('坑'), priority=5)
remind0 = on_command("留言", rule=Check_('留言'), priority=10)
remind1 = on_command("挖坑", rule=Check_('挖坑'), permission=SUPERUSER, priority=3)
remind2 = on_command("填坑", rule=Check_('填坑'), permission=SUPERUSER, aliases={"弃坑"}, priority=3)

datax = DataList('remind')
data = datax.data

cmds = [
'坑',
'挖坑',
'填坑',
'留言'
]
con.addcmds("基础功能", cmds)
con.addcmds("坑", cmds)


async def add(work: str):
    global data
    data['tot'] += 1
    data['a'].append(work)
    data['time'].append(time.strftime("%Y-%m-%d", time.localtime()))
    await datax.output()


async def delete(id: int):
    data['tot'] -= 1
    del data['a'][id]
    del data['time'][id]
    await datax.output()


@remind.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if str(event.message).strip():
        await remind.finish()
    if not con.check(event, '坑'):
        await remind.finish()
    if data['tot'] == 0:
        await con.send(bot, event, "目前没有任何坑")
        await remind.finish()
    mystr = "目前的坑有："
    for i in range(data['tot']):
        mystr = mystr + '\n%d : %s , 挖坑时间:%s' % (i, data['a'][i], data['time'][i])
    await con.send(bot, event, mystr)
    await remind.finish()

@remind0.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    await bot.send_private_msg(user_id = 847360401, message =  str(event.get_message()).strip())
    await remind0.finish()

@remind1.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if not con.check(event, '挖坑'):
        await remind1.finish()
    args = str(event.get_message()).strip()
    await add(args)
    await con.send(bot, event, "挖坑: %s 成功" % args)
    await remind1.finish()


@remind2.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if not con.check(event, '填坑'):
        await remind2.finish()
    comd = event.raw_message.replace(str(event.get_message()), "")
    comd = comd[1:]
    args = str(event.get_message()).strip()
    mystr = data['a'][int(args)]
    await delete(int(args))
    await con.send(bot, event, "%s: %s 成功" % (comd, mystr))
    await remind2.finish()
