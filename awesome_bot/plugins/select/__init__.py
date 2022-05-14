from .._gb import *

select = on_command("选择", rule=Check_("选择"), priority=5)
judge = on_command("判断", rule=Check_("判断"), priority=5)

cmds=[
'选择',
'判断'
]
con.addcmds('基础功能', cmds)
con.addcmds('帮你选择', cmds)

con.addhelp('选择',"""
选择 xx还是xx[还是xxx[...]] ：替你随机选择一个选项
判断 xx  ： 替你判断这个是对是错(随机)
""".strip(),
['判断', '帮你选择', '选择'])

scheduler = require('nonebot_plugin_apscheduler').scheduler

times = {}
err = {}

@select.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    flag = True
    if args:
        arg = args.split("还是")
        if len(arg)>=2:
            op = random.randint(0,len(arg)-1)
            await con.send(bot, event, "\n建议你选择%s" % arg[op], at_sender=True)
            flag = False
    if flag:
        await con.send(bot, event, "命令格式错误，请输入帮助帮你选择查看帮助")
    await select.finish()

@judge.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    arg = str(event.get_message()).strip()
    if event.group_id in err:
        if time.time() - err[event.group_id] < 60:
            await con.send(bot, event, "过载中……")
            await judge.finish()
    if not event.group_id in times:
        times[event.group_id] = 0
    times[event.group_id] += 1
    per = times[event.group_id] * 0.05
    if random.random() < per:
        err[event.group_id] = time.time()
        await con.send(bot, event, f"球脑过载，判断不出来了 #{per}")
        times[event.group_id] = 0
        await judge.finish()

    if arg:
        op = random.randint(0,1)
        mystr1 = "是"
        mystr2 = "否"
        if "是否" in arg:
            mystr1 = "是"
            mystr2 = "否"
        elif "好吗" in arg or "好不好" in arg:
            mystr1 = "好"
            mystr2 = "不好"
        elif "对吗" in arg or "对不对" in arg:
            mystr1 = "对"
            mystr2 = "不对"
        elif "该吗" in arg or "该不该" in arg:
            mystr1 = "应该"
            mystr2 = "不应该"
        elif "合适吗" in arg or "合不合适" in arg:
            mystr1 = "合适"
            mystr2 = "不合适"
        elif "不" in arg:
            id = arg.find("不")
            if arg[id - 1] == arg[id + 1]:
                mystr1 = arg[id - 1]
                mystr2 = '不' + arg[id + 1]
            elif arg[id-2: id] == arg[id+1: id+3]:
                mystr1 = arg[id - 2: id]
                mystr2 = '不' + arg[id - 2: id]

        if op:
            mystr = mystr1
        else:
            mystr = mystr2
        await con.send(bot, event, "\n%s\n判断：%s" % (arg, mystr), at_sender=True)
    else:
        await con.send(bot, event, "命令格式错误，请输入帮助帮你选择查看帮助")
    await judge.finish()

@scheduler.scheduled_job("interval" , minutes = 30)
async def re_handle():
    global times, err
    times = {}
    err = {}
