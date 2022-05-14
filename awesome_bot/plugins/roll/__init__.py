from .._gb import *

roll = on_command("roll", aliases={"骰子"}, rule=Check_('roll'), priority=5)

cmds = ['roll']
con.addcmds('基础功能',cmds)
con.addcmds('骰子',cmds)

con.addhelp("骰子","""
使用方法：roll xdy(+/-z)
投掷y面骰子x次，并返回骰子数值总合，附加值+/-z
""".strip(),['roll'])

@roll.handle()
async def handle_roll(bot: Bot, event: Event, state: T_State):
    if not con.check(event, 'roll'):
        return
    args = str(event.get_message()).strip()
    if args:
        flag = False
        flag2 = False
        flag3 = False
        a = args.split('d')
        if len(a) == 2:
            b = a[1].split('+')
            c = a[1].split('-')
            if len(b) == 2:
                flag2 = True
                a[1] = b[0]
            if len(c) == 2:
                flag3 = True
                a[1] = c[0]
            if a[0].isnumeric() and a[1].isnumeric():
                flag = True
                if flag2:
                    if b[1].isnumeric():
                        z = int(b[1])
                    else:
                        flag = False
                if flag3:
                    if c[1].isnumeric():
                        z = -int(c[1])
                    else:
                        flag = False
                x = int(a[1])
                y = int(a[0])
        if flag:
            if x>19260817:
                await bot.send(event, "您输入的骰子面太大了，超过了某8位大质数！")
            elif x<=0:
                await bot.send(event, "骰子至少要有1面*愤怒*！")
            elif y>514:
                await bot.send(event, "投掷次数太多了，最多投掷514次！")
            elif y<=0:
                await bot.send(event, "至少投一次才有结果吧QAQ！")
            else:
                sumq = await get_number(x, y)
                if flag2 or flag3:
                    sumq += z
                await bot.send(event, str(sumq))
        else:
            await bot.send(event, "命令格式错误，请输入帮助骰子查看帮助")
    else:
        await bot.send(event, "命令格式错误，请输入帮助骰子查看帮助")

async def get_number(x: int, y: int):
    sumq = 0
    for i in range(0,y):
        sumq+=random.randint(1, x)
    return sumq

