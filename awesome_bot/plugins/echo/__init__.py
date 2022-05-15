from .._gb import *


echo0 = on_command('echo', permission=SUPERUSER, rule=Check_('echo'), priority=1)
echo1 = on_command('send', permission=SUPERUSER, rule=Check_('send'), priority=1)
echo2 = on_command('test', rule=Check_('test', 'group'), permission=SUPERUSER, priority=1)
echo_rick = on_command('rick', rule=Check_('rick', 'group'), priority=10)

cmds = [
'echo',
'send',
'test',
'rick'
]
con.addcmds('基础功能', cmds)

@echo0.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    mid = await con.send(bot, event, str(event.get_message()))
    if mid:
        await con.send(bot, event, 'message_id = ' + str(mid))
    await echo0.finish()

@echo1.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    mid = await con.send(bot, event, str(event.get_message()), auto_escape=True)
    if mid:
        await con.send(bot, event, 'message_id = ' + str(mid))
    await echo1.finish()

@echo2.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip().split()

    msgs = []
    # msgs.append(segement('text', text='这是一条测试信息\n'))
    # msgs.append(segement('face', id='123'))
    # msgs.append(segement('at', qq='847360401'))
    # msgs.append(segement('image', file='https://pics3.baidu.com/feed/5882b2b7d0a20cf4ce4aaa5d988e6830aeaf99ec.png'))
    msgs.append(segement('image', file=r'C:\Database\image\xp\0xa0e66ae7d673fc3e.jpg'))
    msgid = await bot.call_api('send_group_msg', message=msgs, group_id=event.group_id)
    #msgid = await con.send(bot, event, msgs)
    await con.send(bot, event, 'msg_id = %s' % msgid['message_id'])
    msg = await bot.call_api('get_msg', message_id=msgid['message_id'])
    await con.send(bot, event, 'get_msg = ' + str(msg))
    await echo2.finish()

@echo_rick.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    if '[CQ:image,' in msg:
        left = msg.index('[CQ:image,')
        right = msg.index(']', left + 5)
        urlid = msg.index(',url=', left + 5, right)
        url = msg[urlid + 5:right]
        msg = msg[:left] + msg[right+1:]
    else:
        url = 'https://gchat.qpic.cn/gchatpic_new/323690346/963370810-2433807771-5B8FC6AFD2A02A7124A6550C64ACF8C2/0?term=2'

    msg = msg.split()
    msgs = []
    if len(msg) >=1:
        title = msg[0]
    else:
        title = "球图"
    if len(msg) >=2:
        content = msg[1]
    else:
        content = "分享一些可爱的白泽球图"
    msgs.append(segement('share',
                         title=title,
                         content=content,
                         url="www.bilibili.com/video/BV1uT4y1P7CX",
                         image=url)
                )
    await bot.call_api('send_group_msg', message=msgs, group_id=event.group_id)
    await echo_rick.finish()
