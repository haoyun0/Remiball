from ..._gb import *
import math

game_guessnumber1 = on_command("开始猜数字", aliases={"开始 猜数字"}, rule=Check_('开始猜数字'), priority=10)
game_guessnumber2 = on_command("开始我来猜数字", aliases={"开始 我来猜数字"}, rule=Check_('开始我来猜数字'), priority=10)
game_guessnumber3 = on_command("开始极限猜数字", aliases={"开始 极限猜数字"}, rule=Check_('开始极限猜数字'), priority=10)
game_guessnumbertot = on_command("猜数字统计", rule=Check_('猜数字统计'), priority=10)
game_guessnumberrank = on_command("猜数字排行榜", aliases={"猜数字排行"}, rule=Check_('猜数字排行榜'), priority=10)

cmds = [
'开始猜数字',
'开始我来猜数字',
'开始极限猜数字',
'猜数字统计',
'猜数字排行榜'
]
con.addcmds('小游戏',cmds)
con.addcmds('基础功能',cmds)

datax = DataList('guessnumber')
data = datax.data

guess_bonus = [20000, 5000, 2000, 1000, 500, 200, 50, 10]

con.addhelp("猜数字","""
游戏规则：猜测一个各位不重复的四位数（首位可以是0）abcd。发送“猜数字 abcd”。结果会以“xAyB”的形式呈现。A表示位置和数字都猜对的情况；B表示数字对但位置不对的情况。
最多猜测8次
若带参数[复盘]，可以在游戏正常结束后复盘
若带参数[付费复盘]，花费100Q，功能更强大
若带参数[导师模式]，花费10000Q，复盘功能显性
若带参数[外挂模式]，花费100000Q，每步给出几种建议
若有账户可获得一丢丢Q奖励
相关指令：
开始猜数字
开始我来猜数字
开始极限猜数字
猜数字统计
猜数字排行榜
""".strip())

con.addhelp("我来猜数字","""
规则同猜数字，但是由蕾米球来猜，你来给出xAyB的形式来回复蕾米球
如果蕾米球猜中，请回答“恭喜你，猜中了”，双引号不用输入
目前算法复杂度过大，第一次回复可能需要等待几秒
不是最优解
""".strip())

con.addhelp("极限猜数字","""
规则同猜数字，但是你一定会遇到比较坏的情况，没有次数限制。
若带参数[导师模式]，花费100Q，获得显性复盘功能，蕾米球帮你分析对局
若带参数[宝宝模式]，花费1000Q，蕾米球手把手教你猜数字
""".strip())

number_org = []
for i1 in range(10):
    for i2 in range(10):
        for i3 in range(10):
            for i4 in range(10):
                if i1 != i2 and i1 != i3 and i1 != i4 and i2 != i3 and i2 != i4 and i3 != i4:
                    number_org.append(str(i1) + str(i2) + str(i3) + str(i4))

@game_guessnumber1.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    mode = ""
    mode = await mode_select(bot, event, state)
    if mode is None:
        await game_guessnumber1.finish()
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    number = ""
    for i in range(4):
        number += random.choice(numbers)
        numbers.remove(number[i])
    uid = str(event.user_id)
    await data_examine(uid)
    data[uid]['times'] += 1
    data[uid]['total'] += 9
    data[uid]['day']['times'] += 1
    data[uid]['day']['total'] += 9
    data[uid]['week']['times'] += 1
    data[uid]['week']['total'] += 9
    state['number'] = number
    state['times'] = 0
    state['history'] = "您本次的目标是猜出" + "".join(str(i) for i in number)
    state['p'] = number_org.copy()
    state['money'] = 1
    await con.send(bot, event, "数字已刷新，请直接发送猜测的四位数字进行猜测\n" + mode, at_sender=True)


@game_guessnumber2.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if str(event.message).strip():
        await game_guessnumber2.finish()
    state['numbers'] = number_org.copy()
    state['guess'] = '0123'
    await con.send(bot, event, "蕾米球已经准备好猜数字了\n蕾米球首先猜0123", at_sender=True)

@game_guessnumber3.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    mode = await mode_select2(bot, event, state)
    if mode is None:
        await game_guessnumber3.finish()
    state['numbers'] = number_org.copy()
    state['times'] = 0
    await con.send(bot, event, "数字已刷新，请直接发送猜测的四位数字进行猜测\n" + mode, at_sender=True)

@game_guessnumber1.receive()
async def receive(bot: Bot, event: Event, state: T_State):
    arg = str(event.message).strip()
    uid = str(event.user_id)
    if arg == '结束游戏' or arg == '结束' or arg == '认输' or arg == '投降':
        await datax.output()
        await con.send(bot, event, "已结束")
        await game_guessnumber1.finish()
    if len(arg) != 4:
        await game_guessnumber1.reject()
    if not arg.isnumeric():
        await con.send(bot, event, "格式错误，如有需要请输入结束游戏，并查看帮助", at_sender=True)
        await game_guessnumber1.reject()
    guess = ""
    a = 0
    b = 0
    number = state['number']
    for i in range(4):
        if arg[i] in guess:
            await con.send(bot, event, "请输入不带重复数字的四位数字")
            await game_guessnumber1.reject()
        else:
            guess += arg[i]
            if guess[i] == number[i]:
                a += 1
            elif guess[i] in number:
                b += 1
    state['times'] += 1
    ppp = state['p'].copy()
    for si in ppp:
        aa = 0
        bb = 0
        for i in range(4):
            if guess[i] == si[i]:
                aa += 1
            elif si[i] in guess:
                bb += 1
        if aa != a or bb != b:
            state['p'].remove(si)
    lx = len(ppp)
    if a == 4:
        ly = 0
    else:
        ly = len(state['p'])
    if data['times'][lx] >= 5:
        lz = data['all'][lx] / data['times'][lx]
    else:
        lz = lx
    if ly > 1:
        db = lz / ly + 1
    else:
        db = lz
    db = int(math.log2(db - 0.00001)) + 1
    if db < 1:
        db = 1
    state['money'] *= db


    data['all'][lx] += ly
    data['times'][lx] += 1
    tutor = '\n█你第%d次猜了' % state['times'] + guess
    if a == 4:
        tutor += '\n您在第%d次成功猜出' % state['times']
    else:
        tutor += '\n\t得到的反馈是%dA%dB' % (a, b)
        tutor += '\n\t剩余可能性数:' + str(ly)
        if len(state["p"]) <= 5:
            tutor += '\n\t他们分别为:' + str(state['p'])
        if data['times'][lx] > 5 and ly > 1:
            tutor += '\n\t玩家平均剩余可能性数:%.3f' % (lz)
        if state['vipre']:
            tutor += vipre(state['p'])
    state['history'] += tutor

    if a==4:
        z = await coin.get(uid)
        mystr = "恭喜你，猜中了！你本轮共猜了%d次" % state['times']
        if z >= 0:
            getq = state['money'] * guess_bonus[state['times'] - 1]
            if data[uid]['day']['times'] > 50:
                getq = 0
                mystr += "\n疲劳了，不获得Q"
            else:
                getq = int((1.02 - 0.02 * data[uid]['day']['times']) * getq)
                buff_f = require('awesome_bot.plugins.draw_card.user').getBuff
                buff = await buff_f(uid)
                if buff > 0:
                    mystr += '\n球球增益:%.1f%%' % buff
                getq = int(getq * (1 + buff / 100))
                mystr += "\n你获得了%dQ的奖励" % getq
            await coin.modify(uid, getq)
            data[uid]['total'] += state['times'] - 9
            data[uid]['day']['total'] += state['times'] - 9
            data[uid]['week']['total'] += state['times'] - 9
            await datax.output()
        await con.send(bot, event, mystr, at_sender=True)
        if state['re']:
            time.sleep(1)
            await con.send(bot, event, state['history'])
        await game_guessnumber1.finish()
    if state['tutor']:
        if state['cheat']:
            tutor += await get_advice(state['p'], a, b, number)
        await con.send(bot, event, tutor, at_sender=True)
    else:
        await con.send(bot, event, "%dA%dB" % (a, b), at_sender=True)
    if state["times"] >= 8:
        time.sleep(1)
        mystr = str(state['number'][0]) + str(state['number'][1]) + str(state['number'][2]) + str(state['number'][3])
        await con.send(bot, event, "游戏结束，你没有在8次中猜出来，据说最坏情况也能7次猜出哦。\n本次的答案是"+mystr, at_sender=True)
        if state['re']:
            time.sleep(1)
            await con.send(bot, event, state['history'])
        await game_guessnumber1.finish()
    await game_guessnumber1.reject()

@game_guessnumber2.receive()
async def receive(bot: Bot, event: Event, state: T_State):
    arg = str(event.message).strip()
    if arg == '结束游戏':
        await con.send(bot, event, "已结束")
        await game_guessnumber2.finish()
    if arg == '恭喜你，猜中了' or arg == '4A0B':
        await con.send(bot, event, "好耶，又猜中了一次")
        await game_guessnumber2.finish()
    if len(arg) != 4:
        await game_guessnumber2.reject()
    flag = True
    arg1 = arg.split('A')
    if len(arg1)==2:
        if arg1[0].isnumeric() and len(arg1[0])==1:
            aa = int(arg1[0])
            if arg1[1][1] == 'B':
                if arg1[1][0].isnumeric():
                    bb = int(arg1[1][0])
                    flag = False
    if flag:
        await con.send(bot, event, "格式错误，如有需要请输入结束游戏，并查看帮助", at_sender=True)
        await game_guessnumber2.reject()
    numbers = state['numbers'].copy()
    guess = state['guess']
    for k in numbers:
        a = 0
        b = 0
        for i in range(4):
            if guess[i] == k[i]:
                a += 1
            elif guess[i] in k:
                b += 1
        if a != aa or b != bb:
            state['numbers'].remove(k)
    numbers = state['numbers']
    if len(numbers) == 0:
        await con.send(bot, event, "你自相矛盾了，请确定你想的数字以及之前的回答", at_sender=True)
        await game_guessnumber2.finish()
    ans_min = 5040
    ans = []
    for guess in numbers:
        ans_max = 0
        for aa in range(5):
            if ans_max > ans_min:
                break
            for bb in range(5 - aa):
                if ans_max > ans_min:
                    break
                ans_now = 0
                for k in numbers:
                    a = 0
                    b = 0
                    for i in range(4):
                        if guess[i] == k[i]:
                            a += 1
                        elif guess[i] in k:
                            b += 1
                    if aa == a and bb == b:
                        ans_now += 1
                if ans_now > ans_max:
                    ans_max = ans_now
        if ans_max < ans_min:
            ans_min = ans_max
            ans.clear()
            ans.append(guess)
        elif ans_max == ans_min:
            ans.append(guess)
    state['guess'] = random.choice(ans)
    await con.send(bot, event, "蕾米球猜是 " + state['guess'], at_sender=True)
    await game_guessnumber2.reject()


@game_guessnumber3.receive()
async def receive(bot: Bot, event: Event, state: T_State):
    arg = str(event.get_message()).strip()
    if arg == '结束游戏':
        await con.send(bot, event, "已结束")
        await game_guessnumber3.finish()
    if arg == '公布答案':
        if len(state['numbers']) <= 10:
            mystr = "可能的答案有："
            for i in state["numbers"]:
                mystr += '\n' + str(i[0]) + str(i[1]) +str(i[2]) + str(i[3])
            await con.send(bot, event, mystr)
            await game_guessnumber3.finish()
        else:
            await con.send(bot, event, "别放弃，再努力一下吧")
            await game_guessnumber3.reject()
    if len(arg) != 4:
        await game_guessnumber3.reject()
    if not arg.isnumeric():
        await con.send(bot, event, "格式错误，如有需要请输入结束游戏，并查看帮助", at_sender=True)
        await game_guessnumber3.reject()
    guess = ""
    for i in range(4):
        if arg[i] in guess:
            await con.send(bot, event, "请输入不带重复数字的四位数字")
            await game_guessnumber3.reject()
        else:
            guess += arg[i]
    state["times"] += 1
    ans = []
    ans_max = 0
    for aa in range(5):
        for bb in range(5 - aa):
            ans_now = 0
            for k in state['numbers']:
                a = 0
                b = 0
                for i in range(4):
                    if guess[i] == k[i]:
                        a += 1
                    elif guess[i] in k:
                        b += 1
                if a==aa and b==bb:
                    ans_now += 1
            if ans_now > ans_max:
                ans_max = ans_now
                ans.clear()
                ans.append((aa, bb))
            elif ans_now == ans_max:
                ans.append((aa, bb))
    numbers = state['numbers'].copy()
    if (4, 0) in ans:
        ans.remove((4, 0))
    if len(ans) == 0:
        await con.send(bot, event, "恭喜你，猜中了！你本轮共猜了%d次" % state['times'], at_sender=True)
        await game_guessnumber3.finish()
    reply = random.choice(ans)
    for k in numbers:
        a = 0
        b = 0
        for i in range(4):
            if guess[i] == k[i]:
                a += 1
            elif guess[i] in k:
                b += 1
        if a != reply[0] or b != reply[1]:
            state['numbers'].remove(k)
    if state['tutor']:
        tutor = '\n█你第%d次猜了' % state['times'] + guess
        tutor += '\n\t得到的反馈是%dA%dB' % (reply[0], reply[1])
        tutor += '\n\t剩余可能性数:%d' % len(state['numbers'])
        if len(state['numbers']) <= 5:
            tutor += '\n\t他们分别为:' + str(state['numbers'])
        tutor += vipre(state['numbers'])
        if state['cheat']:
            tutor += await get_advice(state['numbers'], reply[0], reply[1], None)
        await con.send(bot, event, tutor, at_sender=True)
    else:
        await con.send(bot, event, "%dA%dB" % (reply[0], reply[1]), at_sender=True)
    await game_guessnumber3.reject()

@game_guessnumbertot.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    if not uid in data:
        data[uid] = {
            'times' : 0,
            'total' : 0,
            'date_day' : -1,
            'date_week' : -1,
            'day':{
                'times' : 0,
                'total' : 0
            },
            'week': {
                'times': 0,
                'total': 0
            }
        }
        await datax.output()
    if data[uid]['times'] > 0:
        mystr = "你一共猜了%d次，平均猜出次数为%.3f" % (data[uid]['times'], data[uid]['total'] / data[uid]['times'])
        mystr += "\n你这周猜了%d次，平均猜出次数为%.3f" % (data[uid]['week']['times'], data[uid]['week']['total'] / data[uid]['week']['times'])
        mystr += "\n你今天猜了%d次，平均猜出次数为%.3f" % (data[uid]['day']['times'], data[uid]['day']['total'] / data[uid]['day']['times'])
        await con.send(bot, event, mystr)
    else:
        await con.send(bot, event, "你还没有猜过数字")
    await game_guessnumbertot.finish()

@game_guessnumberrank.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    srt = []
    srt_day = []
    srt_week = []
    for uid in data:
        if uid.isnumeric():
            await data_examine(uid)
            if data[uid]['times'] >= 10:
                srt.append((data[uid]['total'] / data[uid]['times'], uid, data[uid]['times']))
            if data[uid]['week']['times'] >= 5:
                srt_week.append((data[uid]['week']['total'] / data[uid]['week']['times'], uid, data[uid]['week']['times']))
            if data[uid]['day']['times'] >= 3:
                srt_day.append((data[uid]['day']['total'] / data[uid]['day']['times'], uid, data[uid]['day']['times']))
    srt.sort()
    srt_day.sort()
    srt_week.sort()
    mystr = '█排行榜(总)前十如下:' + get_rank(srt, 10)
    mystr += '\n\n█排行榜(周)前五如下:' + get_rank(srt_week, 5)
    mystr += '\n\n█排行榜(日)前三如下:' + get_rank(srt_day, 3)


    await con.send(bot, event, mystr)
    await game_guessnumberrank.finish()

def get_rank(srt, l) -> str:
    ans = ""
    l = min(l, len(srt))
    for i in range(l):
        ans += '\n第%d名: %s\n\t平均猜测次数:%.3f\n\t总猜测次数:%d' % (
        i + 1, srt[i][1], srt[i][0], srt[i][2])
    return ans

async def data_examine(uid):
    uid = str(uid)
    if not uid in data:
        data[uid] = {
            'times': 0,
            'total': 0,
            'date_day': -1,
            'date_week': -1,
            'day': {
                'times': 0,
                'total': 0
            },
            'week': {
                'times': 0,
                'total': 0
            }
        }
        await datax.output()
    now = time.localtime(time.time())
    day = int(time.strftime("%j", now))
    week = int(time.strftime("%W", now))
    if not 'date_day' in data[uid]:
        data[uid]['date_day'] = day
        data[uid]['date_week'] = week
        data[uid]['day'] = {
            'times': 0,
            'total': 0
        }
        data[uid]['week'] = {
            'times': 0,
            'total': 0
        }
    if data[uid]['date_day'] != day:
        data[uid]['date_day'] = day
        data[uid]['day'] = {
                'times': 0,
                'total': 0
            }
        await datax.output()
    if data[uid]['date_week'] != week:
        data[uid]['date_week'] = week
        data[uid]['week'] = {
                'times': 0,
                'total': 0
            }
        await datax.output()


def vipre(dic: list):
    if len(dic) > 50:
        return ""
    if len(dic) <= 1:
        return ""
    ans = ""
    p  = {}
    for num in dic:
        ps = [num[0], num[1], num[2], num[3]]
        ps.sort()
        ns = "".join(ps)
        if not ns in p:
            p[ns] = 1
        else:
            p[ns] += 1
    if len(p) <= 10:
        ans += '\n\t可能的数字组合如下:'
        for num in p:
            ans += '\n\t\t%s: %d times' % (num, p[num])
        c = []
        for _ in range(10):
            c.append([0]*4)
        for num in dic:
            for j in range(4):
                c[ord(num[j]) - 48][j] += 1
        ans += '\n\t数字宫格如下:'
        for k in range(10):
            if c[k][0] + c[k][1] + c[k][2] + c[k][3] > 0:
                ans += '\n\t\t'
                for j in range(4):
                    if c[k][j] > 0:
                        ans += str(k)
                    else:
                        ans += 'x'
                ans += '\t\t%dtimes' % (c[k][0] + c[k][1] + c[k][2] + c[k][3])
    return ans

async def mode_select(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    uid = str(event.user_id)
    if msg == '复盘' or msg == '复盘模式':
        mode = '复盘模式'
        state['re'] = True
        state['vipre'] = False
        state['tutor'] = False
        state['cheat'] = False
    elif msg == '付费复盘' or msg == '付费复盘模式':
        m = await coin.get(uid)
        if m >= 100:
            await coin.modify(uid, -100)
        else:
            await con.send(bot, event, '你不够Q')
            return None
        mode = '付费复盘模式'
        state['re'] = True
        state['vipre'] = True
        state['tutor'] = False
        state['cheat'] = False
    elif msg == '导师模式' or msg == '导师':
        m = await coin.get(uid)
        if m >= 10000:
            await coin.modify(uid, -10000)
        else:
            await con.send(bot, event, '你不够Q')
            return None
        mode = '导师模式'
        state['re'] = True
        state['vipre'] = True
        state['tutor'] = True
        state['cheat'] = False
    elif msg == '外挂模式' or msg == '外挂' or msg == '开挂模式' or msg == '开挂':
        m = await coin.get(uid)
        if m >= 100000:
            await coin.modify(uid, -100000)
        else:
            await con.send(bot, event, '你不够Q')
            return None
        mode = '外挂模式'
        state['re'] = True
        state['vipre'] = True
        state['tutor'] = True
        state['cheat'] = True
    else:
        mode = '普通模式'
        state['re'] = False
        state['vipre'] = False
        state['tutor'] = False
        state['cheat'] = False
    return mode

async def mode_select2(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    uid = str(event.user_id)
    if msg == '导师模式' or msg == '导师':
        m = await coin.get(uid)
        if m >= 100:
            await coin.modify(uid, -100)
        else:
            await con.send(bot, event, '你不够Q')
            return None
        mode = '导师模式'
        state['tutor'] = True
        state['cheat'] = False
    elif msg == '宝宝模式' or msg == '宝宝':
        m = await coin.get(uid)
        if m >= 1000:
            await coin.modify(uid, -1000)
        else:
            await con.send(bot, event, '你不够Q')
            return None
        mode = '宝宝模式'
        state['tutor'] = True
        state['cheat'] = True
    else:
        mode = '普通模式'
        state['tutor'] = False
        state['cheat'] = False
    return mode

async def get_advice(numbers: list[str], aa, bb, real_num) -> str:
    ll = len(numbers)
    nm_c = numbers.copy()
    mystr = ""
    for _ in range(ll // 2):
        x = random.choice(nm_c)
        if real_num:
            while x == real_num:
                x = random.choice(nm_c)
        nm_c.remove(x)
    mystr += "\n土块的建议:" + random.choice(nm_c)
    if ll < 700:
        ans_min = 5040
        ans2_min = 5040
        ans = []
        ans2 = []
        for guess in numbers:
            ans_max = 0
            ans_now2 = 0
            for aa in range(5):
                for bb in range(5 - aa):
                    ans_now = 0
                    for k in numbers:
                        a = 0
                        b = 0
                        for i in range(4):
                            if guess[i] == k[i]:
                                a += 1
                            elif guess[i] in k:
                                b += 1
                        if aa == a and bb == b:
                            ans_now += 1
                    if ans_now > ans_max:
                        ans_max = ans_now
                    ans_now2 += ans_now * ans_now / ll
            if ans_max < ans_min:
                ans_min = ans_max
                ans.clear()
                ans.append(guess)
            elif ans_max == ans_min:
                ans.append(guess)
            if ans_now2 < ans2_min:
                ans2_min = ans_now2
                ans2.clear()
                ans2.append(guess)
            elif ans_now2 == ans2_min:
                ans2.append(guess)
        mystr += '\n稳妥的建议:' + random.choice(ans)
        mystr += '\n理智的建议:' + random.choice(ans2)
    return mystr

def GetTimes(uid):
    return data[uid]['day']['times']

export = export()
export.getF = GetTimes