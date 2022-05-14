from pydantic import BaseSettings

class Config(BaseSettings):

    # plugin custom config
    plugin_setting: str = "default"
    SUPERUSERS=["847360401", "2720673792", "323690346"]
    ban = {
        738721109: {
            'cmd_head': ['!'],
            'user': [3056318700]
        }
    }
    #cmd_head, user
    class Config():
        extra = "ignore"
