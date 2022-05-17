from .._gb import *


coin_daka = on_command("签到", aliases={"打卡"}, rule=Check_("签到"), priority=5)
coin_inf = on_command("个人信息", aliases={"个人资料", "我的", "信息", "个人查询"}, rule=Check_("个人信息"), priority=5)
coin_all = on_command("全服补偿", rule=Check_("全服补偿"), permission=SUPERUSER, priority=2)
coin_sin = on_command("补偿", rule=Check_("补偿"), permission=SUPERUSER, priority=2)
coin_vip = on_command("VIP", rule=Check_("VIP"), permission=SUPERUSER, priority=2)
coin_store = on_command("存Q", rule=Check_("存Q"), priority=5)
coin_load = on_command("取Q", rule=Check_("取Q"), priority=5)
coin_qbank = on_command("QBank", aliases={"Q存款"}, rule=Check_("QBank"), priority=5)
coin_loan = on_command("借Q", rule=Check_("借Q"), priority=5)
coin_give = on_command("转Q", rule=Check_("转Q"), priority=5)



cmds = [
'签到',
'个人信息',
'补偿',
'全服补偿',
'VIP',
'存Q',
'取Q',
'QBank',
'借Q',
'转Q'
]

con.addcmds('好感度系统',cmds)
con.addhelp('好感度系统',"""
每天签到可以获得一定的代币，
连续签到有额外奖励，还能增加蕾米球好感度
发送“打卡/签到”即可签到
（代币单位为Q，指球币）
发送“个人信息”可查看自己Q,好感度等
QBank请查看QBank的帮助
""".strip(), ['好感度','好感度功能','Q','Q系统','货币系统'])
con.addhelp('QBank',"""
QBank提供存取Q的服务
不收手续费，没有利息
指令：
存Q x:存xQ进入QBank
取Q x:从QBank取xQ出来
QBank:查看QBank里存了多少Q，欠了多少Q
借Q x:可借至多好感度*100的Q，借贷后所有收入25%将自动还款，不能主动还款，欠款时不能继续借，不收利息
转Q qq x:转给qq,xQ (转的是现Q，不是存款)
""".strip())



datax = coin.datax
data = coin.data

@coin_daka.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    uid = str(event.user_id)
    if not uid in data:
        data[uid] = {"last_day": 0, "coins": 0, "love": 0, "last": -1}
    day = int(time.strftime("%j",time.localtime(time.time())))
    if data[uid]["last"] == day:
        await con.send(bot, event, "你今天已经打过卡啦", at_sender=True)
        await coin_daka.finish()
    if data[uid]['last'] >= 365 or data[uid]["last"] == day - 1:
        data[uid]["last_day"] += 1
    else:
        data[uid]["last_day"] = 0
    luck = await GetLuck(uid)
    d1 = random.randint(251 - luck * 50, 500)
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = random.randint(1, 3) + 5 - luck
    mystr = "\n基础签到奖励：%dQ" % d1
    if data[uid]["last_day"] > 0:
        if data[uid]["last_day"] < 10:
            d2 = data[uid]["last_day"] * 50
        else:
            d2 = 500
        mystr += "\n连续签到奖励：%dQ" % d2

    if random.randint(0,99) < 20 - data[uid]["last_day"] - luck:
        r = random.randint(1,7)
        if r <= 4:
            d3 = 500
        elif r <= 6:
            d3 = 1000
        else:
            d3 = 2000
        mystr += "\n欧皇签到奖励：%dQ" % d3

    if 'vip' in data[uid]:
        mystr += '\n捐助签到奖励：%dQ' % data[uid]['vip']
        d4 = data[uid]['vip']

    if data[uid]["last_day"] > 5:
        dl = data[uid]["last_day"] - 5
        if dl > 5:
            dl = 5
        data[uid]["love"] += dl
        mystr += "\n蕾米球好感度增加：%d" % dl
    dc = await card.get(uid)
    if dc < 0:
        await card.new_user(uid)
    mystr += '\n获得了%d张单抽券' % d5

    dsum = d1 + d2 + d3 + d4
    buff_f = require('awesome_bot.plugins.draw_card.user').getBuff
    buff = await buff_f(uid)
    if buff > 0:
        mystr += '\n球球增益:%.1f%%' % (buff * 10)
    dsum = int(dsum * (1 + buff / 10))
    mystr += '\n共获得%dQ' % dsum

    await coin.modify(uid, dsum)
    data[uid]['last'] = day


    await card.modify(uid, 'single', d5)


    await con.send(bot, event, mystr, at_sender=True)
    await datax.output()
    await coin_daka.finish()

@coin_inf.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    uid = str(event.user_id)
    if not uid in data:
        data[uid] = {"last_day": 0, "coins": 0, "love": 0, "last": -1}
        await datax.output()
    mystr = ""
    if 'vip' in data[uid]:
        mystr +="\n感谢您，蕾米球的捐赠者"
    mystr += "\n你拥有：%dQ\n好感度：%d\n你已经连续签到了%d天" % (data[uid]['coins'], data[uid]['love'], data[uid]['last_day'] + 1)
    await con.send(bot, event, mystr, at_sender=True)
    await coin_inf.finish()

@coin_all.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    msg = str(event.get_message()).strip()
    if msg.isdigit():
        z = int(msg)
        for qq in data:
            await coin.modify(qq, z)
        await con.send(bot, event, '已全服补偿%dQ' % z)
    else:
        await con.send(bot, event, '非法参数')
    await coin_all.finish()

@coin_sin.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip().split()
    z0 = int(msg[0])
    z1 = int(msg[1])
    m = await coin.get(z0)
    if m >= 0:
        await coin.modify(z0, z1)
        await con.send(bot, event, '已补偿%dQ' % z1)
    await coin_sin.finish()

@coin_vip.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip().split()
    z0 = msg[0]
    z1 = int(msg[1])
    global data
    if 'vip' in data[z0]:
        data[z0]['vip'] += z1
    else:
        data[z0]['vip'] = z1
    await con.send(bot, event, '已添加')
    await datax.output()
    await coin_vip.finish()

@coin_store.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    uid = str(event.user_id)
    if not 'QBank' in data[uid]:
        data[uid]['QBank'] = 0
        await datax.output()
    m = await coin.get(uid)
    z = int(str(event.get_message()).strip())
    if z <= 0:
        await con.send(bot, event, '非法参数', at_sender=True)
        await coin_store.finish()
    if m < z:
        await con.send(bot, event, '你不够Q', at_sender=True)
    else:
        await coin.modify(uid, -z)
        data[uid]["QBank"] += z
        await datax.output()
        await con.send(bot, event, '存入%dQ成功' % z, at_sender=True)
    await coin_store.finish()

@coin_load.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    uid = str(event.user_id)
    if not 'QBank' in data[uid]:
        data[uid]['QBank'] = 0
        await datax.output()
    m = data[uid]['QBank']
    z = int(str(event.get_message()).strip())
    if z <= 0:
        await con.send(bot, event, '非法参数', at_sender=True)
        await coin_load.finish()
    if m < z:
        await con.send(bot, event, '你不够Q', at_sender=True)
    else:
        await coin.modify(uid, z)
        data[uid]["QBank"] -= z
        await datax.output()
        await con.send(bot, event, '取出%dQ成功' % z, at_sender=True)
    await coin_load.finish()

@coin_qbank.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global data
    uid = str(event.user_id)
    if not 'QBank' in data[uid]:
        data[uid]['QBank'] = 0
        await datax.output()
    mystr = "您在QBank的存款为：%dQ" % data[uid]['QBank']
    if not 'loan' in data[uid]:
        data[uid]['loan'] = 0
        await datax.output()
    if data[uid]['loan'] > 0:
        mystr += '\n你目前负债%dQ' % data[uid]['loan']
    await con.send(bot, event, mystr, at_sender=True)
    await coin_qbank.finish()

@coin_loan.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    z = str(event.get_message()).strip()
    if not 'loan' in data[uid]:
        data[uid]['loan'] = 0
        await datax.output()
    if z.isnumeric():
        z = int(z)
        if z > 0:
            if data[uid]['loan'] > 0:
                await con.send(bot, event, '你还欠着呢，还完再说')
            else:
                if z <= data[uid]['love'] * 100 + 1000:
                    await con.send(bot, event, '成功借款%dQ' % z)
                    await coin.modify(uid, z)
                    data[uid]['loan'] = z
                    await datax.output()
                else:
                    await con.send(bot, event, '我们的关系好像不值这么多吧')
        else:
            await con.send(bot, event, '参数非法')
    else:
        await con.send(bot, event, '参数非法')

@coin_give.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msgs = str(event.get_message()).strip().split()
    if len(msgs) != 2:
        await con.send(bot, event, '格式错误')
        await coin_give.finish()
    uid = str(event.user_id)
    qid = msgs[0]
    z = msgs[1]
    if not z.isnumeric():
        await con.send(bot, event, '格式错误')
        await coin_give.finish()
    z = int(z)
    if z <= 0:
        await con.send(bot, event, '转让Q数量非法')
        await coin_give.finish()
    m = await coin.get(qid)
    if m < 0:
        await con.send(bot, event, '对方不存在Q账户')
        await coin_give.finish()
    m = await coin.get(uid)
    if m < z:
        await con.send(bot, event, '你不够Q')
        await coin_give.finish()
    await coin.modify(uid, -z)
    await coin.modify(qid, z)
    await con.send(bot, event, '成功转让%dQ给%s' % (z, qid), at_sender=True)
    await coin_give.finish()

