from pydantic import BaseModel


class Config(BaseModel):
    """插件配置"""

    # 模式开关
    onebot2tg_enable_bridge: bool = True
    """开启互通模式（双向转发，需配置互通群号，默认开启）"""

    onebot2tg_enable_forward: bool = False
    """开启转发模式（QQ所有消息单向转发到TG私聊）"""

    # 互通模式配置（一对一）
    onebot2tg_bridge_group_id: str | int = ""
    """互通模式下，要互通的QQ群号"""

    onebot2tg_bridge_tg_chat_id: str | int = ""
    """互通模式下，TG对应的chat_id（群或频道）"""

    # 转发模式配置
    onebot2tg_forward_target_chat_id: str | int = ""
    """转发模式下，QQ消息转发到TG的目标chat_id（私聊或群）"""

    # 转发模式黑白名单
    onebot2tg_forward_filter_mode: str = "none"
    """转发模式过滤方式：none（不过滤，默认）、blacklist（黑名单）、whitelist（白名单）"""

    onebot2tg_forward_filter_list: list[str | int] = []
    """转发模式过滤列表：QQ号或群号列表。黑名单模式下不转发这些来源的消息；白名单模式下只转发这些来源的消息"""
