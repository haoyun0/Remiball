from ..._gb import *

g21 = on_command('开始21点', rule=Check_('开始21点'), priority=5)
g21x = on_command('开始多人21点', rule=Check_("开始多人21点", 'group'), priority=5)
g21_see = on_command("查看21点牌堆", rule=Check_("查看21点牌堆", 'private'), permission=SSpecial_list([]),priority=6)
g21_tot = on_command("21点统计", rule=Check_("21点统计"), priority=5)
cmds = [
'开始21点',
'开始多人21点',
"查看21点牌堆",
'21点统计'
]
con.addcmds('好感度系统', cmds)
con.addcmds('小游戏', cmds)
con.addcmds('基础功能', cmds)

con.addhelp('21点', """
21点游戏者的目标是使手中的牌的点数之和不超过 21 点且尽量大
开始时，蕾米球坐庄，一开始明一张牌，暗一张牌，
玩家会获得两张牌，首先玩家开始要牌，可以随意要多少张，但是如果所有的牌加起来超过21点，玩家就输了
当玩家决定不要牌时，蕾米球开始要牌，最后比最终大小。
必须下注，必须为10的正次方，如10,100,1000,1000……
货币为Q，签到可得
获胜之后获得双倍赌注，失败之后就没了。
牌型：
黑杰克：一张A，一张十点数的牌，所有牌型最大
五小龙：5张牌后还没超过21点，除黑杰克最大
游戏外指令：
开始21点 [赌注(数字，可选)],例!开始21点 100
游戏中指令：
要牌/拿牌：要一张牌
结束/停牌：结束要牌
加倍/翻倍：玩家没有黑杰克，可加倍，加倍后立刻摸一张牌，且不能再摸
以下为第一次要牌开始前操作：
保险：若蕾米球明牌为A，可以选择花一半注金买保险，如果蕾米球是黑杰克，玩家可拿回额外两倍保险金，如果没有，玩家输掉保险金，游戏正常继续
认输/投降/弃牌：若蕾米球明牌不为A，可以认输，获得一半的赌注并立刻输掉
牌堆：查看牌堆还剩下多少张牌

""".strip(), ['开始21点'])

con.addhelp('多人21点', """
比大小规则同21点，大家起手一张暗牌一张明牌，抽到是暗牌
暗牌由蕾米球私聊发送，但是要牌等操作只能在群聊进行
游戏分为三阶段，分别为盲注阶段和要牌阶段和最后阶段：
盲注阶段：
大家只能看见所有人的明牌，不能要牌，开始加一轮注，直到所有人都选择过牌
其中，一开始随机一人强制加盲注100
要牌阶段：
该阶段各自要牌直到所有人停牌
最后阶段：
正常操作直到所有人都选择过牌
游戏中操作：
要牌/拿牌：你可以在要牌阶段要一张牌，但是>=21点或者有五张牌后就不能要了
停牌：在要牌阶段不继续要牌后请输入停牌
加注：在最大注的基础上加注x，到你的回合时，你永远可以进行加注, 100起步
跟注/跟牌：跟注到最大注
过牌：如果你是最大注，可以过牌
梭哈/allin：直接梭哈所有Q，如果不如最大注，如果最后赢了将按比例分
弃牌/认输/投降：你可以选择弃牌结束游戏，已经下了的注不会归还
""".strip())

colors = ['♦', '♣', '♥', '♠']
points = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
pile_org = []

datax = DataList('21')
data = datax.data

friend_list = []
for i in range(4):
    for j in range(13):
        pile_org.append({
            "color" : i,
            "point" : j
        })
async def Reflash(bot = None):
    global  pile_org
    p = []
    for _ in range(52):
        g = random.choice(pile_org)
        while g in p:
            g = random.choice(pile_org)
        p.append(g)
    if bot:
        mystr = '牌堆已刷新\n'
        for x in p:
            mystr += GetName(x) + ', '
        await bot.send_private_msg(user_id = 847360401, message = mystr)
    return p
pile = []

async def GetOne(bot = None):
    global pile
    if len(pile) == 0:
        pile = await Reflash(bot)
    x = pile[0]
    del pile[0]
    return x

def GetName(a):
    return colors[a['color']] + points[a['point']]

def GetPoints(a):
    flag = False
    pt = 0
    for i in a:
        if i['point'] > 9:
            pt += 10
        else:
            pt += i['point'] + 1
            if i['point'] == 0:
                flag = True
    if flag and pt <= 11:
        pt += 10
    return pt

def BJ(a):
    if len(a) == 2:
        if a[0]['point'] == 0 and a[1]['point'] >= 9:
            return True
        elif a[1]['point'] == 0 and a[0]['point'] >= 9:
            return True
    return False


def Count(remi, player):
    if GetPoints(remi) >= 19:
        return False
    if GetPoints(remi) < GetPoints(player) and GetPoints(remi) < 17:
        return True
    if GetPoints(remi) > GetPoints(player) and GetPoints(remi) >= 15:
        return False
    global pile
    pd = pile.copy()
    pl = player.copy()
    rm = remi.copy()
    pd.append(player[-1])
    pt0 = GetPoints(rm)
    rm.append(pd[0])
    cx = 0
    cy = 0
    for i in pd:
        pl[-1] = i
        pt1 = GetPoints(pl)
        if pt1 >= 15:
            for k in pd:
                if k!=i:
                    rm[-1] = k
                    if pt0 <= pt1 and (pt0 < GetPoints(rm) <= 21 or pt0 <= 14):
                        cx += 1
                    else:
                        cy += 1
    if cy == 0:
        return True
    else:
        return cx / cy > 0.3

@g21.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    z = str(event.get_message()).strip()
    flag = True
    if z.isnumeric():
        if z[0] == '1' and len(z) > 1:
            for i in range(1, len(z)):
                if z[i] != '0':
                    flag = False
                    break
        else:
            flag = False
    else:
        flag = False

    if not flag:
        await con.send(bot, event, "请下注且下正确的金额", at_sender=True)
        await g21.finish()
    z = int(z)
    m = await coin.get(event.user_id)
    if m < z:
        await con.send(bot, event, "你不够Q")
        await g21.finish()
    uid = str(event.user_id)
    await user_exmine(uid)
    await coin.modify(uid, -z)
    data[uid]['times'] += 1
    data[uid]['day_times'] += 1
    data[uid]['Q_in'] += z
    data[uid]['day_in'] += z
    state['remi'] = [await GetOne(bot), await GetOne(bot)]
    state['player'] = [await GetOne(bot), await GetOne(bot)]
    state['money'] = z
    state['fail'] = True
    state['double'] = False
    state['ins'] = 0
    mystr = "\n蕾米球的手牌为: " + GetName(state['remi'][0]) + ', ?\n'
    mystr += "你的手牌为: " + GetName(state["player"][0])
    for i in range(1, len(state['player'])):
        mystr += ', ' + GetName(state["player"][i])
    #await bot.call_api('send_group_msg', group_id=963370810, message="testing 21: message_type=" + event.message_type +", sub_type=" + event.sub_type)
    await con.send(bot, event, mystr, at_sender=True)




@g21.receive()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    uid = str(event.user_id)
    if msg == '认输' or msg == '投降' or msg == '弃牌':
        if state['fail']:
            if state['remi'][0]['point'] == 0:
                await con.send(bot, event, '蕾米球明牌为A，不能认输，考虑买保险')
                await g21.reject()
            else:
                await con.send(bot, event, '你认输了，拿回一半Q', at_sender=True)
                await coin.modify(uid, state['money'] // 2)
                data[uid]['Q_out'] += state['money'] // 2
                data[uid]['day_out'] += state['money'] // 2
                await datax.output()
                await g21.finish()
        else:
            await con.send(bot, event, '你已经要过牌了，不能认输了哦', at_sender=True)
            await g21.reject()
    elif msg == '要牌' or msg == '拿牌':
        if state['double']:
            await con.send(bot, event, '你已经加倍了，不能再要了，请结束', at_sender=True)
            await g21.reject()
        if len(state['player']) >= 5:
            await con.send(bot, event, '你有5张牌了，不能再要了，请结束', at_sender=True)
            await g21.reject()
        elif BJ(state['player']):
            await con.send(bot, event, '你有黑杰克，不能再要了，请结束', at_sender=True)
            await g21.reject()
        state['fail'] = False
        state['player'].append(await GetOne(bot))
        mystr = "\n蕾米球的手牌为: " + GetName(state['remi'][0]) + ', ?\n'
        mystr += "你的手牌为: " + GetName(state["player"][0])
        for i in range(1, len(state['player'])):
            mystr += ', ' + GetName(state["player"][i])
        await con.send(bot, event, mystr, at_sender=True)
        pt = GetPoints(state['player'])
        if pt > 21:
            await datax.output()
            await con.send(bot, event, 'You lose!', at_sender=True)
            await g21.finish()
        await g21.reject()
    elif msg == '加倍' or msg == '翻倍':
        if state['double']:
            await con.send(bot, event, "你已加倍，不能再加倍", at_sender=True)
        else:
            if BJ(state['player']):
                await con.send(bot, event, "你有黑杰克，不能加倍", at_sender=True)
                await g21.reject()
            else:
                m = await coin.get(uid)
                if m < state['money']:
                    await con.send(bot, event, "你不够Q")
                    await g21.reject()
                else:
                    await con.send(bot, event, "你已加倍", at_sender=True)
                    await coin.modify(uid, -state['money'])
                    data[uid]['Q_in'] += state['money']
                    data[uid]['day_in'] += state['money']
                    state['money'] *= 2
                    state['double'] = True
                    state['fail'] = False
                    state['player'].append(await GetOne(bot))
                    mystr = "\n蕾米球的手牌为: " + GetName(state['remi'][0]) + ', ?\n'
                    mystr += "你的手牌为: " + GetName(state["player"][0])
                    for i in range(1, len(state['player'])):
                        mystr += ', ' + GetName(state["player"][i])
                    await con.send(bot, event, mystr, at_sender=True)
                    pt = GetPoints(state['player'])
                    if pt > 21:
                        await datax.output()
                        await con.send(bot, event, 'You lose!', at_sender=True)
                        await g21.finish()
                    time.sleep(1.5)
    elif msg == '保险':
        if state['fail']:
            if state['remi'][0]['point'] == 0:
                m = await coin.get(uid)
                if m < state['money'] // 2:
                    await con.send(bot, event, "你不够Q")
                else:
                    await con.send(bot, event, "你已买保险", at_sender=True)
                    data[uid]['Q_in'] += state['money'] // 2
                    data[uid]['day_in'] += state['money'] // 2
                    state['ins'] = state['money'] // 2
                    await coin.modify(event.user_id, -state['ins'])
            else:
                await con.send(bot, event, "蕾米球明牌不为A，不能买保险", at_sender=True)
        elif state['ins'] > 0:
            await con.send(bot, event, "你已经买过保险啦", at_sender=True)
        else:
            await con.send(bot, event, "你已要牌，不能买保险", at_sender=True)
        await g21.reject()
    elif msg == '牌堆':
        await con.send(bot, event, "牌堆有%d张牌" % len(pile), at_sender=True)
        await g21.reject()
    if msg == '停牌' or msg == '结束' or state['double']:
        mystr = "\n你的手牌为: " + GetName(state["player"][0])
        for i in range(1, len(state['player'])):
            mystr += ', ' + GetName(state["player"][i])
        pt0 = GetPoints(state['player'])
        mystr += "\n你的得分为：%d" % pt0
        await con.send(bot, event, mystr, at_sender=True)
        time.sleep(1)
        if state['ins'] > 0:
            if BJ(state['remi']):
                await con.send(bot, event, '黑杰克，获得双倍保险金', at_sender=True)
                await coin.modify(event.user_id, state['ins'] * 3)
                data['Q_out'] += state['ins'] * 3
                data['day_out'] += state['ins'] * 3
            else:
                await con.send(bot, event, '蕾米球没有黑杰克，输掉保险金', at_sender=True)
            time.sleep(1)
        while True:
            mystr = "\n蕾米球的手牌为: " + GetName(state['remi'][0])
            for i in range(1, len(state['remi'])):
                mystr += ', ' + GetName(state["remi"][i])
            pt1 = GetPoints(state['remi'])
            mystr += "\n蕾米球的得分为：%d" % pt1
            await con.send(bot, event, mystr, at_sender=True)
            if pt1 > 21:
                await win21(bot, event, state)
                await g21.finish()
            elif len(state['remi']) < 5 and not BJ(state['remi']) and (len(state['player']) >=5 or Count(state['remi'], state['player'])):
                state['remi'].append(await GetOne(bot))
                time.sleep(1.5)
            else:
                if len(state['player']) >= 5:
                    if len(state['remi']) < 5:
                        if BJ(state['remi']):
                            await datax.output()
                            await con.send(bot, event, 'Black Jack! You lose!', at_sender=True)
                        else:
                            await win21(bot, event, state)
                    else:
                        if pt0 >  pt1:
                            await win21(bot, event, state)
                        elif pt0 == pt1:
                            await con.send(bot, event, "平局，你能拿回你的Q", at_sender=True)
                            await coin.modify(event.user_id, state['money'])
                            data['Q_out'] += state['money']
                            data['day_out'] += state['money']
                            await datax.output()
                        else:
                            await datax.output()
                            await con.send(bot, event, 'You lose!', at_sender=True)
                elif len(state['remi']) >= 5:
                    if BJ(state['player']):
                        await win21(bot, event, state)
                    else:
                        await datax.output()
                        await con.send(bot, event, '五小龙, You lose!', at_sender=True)
                elif pt1 > pt0:
                    await datax.output()
                    await con.send(bot, event, 'You lose!', at_sender=True)
                elif pt1 == pt0:
                    if BJ(state['player']):
                        if not BJ(state['remi']):
                            await win21(bot, event, state)
                            await g21.finish()
                    if BJ(state['remi']):
                        if not BJ(state['player']):
                            await datax.output()
                            await con.send(bot, event, 'Black Jack! You lose!', at_sender=True)
                            await g21.finish()
                    await con.send(bot, event, "平局，你能拿回你的Q", at_sender=True)
                    await coin.modify(event.user_id, state['money'])
                    data['Q_out'] += state['money']
                    data['day_out'] += state['money']
                    await datax.output()
                else:
                    await win21(bot, event, state)
                await g21.finish()
    await g21.reject()
room = {}

async def win21(bot, event, state):
    uid = str(event.user_id)
    if BJ(state['player']):
        await con.send(bot, event, 'You win! 黑杰克，额外获得一倍Q', at_sender=True)
        await coin.modify(event.user_id, state['money'] * 3)
        data[uid]['Q_out'] += state['money'] * 3
        data[uid]['day_out'] += state['money'] * 3
    else:
        await con.send(bot, event, 'You win!', at_sender=True)
        await coin.modify(event.user_id, state['money'] * 2)
        data[uid]['Q_out'] += state['money'] * 2
        data[uid]['day_out'] += state['money'] * 2
    data[uid]['wins'] += 1
    data[uid]['day_wins'] += 1
    await datax.output()

async def GetNext(bot: Bot, event: Event, gid: int):
    global room
    k = len(room[gid]['players'])
    nnid = -1
    cnt = 0
    cnt2 = 0
    for uid in room[gid]['players']:
        if not room[gid]['player'][uid]['fail']:
            cnt2 += 1
    if 0 <= cnt2 <= 1:
        return cnt2
    for i in range(k + 1):
        room[gid]['now'] += 1
        if room[gid]['now'] >= k:
            room[gid]['now'] = 0
        nid = room[gid]['players'][room[gid]['now']]
        if nnid == -1 and room[gid]['skip'] == nid:
            return 0
        if room[gid]['player'][nid]['soha']:
            continue
        if not room[gid]['player'][nid]['fail']:
            if i < k:
                cnt += 1
            if nnid == -1:
                nnid = room[gid]['now']
    if nnid >= 0:
        room[gid]['now'] = nnid
        mystr = "现在是[CQ:at,qq=%d]的回合\n现在最大注为%d" % (room[gid]['players'][room[gid]['now']], room[gid]['max'])
        await con.send(bot, event, mystr)
    if cnt == 1:
        flag = False
        for q in room[gid]['players']:
            if room[gid]['player'][q]['soha']:
                pass
            if room[gid]['player'][q]['money'] < room[gid]['max']:
                flag = True
                break
        if flag:
            cnt = 2
    return cnt

def GetWinner(a, gid):
    if len(a) == 1:
        return a
    global room
    ans = []
    #BJ
    for q in a:
        if BJ(room[gid]['player'][q]['card']):
            ans.append(q)
    if len(ans) > 0:
        return ans
    #5
    maxx = 0
    for q in a:
        if len(room[gid]['player'][q]['card']) >=5 and maxx < GetPoints(room[gid]['player'][q]['card']) <= 21:
            maxx = GetPoints(room[gid]['player'][q]['card'])
    if maxx > 0:
        for q in a:
            if len(room[gid]['player'][q]['card']) >=5 and maxx == GetPoints(room[gid]['player'][q]['card']):
                ans.append(q)
    if len(ans) > 0:
        return ans
    #normal
    for q in a:
        if maxx < GetPoints(room[gid]['player'][q]['card']) <= 21:
            maxx = GetPoints(room[gid]['player'][q]['card'])
    if maxx > 0:
        for q in a:
            if maxx == GetPoints(room[gid]['player'][q]['card']):
                ans.append(q)
    if len(ans) > 0:
        return ans
    #fail
    return a.copy()

@g21_see.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global pile
    pp = pile.copy()
    mystr = '牌堆有%d张牌\n' % len(pp)
    for x in pp:
        mystr += GetName(x) + ', '
    await con.send(bot, event, mystr)
    await g21_see.finish()

@g21x.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    global room, friend_list
    if len(friend_list) == 0:
        fl = await bot.call_api('get_friend_list')
        for fd in fl:
            friend_list.append(fd['user_id'])
    if event.group_id in room:
        if room[event.group_id]['total'] > 0:
            await con.send(bot, event, '游戏已经在进行中')
            await g21x.finish()
        if event.user_id in room[event.group_id]['players']:
            await con.send(bot, event, "检测到过期房间，已清除，请重新输入该指令开房")
            del room[event.group_id]
            await g21x.finish()
        m = await coin.get(event.user_id)
        if m < 100:
            await con.send(bot, event, "你不够Q")
            await g21x.finish()
        state['author'] = False
        room[event.group_id]['players'].append(event.user_id)
        room[event.group_id]['player'][event.user_id] = {}
        await con.send(bot, event, "已加入本群21点房间，若房主不在可输入'拆房'来解散房间")
    else:
        m = await coin.get(event.user_id)
        if m < 100:
            await con.send(bot, event, "你不够Q")
            await g21x.finish()
        room[event.group_id] = {
            'player' : {
                event.user_id:{}
            },
            'players': [event.user_id],
            'max' : 0,
            'total' : 0,
            'start' : -1,
            'now' : 0
        }
        state['author'] = True
        await con.send(bot, event, "本群21点房间已创建，房主在够人之后可以发'开始游戏'来开始")

@g21x.receive()
async def handle(bot: Bot, event: Event, state: T_State):
    global room
    gid = event.group_id
    uid = event.user_id
    cnt = -1
    fail_flag = False
    if gid in room:
        if uid in room[gid]['players']:
            pass
        else:
            await con.send(bot, event, "房间已解散", at_sender=True)
            await g21x.finish()
    else:
        await con.send(bot, event, "房间已解散", at_sender=True)
        await g21x.finish()
    msg = str(event.get_message()).strip().split()
    if msg[0] == '开始游戏':
        if state['author']:
            if len(room[gid]['players']) >= 2:
                await con.send(bot, event, "游戏开始")
                room[gid]['total'] = 100
                l = len(room[gid]['players'])
                st = random.randint(0, l - 1)
                room[gid]['start'] = st
                idst = room[gid]['players'][st]
                m = await coin.get(idst)
                if m < 100:
                    await con.send(bot, event, "没有100Q还想玩21点？爬！\n[CQ:at,qq=%d]被踢出了房间\n意外情况，房间解散" % idst)
                    await bot.call_api("set_group_ban_async", group_id=event.group_id, user_id=idst,
                                       duration=60)
                    del room[gid]
                    await g21x.finish()
                await coin.modify(idst, -100)
                mystr = '首先，[CQ:at,qq=%d]强制下盲注100' % idst
                await con.send(bot, event, mystr)
                room[gid]['now'] = st + 1
                if room[gid]['now'] >= l:
                    room[gid]['now'] = 0
                mystrx = "大家的明牌分别是:"
                for i in range(0, l):
                    id = room[gid]['players'][(st + i + l) % l]
                    room[gid]['player'][id]['card'] = [await GetOne(bot), await GetOne(bot)]
                    mystrx += '\n[CQ:at,qq=%d] ' % id + GetName(room[gid]['player'][id]['card'][0])
                    room[gid]['player'][id]['money'] = 0
                    room[gid]['player'][id]['soha'] = False
                    room[gid]['player'][id]['fail'] = False
                    room[gid]['player'][id]['stop'] = False
                await con.send(bot, event, mystrx)
                room[gid]['player'][idst]['money'] = 100
                room[gid]['max'] = 100
                room[gid]['blind'] = True
                room[gid]['get'] = False
                room[gid]['final'] = False
                room[gid]['skip'] = room[gid]['players'][room[gid]['now']]
                room[gid]['remain'] = l
                room[gid]['stop'] = 0
                room[gid]['add'] = 0
                await con.send(bot, event, "现在为：盲注阶段")
                time.sleep(0.5)
                mystr = "现在是[CQ:at,qq=%d]的回合\n现在最大注为%d" % (room[gid]['players'][room[gid]['now']], room[gid]['max'])
                await con.send(bot, event, mystr)
            else:
                await con.send(bot, event, "你跟自己玩吗？")
        else:
            await con.send(bot, event, "你不是房主，请让房主开始游戏")
    elif msg[0] == '拆房':
        if room[gid]['total'] > 0:
            await con.send(bot, event, "游戏正在进行中")
        else:
            del room[gid]
            await con.send(bot, event, "房间已解散", at_sender=True)
            await g21x.finish()
    elif msg[0] == '要牌' or msg[0] == '拿牌':
        if GetPoints(room[gid]['player'][uid]['card']) >= 21 or len(room[gid]['player'][uid]['card']) >= 5 or room[gid]['player'][uid]['stop']:
            if uid in friend_list:
                await bot.call_api('send_private_msg', user_id=uid, message="不能再要牌了")
            else:
                await bot.sendTempMsg(group_id=gid, user_id=uid, message="不能再要牌了")
        elif not room[gid]['get']:
            await con.send(bot, event, "非要牌阶段不能要牌", at_sender=True)
        else:
            room[gid]['player'][uid]['card'].append(await GetOne(bot))
            mystr = "你的手牌为: " + GetName(room[gid]['player'][uid]['card'][0])
            for i in range(1, len(room[gid]['player'][uid]['card'])):
                mystr += ', ' + GetName(room[gid]['player'][uid]['card'][i])
            if uid in friend_list:
                await bot.call_api('send_private_msg', user_id=uid, message=mystr)
            else:
                await bot.sendTempMsg(group_id=gid, user_id=uid, message=mystr)
    elif msg[0] == '跟注' or msg[0] == '跟牌':
        if room[gid]['get']:
            await con.send(bot, event, "要牌阶段只能要牌", at_sender=True)
        elif uid == room[gid]['players'][room[gid]['now']]:
            z = room[gid]['max'] - room[gid]['player'][uid]['money']
            m = await coin.get(uid)
            if m < z:
                await con.send(bot, event, "你不够Q")
            else:
                room[gid]['total'] += z
                await coin.modify(uid, -z)
                room[gid]['player'][uid]['money'] = room[gid]['max']
                await con.send(bot, event, "你已跟注", at_sender=True)
                cnt = await GetNext(bot, event, gid)
        else:
            await con.send(bot, event, "现在不是你的回合", at_sender=True)
    elif msg[0] == '加注':
        if room[gid]['get']:
            await con.send(bot, event, "要牌阶段只能要牌", at_sender=True)
        elif uid == room[gid]['players'][room[gid]['now']]:
            if msg[1].isnumeric():
                x = int(msg[1])
                if x >= 100:
                    m = await coin.get(uid)
                    z = room[gid]['max'] + x - room[gid]['player'][uid]['money']
                    room[gid]['skip'] = uid
                    if m < z:
                        await con.send(bot, event, "你不够Q")
                    else:
                        room[gid]['add'] = uid
                        room[gid]['total'] += z
                        await coin.modify(uid, -z)
                        room[gid]['max'] += x
                        room[gid]['player'][uid]['money'] = room[gid]["max"]
                        await con.send(bot, event, "你已加注%dQ" % x)
                        cnt = await GetNext(bot, event, gid)
                else:
                    await con.send(bot, event, "加注数量非法")
            else:
                await con.send(bot, event, "加注数量非法")
        else:
            await con.send(bot, event, "现在不是你的回合", at_sender=True)
    elif msg[0] == '弃牌' or msg[0] == '认输' or msg[0] == '投降':
        if room[gid]['get']:
            await con.send(bot, event, "要牌阶段只能要牌", at_sender=True)
        elif uid == room[gid]['players'][room[gid]['now']]:
            if room[gid]['player'][uid]['fail']:
                await con.send(bot, event, "你已经弃牌了", at_sender=True)
            else:
                room[gid]['stop'] += 1
                room[gid]['player'][uid]['fail'] = True
                await con.send(bot, event, "你已弃牌", at_sender=True)
                cnt = await GetNext(bot, event, gid)
                if room[gid]['skip'] == uid:
                    room[gid]['skip'] = room[gid]['players'][room[gid]['now']]
                fail_flag = True
        else:
            await con.send(bot, event, "现在不是你的回合", at_sender=True)
    elif msg[0] == '过牌':
        if room[gid]['get']:
            await con.send(bot, event, "要牌阶段只能要牌", at_sender=True)
        elif uid == room[gid]['players'][room[gid]['now']]:
            if room[gid]['player'][uid]['money'] == room[gid]['max']:
                await con.send(bot, event, "你选择过牌", at_sender=True)
                cnt = await GetNext(bot, event, gid)
            else:
                await con.send(bot, event, "你不是最大注，不能过牌", at_sender=True)
        else:
            await con.send(bot, event, "现在不是你的回合", at_sender=True)
    elif msg[0] == '梭哈' or msg[0] == 'allin':
        if room[gid]['get']:
            await con.send(bot, event, "要牌阶段只能要牌", at_sender=True)
        elif uid == room[gid]['players'][room[gid]['now']]:
            m = await coin.get(uid)
            if m + room[gid]['player'][uid]['money'] < 100:
                await con.send(bot, event, "没有100Q还想玩21点？爬！")
                await con.send(bot, event, "被踢出了房间", at_sender=True)
                await bot.call_api("set_group_ban_async", group_id=event.group_id, user_id=uid,
                                   duration=60)
                room[gid]['stop'] += 1
                room[gid]['player'][uid]['fail'] = True
                room[gid]['player'][uid]['soha'] = True
                cnt = await GetNext(bot, event, gid)
                if room[gid]['skip'] == uid:
                    room[gid]['skip'] = room[gid]['players'][room[gid]['now']]
                fail_flag = True
            else:
                await coin.modify(uid, -m)
                room[gid]['player'][uid]['soha'] = True
                room[gid]['total'] += m
                room[gid]['player'][uid]['money'] += m
                if room[gid]['player'][uid]['money'] > room[gid]['max']:
                    room[gid]['max'] = room[gid]['player'][uid]['money']
                    room[gid]['skip'] = uid
                await con.send(bot, event, "梭哈！你把你身前的%dQ全部推了出去" % m, at_sender=True)
                cnt = await GetNext(bot, event, gid)
        else:
            await con.send(bot, event, "现在不是你的回合", at_sender=True)
    elif msg[0] == '停牌':
        if room[gid]['get']:
            if room[gid]['player'][uid]['stop']:
                await con.send(bot, event, "你已经停牌了", at_sender=True)
            else:
                room[gid]['stop'] += 1
                await con.send(bot, event, "你停牌了", at_sender=True)
                room[gid]['player'][uid]['stop'] = True
                if room[gid]["stop"] == len(room[gid]['players']):
                    room[gid]['get'] = False
                    room[gid]['final'] = True
                    time.sleep(0.5)
                    await con.send(bot, event, "现在为：最后阶段")
                    time.sleep(0.5)
                    cnt = 0
                    for ii in range(len(room[gid]['players'])):
                        if room[gid]['skip'] == room[gid]['players'][ii]:
                            room[gid]['now'] = ii
                        if not room[gid]['player'][room[gid]['players'][ii]]['fail'] and not room[gid]['player'][room[gid]['players'][ii]]['soha']:
                            cnt += 1
                    if cnt > 1:
                        if room[gid]['player'][room[gid]['players'][room[gid]['now']]]['soha']:
                            cnt = await GetNext(bot, event, gid)
                        else:
                            mystr = "现在是[CQ:at,qq=%d]的回合\n现在最大注为%d" % (room[gid]['players'][room[gid]['now']], room[gid]['max'])
                            await con.send(bot, event, mystr)
        else:
            await con.send(bot, event, "非要牌阶段不能停牌", at_sender=True)
    time.sleep(0.5)
    if 0 <= cnt <= 1:
        if room[gid]['blind']:
            room[gid]['blind'] = False
            room[gid]['get'] = True
            await con.send(bot, event, "现在为：要牌阶段")
            for id in room[gid]['players']:
                mystr = "你的手牌为: " + GetName(room[gid]['player'][id]['card'][0])
                for i in range(1, len(room[gid]['player'][id]['card'])):
                    mystr += ', ' + GetName(room[gid]['player'][id]['card'][i])
                if id in friend_list:
                    await bot.call_api('send_private_msg', user_id=id, message=mystr)
                else:
                    await bot.sendTempMsg(group_id=gid, user_id=id, message=mystr)
        elif room[gid]['final']:
            mystr = "开始结算，场上剩余玩家有:"
            remain = []
            for p in room[gid]['players']:
                if not room[gid]['player'][p]['fail']:
                    remain.append(p)
                    mystr += "\n[CQ:at,qq=%d]" % p
            await con.send(bot, event, mystr)
            time.sleep(1.5)
            if len(remain) > 1:
                for id in remain:
                    mystr = '[CQ:at,qq=%d]\n' % id
                    mystr += "你的手牌为: " + GetName(room[gid]['player'][id]['card'][0])
                    for i in range(1, len(room[gid]['player'][id]['card'])):
                        mystr += ', ' + GetName(room[gid]['player'][id]['card'][i])
                    await con.send(bot, event, mystr)
                    time.sleep(1.5)
            soha = 0
            while True:
                win = GetWinner(remain, gid)
                if len(remain) == 1:
                    mystr = '这轮只剩下，一个人评奖[CQ:at,qq=%d]，将获得奖池的总共%dQ' % (win[0], room[gid]['total'])
                    await coin.modify(win[0], room[gid]['total'])
                    await con.send(bot, event, mystr)
                    break
                else:
                    flag = True
                    minn = room[gid]['max']
                    for q in win:
                        if room[gid]['player'][q]['money'] < minn:
                            minn = room[gid]['player'][q]['money']
                            flag = False
                    if flag:
                        mystr = '获胜者们为\n'
                        for q in win:
                            mystr += '[CQ:at,qq=%d]' % q
                            await coin.modify(q, room[gid]['total'] // len(win))
                        mystr += '\n每人分得%dQ' % int(room[gid]['total'] // len(win))
                        await con.send(bot, event, mystr)
                        break
                    else:
                        tot = 0
                        for q in room[gid]['players']:
                            if soha < room[gid]['player'][q]['money'] <= minn:
                                tot += room[gid]['player'][q]['money'] - soha
                            elif minn < room[gid]['player'][q]['money']:
                                tot += minn - soha
                        mystr2 = ""
                        for q in remain:
                            mystr2 += '[CQ:at,qq=%d]' % q
                        mystr = "由于有人梭哈，奖励分轮计算，这一轮的评奖人有" + mystr2 + "，获胜者们为:\n"
                        for q in win:
                            mystr += '[CQ:at,qq=%d]' % q
                            await coin.modify(q, int(tot // len(win)))
                        mystr += '\n每人分得%dQ' % int(tot // len(win))
                        await con.send(bot, event, mystr)
                        rmc = remain.copy()
                        for q in rmc:
                            if room[gid]['player'][q]['money'] <= minn:
                                remain.remove(q)
                        room[gid]['total'] -= tot
                        soha = minn
                    pass
            del room[gid]
            await g21x.finish()
    #await con.send(bot, event, "now=" + str(room[gid]['now']) + '\ncnt=%d' % cnt)
    if fail_flag:
        await g21x.finish()
    await g21x.reject()

@g21_tot.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    uid = str(event.user_id)
    await user_exmine(uid)
    mystr = "仅统计单人数据"
    mystr += '\n总共玩了%d次' % data[uid]['times']
    mystr += '\n总共赢了%d次' % data[uid]['wins']
    mystr += '\n总共投入%dQ' % data[uid]['Q_in']
    mystr += '\n总共收入%dQ' % data[uid]['Q_out']
    mystr += '\n今天玩了%d次' % data[uid]['day_times']
    mystr += '\n今天赢了%d次' % data[uid]['day_wins']
    mystr += '\n今天投入%dQ' % data[uid]['day_in']
    mystr += '\n今天收入%dQ' % data[uid]['day_out']
    await con.send(bot, event, mystr, at_sender=True)
    await g21_tot.finish()

async def user_exmine(uid: str):
    uid = str(uid)
    if not uid in data:
        data[uid] = {
            'date': -1,
            'Q_in': 0,
            'Q_out': 0,
            'times': 0,
            'wins': 0
        }
        await datax.output()
    day = int(time.strftime("%j", time.localtime(time.time())))
    if day != data[uid]['date']:
        data[uid]['date'] = day
        data[uid]['day_in'] = 0
        data[uid]['day_out'] = 0
        data[uid]['day_times'] = 0
        data[uid]['day_wins'] = 0
        await datax.output()

def GetWins(uid):
    return data[uid]['day_wins']

export = export()
export.getF = GetWins