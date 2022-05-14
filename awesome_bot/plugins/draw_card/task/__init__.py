from ..._gb import *

task_ask = on_command('查看任务', aliases={'查看任务信息'}, rule=Check_('查看任务') ,priority=5)
task_submit = on_command('提交任务', rule=Check_('提交任务') ,priority=5)
cmds = [
'查看任务',
'提交任务'
]

con.addcmds('模拟抽卡系统', cmds)
con.addcmds('抽卡系统任务', cmds)

con.addhelp('抽卡系统任务', """
在这里有各种任务，完成后可以获得抽卡券
任务每天刷新
指令:
查看任务 :查看今天的任务
提交任务 x :提交任务序号为x的任务
""".strip())

datax = DataList('draw_task')
data = datax.data

task_list = ['猜数字', '球球机', '21点']
plugin_name = {
    '猜数字': 'guess_number',
    '球球机': 'tiger',
    '21点': 'g21'
}

@task_ask.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    await user_examine(uid)
    mystr = "\n你今天有%d个任务" % len(data[uid]['task'])
    for i in range(len(data[uid]['task'])):
        if data[uid]['task'][i]['finish']:
            mystr += '\n█任务%d(已完成): ' % (i + 1) + data[uid]['task'][i]['describe']
        else:
            mystr += '\n█任务%d: ' % (i + 1) + data[uid]['task'][i]['describe']
    mystr += '\n\n任务需要手动提交\n指令:提交任务'
    await con.send(bot, event, mystr, at_sender=True)
    await task_ask.finish()

@task_submit.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    await user_examine(uid)
    msg = str(event.get_message()).strip()
    flag = True
    idx = 0
    if msg.isnumeric():
        idx = int(msg)
        if 1 <= idx <= len(data[uid]['task']):
            flag = False
            idx -= 1
    if flag:
        await con.send(bot, event, '你没有序号为[%s]的任务' % msg, at_sender=True)
        await task_submit.finish()
    if data[uid]['task'][idx]['finish']:
        await con.send(bot, event, '任务已经完成了', at_sender=True)
        await task_submit.finish()
    f = require("awesome_bot.plugins.game." + plugin_name[data[uid]['task'][idx]['name']]).getF
    n = f(uid)
    if n >= data[uid]['task'][idx]['num']:
        data[uid]['task'][idx]['finish'] = True
        await finish_bonus(bot, event, uid)
        await task_submit.finish()
    else:
        await con.send(bot, event, '任务还没完成呢\n进度: %d/%d' % (n, data[uid]['task'][idx]['num']), at_sender=True)
        await task_submit.finish()

async def finish_bonus(bot, event, uid):
    await datax.output()
    mystr = '\n任务成功完成啦'
    luck = await GetLuck(uid)
    if random.randint(0, 99) < 30 - 5 * luck:
        mystr += '\n获得十连券1张'
        c = await card.get(uid, 'ten')
        if c < 0:
            await card.new_user()
        await card.modify(uid, 'ten', 1)
    else:
        x = random.randint(1, 8 - luck)
        mystr += '\n获得单抽券%d张' % x
        c = await card.get(uid, 'single')
        if c < 0:
            await card.new_user()
        await card.modify(uid, 'single', x)
    await con.send(bot, event, mystr, at_sender=True)

async def user_examine(uid):
    uid = str(uid)
    if not uid in data:
        data[uid] = {
            'date': -1,
            'task': []
        }
    day = int(time.strftime("%j", time.localtime(time.time())))
    if day != data[uid]['date']:
        data[uid]['date'] = day
        luck = await GetLuck(uid)
        data[uid]['task'] = []
        if random.randint(0, 99) < 75 - luck * 5:
            m = 1000 * random.randint(1 + luck, 10)
            tsk = {
                'name': '球球机',
                'finish': False,
                'describe': '今天在球球机中赢得%dQ' % m,
                'num': m
            }
            data[uid]['task'].append(tsk)
        if random.randint(0, 99) < 75 - luck * 5:
            m = random.randint(1 + luck, 10)
            tsk = {
                'name': '21点',
                'finish': False,
                'describe': '今天在21点获胜%d局' % m,
                'num': m
            }
            data[uid]['task'].append(tsk)
        if random.randint(0, 99) < 75 - luck * 5 or len(data[uid]['task']) == 0:
            m = random.randint(1 + luck, 10)
            tsk = {
                'name': '猜数字',
                'finish': False,
                'describe': '今天进行%d局猜数字' % m,
                'num': m
            }
            data[uid]['task'].append(tsk)
        await datax.output()