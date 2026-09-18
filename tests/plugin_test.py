import pytest
from fake import fake_group_message_event_v11
from nonebug import App


@pytest.mark.asyncio
async def test_pip(app: App):
    import nonebot
    from nonebot.adapters.onebot.v11 import Bot, Message
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    event = fake_group_message_event_v11(message="pip install nonebot2")
    try:
        from nonebot_plugin_template import pip  # type:ignore
    except ImportError:
        pytest.skip("nonebot_plugin_template.pip not found")

    async with app.test_matcher(pip) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, Message("nonebot2"), result=None, bot=bot)
        ctx.should_finished()


def test_censor_text():
    from nonebot_plugin_onebot2tg import forwarder

    forwarder.config.onebot2tg_blocked_words = ["badword", "敏感词"]
    try:
        assert forwarder._censor_text("hello world") == "hello world"
        assert forwarder._censor_text("") == ""
        assert forwarder._censor_text("this is badword!") == "this is ****!"
        assert forwarder._censor_text("BADWORD") == "****"
        assert forwarder._censor_text("有敏感词哦") == "有****哦"
        assert forwarder._censor_text("badword和敏感词") == "****和****"
    finally:
        forwarder.config.onebot2tg_blocked_words = []


def test_censor_text_empty_config():
    from nonebot_plugin_onebot2tg import forwarder

    forwarder.config.onebot2tg_blocked_words = []
    assert forwarder._censor_text("任何内容") == "任何内容"
