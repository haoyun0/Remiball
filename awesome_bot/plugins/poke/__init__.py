from nonebot import on_notice
from ..rndimage import get_image
from .._gb import *

datax = DataList('poke')
data = datax.data

poke = on_notice(priority=10)
poke_switch = on_command("拍一拍", rule=Check_('拍一拍', 'group'), permission=SUPERUSER, priority=2)

cmds = [
"拍一拍"
]

con.addcmds('基础功能', cmds)
con.addcmds('拍一拍', cmds)

spell_card = ['天罚「Star of David」', '神罚「年幼的恶魔之王」', '冥符「红色的冥界」\t', '狱符「千根针的针山」', '诅咒「弗拉德·特佩斯的诅咒」', '神术「吸血鬼幻想」', '红符「Scarlet Shoot」', '红符「Scarlet Meister」', '「Red Magic」', '「红色的幻想乡」', '红符「红色不夜城」', '红魔「Scarlet Devil」', '必杀「Heart Break」', '神枪「Spear the Gungnir」', '夜符「Demon King Cradle」', '夜王「Dracula Cradle」', '夜符「Bad Lady Scramble」', '符之二「My Heart Break」', '符之三「Hell Catastrophe」', '夜符「Queen of Midnight」', '「Scarlet Destiny」', '魔符「全世界梦魇」', '红符「Bloody Magic Square」', '红蝙蝠「Vampirish Night」', '神鬼「Remilia Stalker」', '命运「Miserable Fate」', '夜符「Bombard Night」', '蝙蝠「Vampire Sweep」', '恶魔「Remilia Stretch」', '「千年吸血鬼」', '「Fitful Nightmare」', '「捉吸血鬼游戏」', '红魔符「Bloody Catastrophe」', '红星符「超人血刀」', '神红符「血腥十七条的光芒」']

def examine(gid):
    if gid:
        if gid in data['ban']:
            return False
    return True


@poke.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    if event.notice_type == 'notify':
        if event.sub_type == 'poke':
            if examine(event.group_id):
                if event.target_id == event.self_id:
                    if event.group_id:
                        await bot.send_group_msg(group_id = event.group_id, message = get_image('球'))
                    else:
                        await bot.send_private_msg(user_id = event.user_id, message=get_image("球"))
                if event.target_id == 323690346:
                    await bot.send_group_msg(group_id = event.group_id, message = random.choice(spell_card))
    await poke.finish()


@poke_switch.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    gid = event.group_id
    if gid in data['ban']:
        data['ban'].remove(gid)
        await con.send(bot, event, '本群拍一拍效果已开启')
    else:
        data['ban'].append(gid)
        await con.send(bot, event, '本群拍一拍效果已关闭')
    await datax.output()
    await poke_switch.finish()