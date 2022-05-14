from .._gb import *

goodnight = on_command("晚安", aliases={"睡觉"}, rule=Check_('晚安', 'group'), priority=5)
goodmorning = on_command("早安", aliases={"起床"}, rule=Check_('早安', 'group'), priority=5)
goodsleep = on_command("打盹", aliases={"午安"}, rule=Check_('打盹', 'group'), priority=5)

datax = DataList('goodnight')
data = datax.data

cmds = [
'晚安',
'早安',
'打盹'
]
con.addcmds('早安晚安',cmds)
con.addcmds('基础功能',cmds)

con.addhelp('早安晚安',"""
早安：记录你是第几个起
晚安：禁言助眠及统计今天清醒时间
打盹\午安：参数可选睡觉时间(分钟)
""".strip(), ['早安','晚安'])


async def check():
    global data
    ddl: list = []
    for i in data['time']:
        flag = True
        t: list = data['time'][i]
        now = time.localtime(time.time())
        t2: list = []
        t2.append(time.strftime("%M", now))
        t2.append(time.strftime("%H", now))
        t2.append(time.strftime("%j", now))
        if t2[2] == t[2]:
            if int(t2[1]) >= 5 and int(t[1]) <= 4:
                flag = False
        elif int(t2[2]) - int(t[2]) == 1:
            if int(t2[1]) >= 5:
                flag = False
            elif int(t[1]) <= 4:
                flag = False
        else:
            flag = False
        if not flag:
            ddl.append(i)
    if len(ddl) > 0:
        for i in ddl:
            del data['time'][i]
            data['tot'] -= 1
        await datax.output()

async def add(qq: str):
    global data
    now = time.localtime(time.time())
    t: list = []
    t.append(time.strftime("%M",now))
    t.append(time.strftime("%H",now))
    t.append(time.strftime("%j",now))
    data['time'][qq] = t
    data['tot'] += 1
    await datax.output()

@goodnight.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if str(event.get_message()).strip():
        await goodnight.finish()
    await check()
    qq = str(event.user_id)
    if qq in data['time']:
        now = time.localtime(time.time())
        day = int(time.strftime("%j",now)) - int(data['time'][qq][2])
        hour = int(time.strftime("%H",now)) - int(data['time'][qq][1]) + day*24
        min = int(time.strftime("%M",now)) - int(data['time'][qq][0])
        if min < 0:
            min += 60
            hour -= 1
        if hour < 3 and int(time.strftime("%H", now))>=5:
            await con.send(bot, event, "刚起就不要睡啦QAQ")
        else:
            if qq in data['sleep']:
                await con.send(bot, event, "你已经发过晚安了，别玩手机早点休息吧（摸摸")
                await goodnight.finish()
            else:
                data['sleep'].append(qq)
                await datax.output()
            tim: int= random.randint(5*60*60, 7*60*60)
            await bot.call_api("set_group_ban_async", group_id=event.group_id, user_id=event.user_id, duration=tim)
            h = int(time.strftime("%H",now))
            if 0 <= h < 5:
                mystr = "不要熬夜哦！我可是很心疼你的喔"
            elif 5 <= h < 16:
                mystr = "大白天睡觉可还行！"
            elif 16 <= h < 20:
                mystr = "诶诶，这么早就要睡了么！"
            else:
                mystr = "晚安哦！"
            usr = await bot.call_api("get_group_member_info", group_id=event.group_id, user_id=event.user_id)
            me = await bot.call_api("get_group_member_info", group_id=event.group_id, user_id=event.self_id)
            mystr2 = ""
            if hour >= 12:
                rd = random.randint(1, 5)
                await coin.modify_love(event.user_id, rd)
                mystr2 = "\n蕾米球好感度增加: %d" % rd
            if (usr['role'] == 'member' and me['role'] != 'member') or me['role'] == 'owner':
                await con.send(bot, event, "%s\n你获得的睡眠时间为:\n%d分钟\n你今天的清醒时间为：\n%d小时%d分钟%s" % (mystr, tim//60, hour, min, mystr2), at_sender=True)
            else:
                await con.send(bot, event, "%s\n你今天的清醒时间为：\n%d小时%d分钟%s" % (mystr, hour, min, mystr2), at_sender=True)
    else:
        await con.send(bot, event, "你还没起呢，怎么就睡啦？")
    await goodnight.finish()

@goodmorning.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if str(event.get_message()).strip():
        await goodmorning.finish()
    await check()
    qq = str(event.user_id) 
    if qq in data['time']:
        await con.send(bot, event, "你已经起过床啦！")
    else:
        if qq in data['sleep']:
            data['sleep'].remove(qq)
            await datax.output()
        await add(str(event.user_id))
        now = time.localtime(time.time())
        hour = int(time.strftime("%H",now))
        if 0 <= hour < 5:
            mystr = "现在起床什么时候睡啊？"
        elif 5 <= hour < 8:
            mystr = "哇，起的真早！"
        elif 8 <= hour < 10:
            mystr = "早上好鸭！"
        elif 10 <= hour < 13:
            mystr = "都快中午了啦！"
        elif 13 <= hour < 16:
            mystr = "诶，一觉睡到下午了？！"
        elif 16 <= hour < 19:
            mystr = "夜行生物吗喂！"
        else:
            mystr = "现在起床还不如不起了呢！"
        mystr2 = "年"
        if event.sender.sex == "female":
            mystr2 = "女"
        await con.send(bot, event, f"%s少%s，你今天是第%d个起床的" % (mystr, mystr2, data['tot']), at_sender=True)
    await goodmorning.finish()

@goodsleep.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args and args.isdigit():
        min = int(args)
        if min <= 120:
            await bot.call_api("set_group_ban_async", group_id=event.group_id, user_id=event.user_id, duration=min*60)
            await con.send(bot, event, "你可以小睡%d分钟" % min)
        else:
            await con.send(bot, event, "不能休息这么久吧？")
    else:
        min = random.randint(20,60)
        await bot.call_api("set_group_ban_async", group_id=event.group_id, user_id=event.user_id, duration=min*60)
        await con.send(bot, event, "你可以小睡%d分钟" % min)
    await goodsleep.finish()