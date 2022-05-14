from .._gb import *
from nonebot import on_message

datax = DataList('strange')
data = datax.data


strange_get = on_message(rule=Check_('', 'group'), priority=10)
strange_speak = on_command('说点怪话', rule=Check_('说点怪话', 'group'), priority=10)
strange_speak_x = on_command('说些怪话', rule=Check_('说些怪话', 'group'), priority=10)
strange_speak_auto = on_command('怪话插入', rule=Check_('怪话插入', 'group'), permission=ADMIN, priority=10)
strange_keyword = on_command('怪话屏蔽关键词', rule=Check_("怪话屏蔽关键词"), permission=SUPERUSER, priority=5)
strange_word = on_command('怪话屏蔽词', rule=Check_("怪话屏蔽词"), permission=SUPERUSER, priority=5)
strange_startwith = on_command('怪话屏蔽开头', rule=Check_("怪话屏蔽开头"), permission=SUPERUSER, priority=5)
strange_qq = on_command('怪话屏蔽qq', rule=Check_("怪话屏蔽qq"), permission=SUPERUSER, priority=5)
last = ""

cmds = [
    '说点怪话',
    '说些怪话',
    '怪话插入',
    '怪话屏蔽词',
    '怪话屏蔽关键词',
    '怪话屏蔽开头',
    '怪话屏蔽qq'
]

con.addcmds('基础功能', cmds)
con.addcmds('怪话', cmds)

frequency = {}
cool_down = {}

@strange_get.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global last, data, frequency, cool_down
    if event.group_id in data['group']:
        msg = str(event.get_message()).strip()
        if msg != last:
            if event.group_id in data['auto']:
                if msg[0] == '!' or msg[0] == '！' or msg[0] == '♂' or msg[0] == '♀':
                    await strange_get.finish()
                if not event.group_id in frequency:
                    frequency[event.group_id] = []
                frequency[event.group_id].append(time.time())
                while time.time() - frequency[event.group_id][0] > 300:
                    del frequency[event.group_id][0]
                if len(frequency[event.group_id]) > 50:
                    flag = False
                    if event.group_id  in cool_down:
                        if time.time() - cool_down[event.group_id] > 60:
                            flag = True
                    else:
                        flag = True
                    if flag:
                        x = random.randint(0, 999)
                        while data['message'][x] == '蕾米球index':
                            x = random.randint(0, 999)
                        await con.send(bot, event, data['message'][x])
                        cool_down[event.group_id] = time.time()

            if len(msg) > 14:
                if not (msg[:4] == '[CQ:' and msg[-1] == ']'):
                    await strange_get.finish()
            if event.user_id in data['ban_qq']:
                await strange_get.finish()
            for w in data['ban_word']:
                if msg == w:
                    await strange_get.finish()
            for w in data['ban_keyword']:
                if w in msg:
                    await strange_get.finish()
            for w in data['ban_startwith']:
                if w in msg:
                    ww = msg.index(w)
                    if ww == 0:
                        await strange_get.finish()
            last = msg
            x = random.randint(0, 999)
            data['message'][x] = msg
            await datax.output()
    await strange_get.finish()

@strange_speak.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    x = random.randint(0, 999)
    while data['message'][x] == '蕾米球index':
        x = random.randint(0, 999)
    await con.send(bot, event, data['message'][x])
    await strange_speak.finish()

@strange_speak_x.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    y = random.randint(3, 5)
    for _ in range(y):
        x = random.randint(0, 999)
        while data['message'][x] == '蕾米球index':
            x = random.randint(0, 999)
        await con.send(bot, event, data['message'][x])
        time.sleep(1)
    await strange_speak_x.finish()

@strange_speak_auto.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    if event.group_id in data['auto']:
        data['auto'].remove(event.group_id)
        await con.send(bot, event, "已关闭")
    else:
        data['auto'].append(event.group_id)
        await con.send(bot, event, "已开启")
    await datax.output()
    await strange_speak_auto.finish()

@strange_keyword.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    data['ban_keyword'].append(msg)
    await datax.output()
    await con.send(bot, event, "屏蔽成功")
    await strange_keyword.finish()
@strange_word.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    data['ban_word'].append(msg)
    await datax.output()
    await con.send(bot, event, "屏蔽成功")
    await strange_word.finish()
@strange_startwith.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    data['ban_startwith'].append(msg)
    await datax.output()
    await con.send(bot, event, "屏蔽成功")
    await strange_startwith.finish()
@strange_qq.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    data['ban_qq'].append(int(msg))
    await datax.output()
    await con.send(bot, event, "屏蔽成功")
    await strange_qq.finish()