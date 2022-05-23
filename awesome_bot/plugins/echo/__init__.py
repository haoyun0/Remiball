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
    #msgs.append(segement('text', text='这是一条测试消息'))
    # msgid = await bot.call_api('send_group_msg', message='这是一条测试消息1', group_id=event.group_id)
    # msgid2 = await bot.call_api('send_group_msg', message='这是一条测试消息2', group_id=event.group_id)
    # msgs2 = []
    # msgs2.append(segement('node', id=msgid['message_id']))
    # msgs2.append(segement('node', id=msgid2['message_id'], nickname='球', user_id='847360401'))
    # msgid3 = await con.send(bot, event, msgs2)
    # await con.send(bot, event, 'msg3 = %s' % str(msgid3))
    await con.sendNode(bot, event, ['测试消息1', '测试消息2'])
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
    if len(msg) >=3:
        url2 = msg[2]
    else:
        url2 = "vdse.bdstatic.com//192d9a98d782d9c74c96f09db9378d93.mp4"
    msgs.append(segement('share',
                         title=title,
                         content=content,
                         url=url2,
                         image=url)
                )
    await bot.call_api('send_group_msg', message=msgs, group_id=event.group_id)
    await echo_rick.finish()
