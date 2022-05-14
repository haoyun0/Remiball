from .._gb import *

sol_24 = on_command("24点", rule=Check_("24点"), priority=5)


cmds = [
'24点'
]
con.addcmds('24点',cmds)
con.addcmds('基础功能',cmds)
con.addhelp('24点',"""
计算24点，并给出随机一组解
注：24点的点数规则是4个1 ~ 10的数
指令:
24点 a b c d
""".strip())

n = 4
m = 24
a = []
b = []
c = []
p = []
ac = ['+','-','*','/']
ans = []
for i in range(n):
    b.append(0)
    p.append(0)
    c.append(0)

@sol_24.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    global a, ans
    a = args.split()
    flag = 0
    if len(a)==4:
        for i in range(4):
            ww = int(a[i])
            if 1 <= ww <= 13:
                pass
            else:
                flag = 1
    else:
        flag = 1
    if flag:
        await con.send(bot, event, "参数错误")
        return
    ans = []
    dfs1(0)
    l = len(ans)
    if l:
        mystr = ans[random.randint(0,l-1)]
    else:
        mystr = args + " 无解"
    await con.send(bot, event, mystr)
    await sol_24.finish()

def cnt(x,y,k) -> float:
    if k==0:
        return x+y
    elif k==1:
        return x-y
    elif k==2:
        return x*y
    elif k==3:
        if y==0:
            return 19260817
        else:
            return x/y

def eps(x,y):
    return abs(x-y)<=1e-6

def test():
    global b, c, m, n
    if n==4:
        #ans.append(f"{b[0]}{ac[c[0]]}{b[1]}{ac[c[1]]}{b[2]}{ac[c[2]]}{b[3]} = {m}")
        #((01)2)3
        x = cnt(b[0], b[1], c[0])
        x = cnt(x, b[2], c[1])
        y = cnt(x, b[3], c[2])
        if eps(y,m):
            ans.append(f"(({b[0]}{ac[c[0]]}{b[1]}){ac[c[1]]}{b[2]}){ac[c[2]]}{b[3]} = {m}")
        #(0(12))3
        y = cnt(b[1], b[2], c[1])
        x = cnt(b[0], y, c[0])
        y = cnt(x, b[3], c[2])
        if eps(y,m):
            ans.append(f"({b[0]}{ac[c[0]]}({b[1]}{ac[c[1]]}{b[2]})){ac[c[2]]}{b[3]} = {m}")
        #(01)(23)
        x = cnt(b[0], b[1], c[0])
        y = cnt(b[2], b[3], c[2])
        y = cnt(x, y, c[1])
        if eps(y,m):
            ans.append(f"({b[0]}{ac[c[0]]}{b[1]}){ac[c[1]]}({b[2]}{ac[c[2]]}{b[3]}) = {m}")
        #0(1(23))
        x = cnt(b[2], b[3], c[2])
        x = cnt(b[1], x, c[1])
        y = cnt(b[0], x, c[0])
        if eps(y,m):
            ans.append(f"{b[0]}{ac[c[0]]}({b[1]}{ac[c[1]]}({b[2]}{ac[c[2]]}{b[3]})) = {m}")
        #0((12)3)
        x = cnt(b[1], b[2], c[1])
        x = cnt(x, b[3], c[2])
        y = cnt(b[0], x, c[0])
        if eps(y,m):
            ans.append(f"{b[0]}{ac[c[0]]}(({b[1]}{ac[c[1]]}{b[2]}){ac[c[2]]}{b[3]}) = {m}")


def dfs2(k):
    global c
    for i in range(4):
        c[k] = i
        if k == n-2:
            test()
        else:
            dfs2(k+1)

def dfs1(k):
    global a, b, p
    for i in range(n):
        if p[i]==0:
            p[i] = 1
            b[k] = a[i]
            if k == n-1:
                dfs2(0)
            else:
                dfs1(k+1)
            p[i] = 0