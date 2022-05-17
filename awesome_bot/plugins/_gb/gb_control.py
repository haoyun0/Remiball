from .gb_database import DataList
import codecs

class Con:
    def __init__(self):
        self.command_list = []
        self.command_lists = {}
        self.help_list = {}
        self.datax = DataList('control')
        self.data = self.datax.data
    def addcmd(self, cmd : str):
        if not cmd in self.command_list:
            self.command_list.append(cmd)
    def addcmds(self, cmd: str, cmds : list):
        for i in cmds:
            self.addcmd(i)
        if not cmd in self.command_lists:
            self.command_lists[cmd] = []
        self.command_lists[cmd] += cmds
    def check(self, event, cmd : str)-> bool:
        gid = self.get_gid(event)
        if gid in self.data:
            return cmd in self.data[gid]
        else:
            return False
    def addhelp(self, name: str, state: str, ow: list=None):
        self.help_list[name]={}
        self.help_list[name]['state'] = state
        if ow:
            self.help_list[name]['ow'] = ow
    async def send(self, bot, event, message, at_sender=False, auto_escape=False) -> int:
        gid = self.get_gid(event)
        if at_sender:
            message = "[CQ:at,qq=%d] " % event.user_id + message
        #message = "DEBUG:\nmessage_type:%s\nsub_type:%s\nmsgid:%s\n" % (event.message_type, event.sub_type, event.message_id) + message
        msgid = await bot.call_api("send_msg", message_type=event.message_type, user_id=event.user_id, group_id=gid, message=message, auto_escape=auto_escape)
        return msgid['message_id']

    def get_gid(self, event):
        if event.message_type == 'group':
            return str(event.group_id)
        else:
            if event.sub_type == 'friend':
                return '19260817'  # 好友消息
            else:
                return '60481729'  # 群临时会话

    def ByteToInt(self, s:bytes):
        return s[3] + 256 * (s[2] + 256 * (s[1] + 256 * s[0]))

    async def sendNode(self, bot, event, messages: list):
        ids = []
        for message in messages:
            msgid = await bot.call_api("send_group_msg", message_type=event.message_type, group_id=146099774,
                                       message=message, auto_escape=False)
            ids.append(msgid['message_id'])
        msgs = []
        for idx in ids:
            msgs.append(segement('node', id=idx))
        await self.send(bot, event, msgs)


def segement(type: str, **kwargs):
    msg = {'type': type, 'data': kwargs}
    return msg

con = Con()