from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from . import forwarder
from .config import Config

config = get_plugin_config(Config)
forwarder.config = config

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-onebot2tg",
    description="OneBot V11 与 Telegram 双向消息转发插件",
    usage="配置 ONEBOT2TG_TARGET_CHAT_ID 和 ONEBOT2TG_OB_TARGET_GROUP_ID 即可自动转发",
    type="application",
    homepage="",
    config=Config,
    supported_adapters={
        "~onebot.v11",
        "~telegram",
    },
)
