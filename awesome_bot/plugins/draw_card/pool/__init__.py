from ..._gb import *

fake_new = on_command('新建模拟池子', rule=Check_('新建模拟池子'), priority=10)
fake_single = on_command("模拟单抽", rule=Check_("模拟单抽"), priority=10)
fake_ten = on_command("模拟十连", rule=Check_("模拟十连"), priority=10)
fake_ask = on_command("查看模拟概率", rule=Check_("查看模拟概率"), priority=10)
fake_all = on_command("查看模拟池子", rule=Check_("查看模拟池子"), priority=10)
fake_del = on_command("删除模拟池子", rule=Check_("删除模拟池子"), priority=10)
office_single = on_command("抽卡单抽", rule=Check_("抽卡单抽"), priority=6)
office_single_ten = on_command("抽卡单抽十连", rule=Check_("抽卡单抽"), priority=6)
office_ten = on_command("抽卡十连", rule=Check_("抽卡十连"), priority=6)
office_ask = on_command("查看概率", rule=Check_("查看概率"), priority=6)
office_up = on_command("查看当前up", rule=Check_("查看当前up"), priority=6)
office_new = on_command("新增卡牌", rule=Check_("新增卡牌"), permission=SUPERUSER, priority=4)

scheduler = require('nonebot_plugin_apscheduler').scheduler

cmds = [
'新建模拟池子',
"模拟单抽",
"模拟十连",
"查看模拟概率",
"查看模拟池子",
"删除模拟池子",
'抽卡单抽',
'抽卡十连',
'抽卡单抽十连',
'查看当前up',
'查看概率',
'新增卡牌'
]

con.addcmds('模拟抽卡系统', cmds)
con.addcmds('抽卡系统抽卡', cmds)

con.addhelp('抽卡系统抽卡', """
抽卡系统自带蕾米球官方池子，也可以自己建自己玩的模拟池子
官方池子指令如下：
抽卡单抽\t\t:可选参数up
抽卡十连\t\t:可选参数up
抽卡单抽十连\t:可选参数up
查看当前up
查看概率
模拟池子指令如下：
新建模拟池子 [池子名字]
模拟单抽 [池子名字]
模拟十连 [池子名字]
查看模拟池子
查看模拟概率 [池子名字]
删除模拟池子 [池子名字]
""".strip())

datax = cardpool.datax
data = datax.data

# data['fake_pool'] = {}
# data['pool'] = [[], [], []]
# data['time'] = [time.time(), time.time(), time.time()]
# data['in_pool'] = {}
# data['level_pool'] = [[], [], [], [], []]
# data['up_st_id'] = [0, 0, 0, 0, 0]
# data['level_pool_up'] = [[], [], [], [], []]
# data['level_num'] = [10, 40, 100, 400, 1500]
# data['level_name'] = ['甲球', '乙球', '丙球', '丁球', '戊球']
# data['level_card'] = {'甲球': 5, '乙球': 20, '丙球': 50, '丁球': 200, '戊球': 725}
# data['level_up'] = [1, 2, 5, 10, 20]

@office_new.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip().split()
    if len(msg) == 2:
        flag = True
        if not msg[0] in data['level_name']:
            flag = False
        if flag and msg[1].isnumeric():
            if int(msg[1]) <= 0:
                flag = False
        else:
            flag = False
        if flag:
            state['level'] = msg[0]
            state['id'] = msg[1]
        else:
            await con.send(bot, event, '格式错误，格式: 稀有度 新增数量')
            await office_new.reject()
    else:
        await con.send(bot, event, '请输入卡牌的稀有度以及新增数量')
        await office_new.reject()
    level = data['level_name'].index(msg[0])
    data['level_num'][level] += int(msg[1])
    data['level_pool'] = [[], [], [], [], []]
    data['level_pool_up'] = [[], [], [], [], []]
    await con.send(bot, event, '已为%s添加%s张新卡\n池子重置成功' % (msg[0], msg[1]))
    await datax.output()
    await office_new.finish()


@office_single.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    msg = str(event.get_message()).strip()
    if msg != "" and msg != 'up':
        await con.send(bot, event, "不带参数为普通池子，带参数up为up池")
        await office_single.finish()
    if msg == 'up':
        up = True
    else:
        up = False
    m = await card.get(uid, 'single')
    if m < 1:
        await con.send(bot, event, "单抽券不足")
        await office_single.finish()
    await card.modify(uid, 'single', -1)
    idx = select_pool(uid)
    await office_other_draw(idx, up)
    level, ans = await office_getone(idx, up)
    upstar = await card.new_card(uid, data['level_name'][level], ans)
    x = random.randint(0, 5)
    for _ in range(x):
        await office_getone(idx, up)
    await datax.output()
    mystr = '\n你抽到了: %s[id=%d]' % (data['level_name'][level], ans)
    if upstar > 0:
        if upstar == 1:
            mystr += '\nNew!!!'
        else:
            mystr += '\n升星!!!升至%d星' % upstar
    await con.send(bot, event, mystr, at_sender=True)
    await office_single.finish()

@office_single_ten.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    msg = str(event.get_message()).strip()
    if msg != "" and msg != 'up':
        await con.send(bot, event, "不带参数为普通池子，带参数up为up池")
        await office_single_ten.finish()
    if msg == 'up':
        up = True
    else:
        up = False
    m = await card.get(uid, 'single')
    if m < 10:
        await con.send(bot, event, "单抽券不足")
        await office_single_ten.finish()
    await card.modify(uid, 'single', -10)
    idx = select_pool(uid)
    await office_other_draw(idx, up)
    mystr = '@%d\n你抽到了:' % event.user_id
    light = 5
    for _ in range(10):
        level, ans = await office_getone(idx, up)
        if level < light:
            light = level
        mystr += '\n%s[id=%d]' % (data['level_name'][level], ans)
        upstar = await card.new_card(uid, data['level_name'][level], ans)
        if upstar > 0:
            if upstar == 1:
                mystr += '\tNew!!!'
            else:
                mystr += '\t升星!!!升至%d星' % upstar
        x = random.randint(0, 2)
        for _ in range(x):
            await office_getone(idx, up)
    await datax.output()
    if light == 0:
        await con.send(bot, event, '\n金光', at_sender=True)
    elif light == 1:
        await con.send(bot, event, '\n紫光', at_sender=True)
    elif light == 2:
        await con.send(bot, event, '\n蓝光', at_sender=True)
    else:
        await con.send(bot, event, '\n白光', at_sender=True)
    await con.sendNode(bot, event, [mystr])
    await office_single_ten.finish()

@office_ten.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    msg = str(event.get_message()).strip()
    if msg != "" and msg != 'up':
        await con.send(bot, event, "不带参数为普通池子，带参数up为up池")
        await office_ten.finish()
    if msg == 'up':
        up = True
    else:
        up = False
    m = await card.get(uid, 'ten')
    if m < 1:
        await con.send(bot, event, "十连券不足")
        await office_ten.finish()
    await card.modify(uid, 'ten', -1)
    idx = select_pool(uid)
    await office_other_draw(idx, up)
    mystr = '@%d\n你抽到了:' % event.user_id
    light = 5
    for _ in range(10):
        level, ans = await office_getone(idx, up)
        if level < light:
            light = level
        mystr += '\n%s[id=%d]' % (data['level_name'][level], ans)
        upstar = await card.new_card(uid, data['level_name'][level], ans)
        if upstar > 0:
            if upstar == 1:
                mystr += '\tNew!!!'
            else:
                mystr += '\t升星!!!升至%d星' % upstar
    x = random.randint(0, 5)
    for _ in range(x):
        await office_getone(idx, up)
    await datax.output()
    if light == 0:
        await con.send(bot, event, '\n金光', at_sender=True)
    elif light == 1:
        await con.send(bot, event, '\n紫光', at_sender=True)
    elif light == 2:
        await con.send(bot, event, '\n蓝光', at_sender=True)
    else:
        await con.send(bot, event, '\n白光', at_sender=True)
    await con.sendNode(bot, event, [mystr])
    await office_ten.finish()

def select_pool(uid):
    return 1

@office_up.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    mystr = '今天各稀有度up的ID为:'
    for i in range(len(data['level_name'])):
        mystr += '\n' + data['level_name'][i] + ", ID:%d~%d" % (data['up_st_id'][i], data['up_st_id'][i] + data['level_up'][i] - 1)
    await con.send(bot, event, mystr)
    await office_up.finish()

@office_ask.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    mystr = '官方池概率如下，无保底'
    for i in range(len(data['level_name'])):
        mystr += '\n' + data['level_name'][i] + ", 概率: %.1f%%" % (data['level_card'][data['level_name'][i]] / 10)
    mystr += '\n\nup池中，每期up卡占其稀有度1/5，各稀有度出率不变'
    mystr += '\n甲球有很牛逼的技能'
    await con.send(bot, event, mystr)
    await office_ask.finish()

async def office_other_draw(idx, up):
    now = time.time()
    while data['time'][idx] < now:
        data['time'][idx] += random.randint(30, 60)
        await office_getone(idx, up)

async def office_getone(idx, up):
    if up:
        pool = 'level_pool_up'
    else:
        pool = 'level_pool'
    if len(data['pool'][idx]) == 0:
        cp = []
        for org_id_ in range(1000):
            cp.append(org_id_)
        data['pool'][idx] = [0] * 1000
        for i in range(len(data['level_name'])):
            for _ in range(data['level_card'][data['level_name'][i]]):
                x = random.choice(cp)
                cp.remove(x)
                data['pool'][idx][x] = i
    level = data['pool'][idx][0]
    del data['pool'][idx][0]
    if len(data[pool][level]) == 0:
        cp = []
        for org_id_ in range(data['level_num'][level] * 3):
            cp.append(org_id_)
        data[pool][level] = [0] * (data['level_num'][level] * 3)
        for nid in range(data['level_num'][level]):
            if up:
                y = 2
                if data['up_st_id'][level] <= nid < data['up_st_id'][level] + data['level_up'][level]:
                    y += data['level_num'][level] // data['level_up'][level]
            else:
                y = 3
            for _ in range(y):
                x = random.choice(cp)
                cp.remove(x)
                data[pool][level][x] = nid
    ans = data[pool][level][0]
    del data[pool][level][0]
    return level, ans


@fake_new.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    name = str(event.get_message()).strip()
    if len(name) == 0:
        await con.send(bot, event, '请输入卡池名字')
        await fake_new.finish()
    if name in data['fake_pool']:
        await con.send(bot, event, "卡池已存在，若要更改请删除之前卡池")
        await fake_new.finish()
    state['name'] = name
    state['card'] = {}
    state['last'] = ""
    state['p'] = 0
    await con.send(bot, event, '请输入各卡稀有度名字以及概率（实数制），各品质概率为独立计算，每次输入一条，概率和为1自动结束，若要提前结束输入[结束],多余概率补充到最后一个输入的品质中\n例1：SSR 0.09\n例2: UP(SSR) 0.01\n注意若同时输入例1例2概率分别计算，也就是SSR概率为0.1')

@fake_new.receive()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if msg == '结束':
        name = state['last']
        if len(name) == 0:
            await con.send(bot, event, "不能一种卡都没有啊")
            await fake_new.reject()
        state['card'][name] += int(1000 * (1 - state['p']))
        await con.send(bot, event, '品质:%s概率自动修改为:%.1f%%\n新建卡池%s成功' % (name, state['card'][name] / 10, state['name']))
    else:
        msg = msg.split()
        if len(msg) != 2:
            await con.send(bot, event, '格式错误')
            await fake_new.reject()
        name = msg[0]
        if len(name) == 0:
            await con.send(bot, event, '格式错误')
            await fake_new.reject()
        p = float(msg[1])
        if p <= 0 or p + state['p'] > 1:
            await con.send(bot, event, '概率错误')
            await fake_new.reject()
        if int(p * 1000) / 1000 != p:
            await con.send(bot, event, '概率最多精确到千分之一')
            await fake_new.reject()
        state['last'] = name
        state['p'] += p
        state['card'][name] = int(p * 1000)
        if state['p'] == 1:
            await con.send(bot, event, '已新建品质:%s, 概率:%.1f%%\n新建卡池[%s]成功' % (name, p * 100, state['name']))
        else:
            await con.send(bot, event, '已新建品质:%s, 概率:%.1f%%' % (name, p * 100))
            await fake_new.reject()
    srt = []
    for pn in state['card']:
        srt.append((state['card'][pn], pn))
    srt.sort()
    id_list = []
    for a in srt:
        id_list.append(a[1])
    data['fake_pool'][state['name']] = {
        'p' : state['card'],
        'pool' : [],
        'id' : id_list,
        'time' : time.time()
    }
    await datax.output()
    await fake_new.finish()

@fake_all.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    mystr = '目前自建模拟池如下:'
    for name in data['fake_pool']:
        mystr += '\n' + name
    await con.send(bot, event, mystr)
    await fake_all.finish()

@fake_ask.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    name = str(event.get_message()).strip()
    if not name in data['fake_pool']:
        await con.send(bot, event, '池子不存在')
        await fake_ask.finish()
    mystr = '池子[%s]概率公示如下:' % name
    for pn in data['fake_pool'][name]['id']:
        mystr += '\n' + pn + ' : %.1f%%' % (data['fake_pool'][name]['p'][pn] / 10)
    await con.send(bot, event, mystr)
    await fake_ask.finish()

@fake_del.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    name = str(event.get_message()).strip()
    if not name in data['fake_pool']:
        await con.send(bot, event, '池子不存在')
        await fake_ask.finish()
    state['name'] = name
    await con.send(bot, event, '即将删除池子[%s]，y/n?' % name)

@fake_del.receive()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if msg == 'y':
        del data['fake_pool'][state['name']]
        await datax.output()
        await con.send(bot, event, '池子[%s]已删除' % state['name'])
    elif msg == 'n':
        await con.send(bot, event, '取消删除')
    else:
        await fake_del.reject()
    await fake_del.finish()

@fake_single.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    name = str(event.get_message()).strip()
    if not name in data['fake_pool']:
        await con.send(bot, event, '池子不存在')
        await fake_single.finish()
    data['fake_pool'][name]['time'] = await fake_other_draw(name, data['fake_pool'][name]['time'])
    ans = await fake_getone(name)
    x = random.randint(0, 5)
    for _ in range(x):
        await fake_getone(name)
    await datax.output()
    await con.send(bot, event, '\n你抽到了: ' + ans, at_sender=True)
    await fake_single.finish()

@fake_ten.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    name = str(event.get_message()).strip()
    if not name in data['fake_pool']:
        await con.send(bot, event, '池子不存在')
        await fake_ten.finish()
    data['fake_pool'][name]['time'] = await fake_other_draw(name, data['fake_pool'][name]['time'])
    mystr = '\n你抽到了:'
    for _ in range(10):
        mystr += '\n' + await fake_getone(name)
    x = random.randint(0, 5)
    for _ in range(x):
        await fake_getone(name)
    await datax.output()
    await con.send(bot, event, mystr, at_sender=True)
    await fake_ten.finish()

async def fake_other_draw(name, tim):
    now = time.time()
    while tim < now:
        tim += random.randint(30, 60)
        await fake_getone(name)
    return tim

async def fake_getone(name):
    if len(data['fake_pool'][name]['pool']) == 0:
        cp = []
        for org_id_ in range(1000):
            cp.append(org_id_)
        data['fake_pool'][name]['pool'] = [0] * 1000
        for i in range(len(data['fake_pool'][name]['id'])):
            for _ in range(data['fake_pool'][name]['p'][data['fake_pool'][name]['id'][i]]):
                x = random.choice(cp)
                cp.remove(x)
                data['fake_pool'][name]['pool'][x] = i
    ans = data['fake_pool'][name]['id'][data['fake_pool'][name]['pool'][0]]
    del data['fake_pool'][name]['pool'][0]
    return ans

@scheduler.scheduled_job("cron" , hour=0, minute=0)
async def ceg():
    data['level_pool_up'] = [[], [], [], [], []]
    for i in range(len(data['level_name'])):
        data['up_st_id'][i] += data['level_up'][i]
        if data['up_st_id'][i] >= data['level_num'][i]:
            data['up_st_id'][i] = 0
    await datax.output()