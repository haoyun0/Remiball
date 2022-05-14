from .._gb import *
import codecs

encode = on_command('蕾米语加密', aliases={'蕾咪语加密'}, rule=Check_('蕾米语加密'), priority=10)
decode = on_command('蕾米语解密', aliases={'蕾咪语解密'}, rule=Check_('蕾米语解密'), priority=10)
encode_b64 = on_command('base64加密', aliases={'b64加密'}, rule=Check_('base64加密'), priority=10)
decode_b64 = on_command('base64解密', aliases={'b64解密'}, rule=Check_('base64解密'), priority=10)
code = [
'蕾米',
'蕾咪',
'蕾眯',
'蕾迷',
'蕾洣',
'蕾侎',
'蕾詸',
'蕾銤',
'蕾冞',

'雷米',
'雷咪',
'雷眯',
'雷迷',
'雷洣',
'雷侎',
'雷詸',
'雷銤',
'雷冞',

'镭米',
'镭咪',
'镭眯',
'镭迷',
'镭洣',
'镭侎',
'镭詸',
'镭銤',
'镭冞',

'擂米',
'擂咪',
'擂眯',
'擂迷',
'擂洣',
'擂侎',
'擂詸',
'擂銤',
'擂冞',

'檑米',
'檑咪',
'檑眯',
'檑迷',
'檑洣',
'檑侎',
'檑詸',
'檑銤',
'檑冞',

'鐳米',
'鐳咪',
'鐳眯',
'鐳迷',
'鐳洣',
'鐳侎',
'鐳詸',
'鐳銤',
'鐳冞',

'鱩米',
'鱩咪',
'鱩眯',
'鱩迷',
'鱩洣',
'鱩侎',
'鱩詸',
'鱩銤',
'鱩冞',

'蕾姆'
]
ans = ''
ans2 = []

cmds = [
'蕾米语加密',
'蕾米语解密',
'base64加密',
'base64解密'
]
con.addcmds("蕾米语", cmds)
con.addcmds("基础功能", cmds)
con.addhelp("蕾米语","""
蕾米语为扫地机借鉴base64加密法改造的一种加密方式(图一乐)
指令：
蕾米语加密 [明文]
蕾米语解密 [密文]
base64加密 [明文]
base64解密 [密文]
""".strip(),["蕾咪语","蕾米语加密","蕾米语解密"])

    
@encode.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        if len(args)<=300:
            encode(args)
            await con.send(bot, event, ans)
        else:
            await con.send(bot, event, "密文过长")

@decode.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        if len(args)<=1000:
            l = len(args)
            if l%8 == 0:
                decode(args, l) 
                ans = bytes(ans2).decode()
                if check(ans):
                    await con.send(bot, event, ans)
                else:
                    await con.send(bot, event, "非法的蕾米语")
            else:
                await con.send(bot, event, "非法的蕾米语")
        else:
            await con.send(bot, event, "密文过长")

@encode_b64.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        s0 = args.encode()
        s1 = codecs.encode(s0, 'base64')
        s2 = str(s1)
        await con.send(bot, event, s2[2:-3])
    else:
        await con.send(bot, event, "明文为空")
    await encode_b64.finish()

@decode_b64.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        try:
            s0 = args.encode()
            s1 = codecs.decode(s0, 'base64')
            s2 = s1.decode()
            await con.send(bot, event, s2)
        except:
            await con.send(bot, event, "密文错误")
    else:
        await con.send(bot, event, "密文为空")
    await encode_b64.finish()

def encoding(a: list):
    global ans
    b = [0,0,0,0]
    b[0] = a[2] // 4
    b[1] = a[2] % 4 * 16 + a[1] // 16
    b[2] = a[1] % 16 * 4 + a[0] // 64
    b[3] = a[0] % 64
    for i in range(4):
        ans += code[b[i]]
        
def encode(mystr2):
    global ans
    ans = ""
    mystr = mystr2.encode()
    tot = 0
    a = [0,0,0]
    for i in mystr:
        print(i)
        a[2-tot] = i
        tot += 1
        if tot == 3:
            encoding(a)            
            tot = 0
    if tot>0:
        while tot<3:
            a[2-tot] = 0
            tot += 1
        encoding(a)

def decoding(a: list):
    global ans2
    b = [0,0,0]
    b[0] = a[2] % 4 * 64 + a[3]
    b[1] = a[1] % 16 * 16 + a[2] // 4
    b[2] = a[0] * 4 + a[1] // 16
    for i in range(0,3):
        if b[2 - i]>0:
            ans2.append(b[2-i])

def decode(mystr : str, l : int):
    global ans2
    ans2 = []
    tot = 0
    a = [0,0,0,0]
    i = 0
    while i<l:
        a[tot] = code.index(mystr[i:i+2])
        tot += 1
        if tot == 4:
            decoding(a)            
            tot = 0
        i += 2



def check(s: str) -> bool:
    return True