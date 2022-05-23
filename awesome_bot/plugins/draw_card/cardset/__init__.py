from ..._gb import *

cardset_new = on_command("新建卡牌", rule=Check_('新建卡牌'), permission=SUPERUSER, priority=3)

cmds = [
    '新建卡牌'
]
con.addcmds('模拟抽卡系统', cmds)

datax = cardset.datax
data = datax.data
name_list = cardpool.data['level_name']
level_num = cardpool.data['level_num']

@cardset_new.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip().split()
    if len(msg) == 2:
        flag = True
        if not msg[0] in name_list:
            flag = False
        if flag and msg[1].isnumeric():
            idx = msg[1]
            if 0 <= int(idx) < level_num[name_list.index(msg[0])]:
                pass
            else:
                flag = False
        else:
            flag = False
        if flag:
            state['level'] = msg[0]
            state['id'] = msg[1]
        else:
            await con.send(bot, event, '格式错误，格式: 稀有度 id')
            await cardset_new.reject()
    else:
        await con.send(bot, event, '请输入卡牌的稀有度以及id')
        await cardset_new.reject()
    flag = False
    if msg[0] in data:
        if idx in data[msg[0]]:
            flag = True
    state['step'] = 1
    if flag:
        mylist = []
        for key in data[msg[0]][str(idx)]:
            if key != 'output':
                if data[msg[0]][str(idx)][key] is None:
                    mylist.append(key)
        await con.send(bot, event, "%s%s缺少条目: " % (msg[0], msg[1]) + str(mylist) + '\n\n请输入要更改的条目名')
    else:
        await cardset.new_card(msg[0], idx)
        await con.send(bot, event, '%s%s没有任何条目，新建卡牌\n\n请输入要更改的条目名' % (msg[0], msg[1]))

@cardset_new.receive()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if state['step'] == 1:
        if msg == '描述':
            state['op'] = 'desc'
        elif msg == '封面' or msg == '图像' or msg == '立绘' or msg == '卡面':
            state['op'] = 'cover'
        elif msg == '技能名称':
            state['op'] = 'skill_name'
        elif msg == '技能描述':
            state['op'] = 'skill_desc'
        elif msg == '技能上限' or msg == '技能限制':
            state['op'] = 'skill_limit'
        elif msg == '名称' or msg == '名字' or msg == '姓名' or msg == '称呼' or msg == '称谓':
            state['op'] = 'name'
        else:
            await con.send(bot, event, '没有条目: ' + msg)
            await cardset_new.reject()
        await con.send(bot, event, '请输入条目内容')
        state['step'] = 2
        await cardset_new.reject()
    elif state['step'] == 2:
        data[state['level']][state['id']][state['op']] = msg
        await datax.output()
        await con.send(bot, event, '条目%s成功更改为%s' % (state['op'], msg))
        await cardset_new.finish()