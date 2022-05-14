from ..._gb import *

game_stone = on_command("开始取石子游戏", aliases={'开始取石子','开始 取石子游戏','开始 取石子'}, rule=Check_('开始取石子游戏'), priority=10)
game_stone_2p = on_command("开始双人取石子游戏", aliases={'开始双人取石子','开始 双人取石子游戏','开始 双人取石子'}, rule=Check_('开始双人取石子游戏', 'group'), priority=10)
game_stone2 = on_command("开始取石子游戏二", aliases={'开始取石子二','开始 取石子游戏二','开始 取石子二'}, rule=Check_('开始取石子游戏二'), priority=10)
game_stone2_2p = on_command("开始双人取石子游戏二", aliases={'开始双人取石子二','开始 双人取石子游戏二','开始 双人取石子二'}, rule=Check_('开始双人取石子游戏二', 'group'), priority=10)

cmds = [
'开始取石子游戏',
'开始双人取石子游戏',
'开始取石子游戏二',
'开始双人取石子游戏二'
]
con.addcmds('小游戏',cmds)
con.addcmds('基础功能',cmds)

con.addhelp('取石子游戏',"""
取石子游戏规则如下：
有两堆石子，两个人轮流取，取完所有石子者获胜。
每次取石子以下3种取法：
1：从第一堆石子取走其中x个
2：从第二堆石子取走其中x个
3：同时取走两堆石子各x个
命令格式 op x,op为取法的编号1~3
x最少为1，最多为剩下的石子数
""".strip(), ['双人取石子游戏'])

con.addhelp('取石子游戏二',"""
取石子游戏二规则如下：
有n堆石子(n>=3)，两个人轮流取，取完所有石子者获胜。
每人每次只能从一堆中取得x个石子：
命令格式 op x
即从第op堆中取走x颗石子。
x最少为1，最多为剩下的石子数
""".strip(), ['双人取石子游戏二'])

imp = ""
cnt = []
ans = {}
ans2 = {}
t = 0
for i in range(1,101):
    if not (i in cnt):
        t += 1
        cnt.append(i)
        cnt.append(i+t)
        ans[i] = i+t
        ans[i+t] = i
        ans2[t]= [i, i+t]
cnt.clear()

room = {}

@game_stone.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if str(event.message).strip():
        await game_stone.finish()
    stones = [random.randint(5,50), random.randint(7,50)]
    state['stones'] = stones
    await con.send(bot, event, f'游戏开始：\n现在两堆石子个数分别为：{stones[0]}, {stones[1]}')

@game_stone2.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if str(event.message).strip():
        await game_stone2.finish()
    n = 3
    while True:
        q = random.randint(0,3)
        if q:
            break;
        n += 1
    stones = []
    for i in range(n):
        stones.append(random.randint(4, 63))
    state['stones'] = stones
    state['n'] = n
    mystr = "游戏开始，有%d堆石子，石子数分别为%d" % (n, stones[0])
    for i in range(1,n):
        mystr += ",%d" % stones[i]
    await con.send(bot, event, mystr)

@game_stone_2p.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if str(event.message).strip():
        await game_stone_2p.finish()
    if event.group_id in room:
        if len(room[event.group_id]['player']) == 1:
            info = await bot.call_api("get_group_member_info",group_id=event.group_id, user_id=event.user_id)
            if info['card']:
                name = info['card']
            else:
                name = info['nickname']
            room[event.group_id]['player'].append(event.user_id)
            room[event.group_id]['name'].append(name)
            stones = [random.randint(5, 50), random.randint(7, 50)]
            room[event.group_id]['stones'] = stones
            room[event.group_id]['running'] = 1
            name = room[event.group_id]['name'][room[event.group_id]['turn']]
            await con.send(bot, event, f'游戏开始：\n现在两堆石子个数分别为：%d, %d\n%s先手' % (stones[0], stones[1], name))
        else:
            await con.send(bot, event, "房间已满")
            await game_stone_2p.finish()
    else:
        info = await bot.call_api("get_group_member_info",group_id=event.group_id, user_id=event.user_id)
        if info['card']:
            name = info['card']
        else:
            name = info['nickname']
        room[event.group_id] = {'player': [event.user_id],'stones' : [], 'running': 0, 'turn':random.randint(0,1), 'name':[name]}
        await con.send(bot, event, "本群取石子游戏房间已创建，请等待别人加入")

@game_stone.receive()
async def receive(bot: Bot, event: Event, state: T_State):
    arg = str(event.message).strip()
    if arg == '结束游戏':
        await con.send(bot, event, "已结束")
        await game_stone.finish()
    args = arg.split(' ')
    flag = True
    if len(args)==2:
        if args[0].isnumeric() and args[1].isnumeric():
            op = int(args[0])
            x = int(args[1])
            flag = False
    if flag:
        await con.send(bot, event, "格式错误，如有需要请输入结束游戏，并查看帮助")
        await game_stone.reject()
    flag = False
    stones = state['stones']
    if x <= 0:
        await con.send(bot, event, "取石子个数不符合规范")
        await game_stone.reject()
    if op==1:
        if stones[0] >= x:
            stones[0] -= x
            flag = True
    elif op==2:
        if stones[1] >= x:
            stones[1] -= x
            flag = True
    elif op==3:
        if stones[0] >= x and stones[1] >= x:
            stones[0] -= x
            stones[1] -= x
            flag = True
    else:
        await con.send(bot, event, "只有三种操作可以选择")
        await game_stone.reject()
    if not flag:
        await con.send(bot, event, "取石子个数不符合规范")
        await game_stone.reject()
    await con.send(bot, event, f"你取石子后，石子数分别为：%d, %d" % (stones[0], stones[1]))
    time.sleep(0.5)
    if stones[0] == 0 or stones[1] == 0:
        if stones[0] == 0 and stones[1] == 0:
            mystr = "恭喜你，战胜了蕾米球"
        elif stones[0] == 0:
            mystr = "蕾米球选择从第2堆石子从取走%d个\n蕾米球获胜了，请再接再厉" % (stones[1])
        elif stones[1] == 0:
            mystr = "蕾米球选择从第1堆石子从取走%d个\n蕾米球获胜了，请再接再厉" % (stones[0])
        await con.send(bot, event, mystr)
        await bot.finish()
    elif ans[stones[0]] == stones[1]:
        op = random.randint(0, 1)
        x = random.randint(1, 10)
        if stones[op] < x:
            x = 1
        stones[op] -= x
        mystr = "蕾米球选择从第%d堆石子从取走%d个\n" % (op+1, x)
    elif ans[stones[0]] < stones[1]:
        k = stones[1] - ans[stones[0]]
        stones[1] = ans[stones[0]]
        mystr = "蕾米球选择从第2堆石子从取走%d个\n" % k
    elif ans[stones[1]] < stones[0]:
        k = stones[0] - ans[stones[1]]
        stones[0] = ans[stones[1]]
        mystr = "蕾米球选择从第1堆石子从取走%d个\n" % k
    else:
        y = abs(stones[0] - stones[1])
        if y == 0:
            await con.send(bot, event, "蕾米球选择从两堆石子同时取走%d个\n蕾米球获胜了，请再接再厉" % (stones[0]))
            await game_stone.finish()
        if stones[0] >stones[1]:
            k = stones[0] - ans2[y][1]
        else:
            k = stones[0] - ans2[y][0]
        mystr = "蕾米球选择从两堆堆石子同时取走%d个\n" % k
        stones[0] -= k
        stones[1] -= k
    mystr += "蕾米球取石子后，石子数分别为：%d, %d" % (stones[0], stones[1])
    await con.send(bot, event, mystr)
    await game_stone.reject()

@game_stone2.receive()
async def receive(bot: Bot, event: Event, state: T_State):
    arg = str(event.message).strip()
    if arg == '结束游戏':
        await con.send(bot, event, "已结束")
        await game_stone2.finish()
    args = arg.split(' ')
    flag = True
    if len(args)==2:
        if args[0].isnumeric() and args[1].isnumeric():
            op = int(args[0])
            x = int(args[1])
            flag = False
    if flag:
        await con.send(bot, event, "格式错误，如有需要请输入结束游戏，并查看帮助")
        await game_stone2.reject()
    n = state['n']
    if op <=0 or op >n:
        await con.send(bot, event, "只有%d堆石子可以选择" % n)
        await game_stone2.reject()
    stones = state['stones']
    if x==0 or stones[op-1] < x:
        await con.send(bot, event, "取石子个数不符合规范")
        await game_stone2.reject()
    stones[op-1] -= x
    mystr = "你取石子后，剩下的石子数分别为%d" % stones[0]
    for i in range(1,n):
        mystr += ",%d" % stones[i]
    await con.send(bot, event, mystr)
    time.sleep(0.5)
    flag = True
    for i in range(n):
        if stones[i] != 0:
            flag = False
            break
    if flag:
        await con.send(bot, event, "恭喜您，战胜了蕾米球")
        await game_stone2.finish()
    tot = 0
    for i in range(n):
        tot ^= stones[i]
    flag = False
    mystr = ""
    for i in range(n):
        k = tot ^ stones[i]
        if k < stones[i]:
            flag = True
            mystr += "蕾米球选择从第%d堆石子中取走%d个\n" % (i+1, stones[i]-k)
            stones[i] = k
            break
    if not flag:
        while True:
            j = random.randint(0,n-1)
            if stones[j]>0:
                break
        k = random.randint(1, stones[j])
        mystr += "蕾米球选择从第%d堆石子中取走%d个\n" % (j+1, k)
        stones[j] -= k

    flag = True
    for i in range(n):
        if stones[i] != 0:
            flag = False
            break
    if flag:
        mystr += "蕾米球获胜了，请再接再厉"
        await con.send(bot, event, mystr)
        await game_stone2.finish()
    mystr += "剩下的石子数分别为%d" % stones[0]
    for i in range(1,n):
        mystr += ",%d" % stones[i]
    await con.send(bot, event, mystr)
    await game_stone2.reject()

@game_stone_2p.receive()
async def receive(bot: Bot, event: Event, state: T_State):
    arg = str(event.message).strip()
    #await con.send(bot, event, str(room))
    if arg == '结束游戏':
        if event.group_id in room:
            del room[event.group_id]
        await con.send(bot, event, "已结束")
        await game_stone_2p.finish()
    if not event.group_id in room:
        await game_stone_2p.finish()
    if not event.user_id in room[event.group_id]['player']:
        await game_stone_2p.finish()
    if not room[event.group_id]['running']:
        await game_stone_2p.reject()
    player = int(event.user_id == room[event.group_id]['player'][1])
    if room[event.group_id]['turn'] != player:
        await con.send(bot, event, "现在不是你的回合，请等待%s行动" % room[event.group_id]['name'][1-player])
        await game_stone_2p.reject()
    args = arg.split(' ')
    flag = True
    if len(args)==2:
        if args[0].isnumeric() and args[1].isnumeric():
            op = int(args[0])
            x = int(args[1])
            flag = False
    if flag:
        await con.send(bot, event, "格式错误，如有需要请输入结束游戏，并查看帮助")
        await game_stone_2p.reject()
    stones = room[event.group_id]['stones']
    if x <= 0:
        await con.send(bot, event, "取石子个数不符合规范")
        await game_stone_2p.reject()
    if op==1:
        if stones[0] >= x:
            stones[0] -= x
            flag = True
    elif op==2:
        if stones[1] >= x:
            stones[1] -= x
            flag = True
    elif op==3:
        if stones[0] >= x and stones[1] >= x:
            stones[0] -= x
            stones[1] -= x
            flag = True
    else:
        await con.send(bot, event, "只有三种操作可以选择")
        await game_stone_2p.reject()
    if not flag:
        await con.send(bot, event, "取石子个数不符合规范")
        await game_stone_2p.reject()
    await con.send(bot, event, "%s取石子后，石子数分别为：%d, %d" % (room[event.group_id]['name'][player], stones[0], stones[1]))
    if stones[0]==0 and stones[1] ==0:
        time.sleep(0.5)
        await con.send(bot, event, "玩家%s获胜" % room[event.group_id]['name'][player])
        del room[event.group_id]
        await game_stone_2p.finish()
    room[event.group_id]['turn'] = 1 - room[event.group_id]['turn']
    await game_stone_2p.reject()