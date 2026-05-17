from __future__ import annotations

from nonebot import logger, get_adapter
from nonebot.rule import is_type
from nonebot.drivers import Request
from nonebot.plugin.on import on_command, on_message
from nonebot.adapters.telegram import Bot as TGBot
from nonebot.adapters.onebot.v11 import (
    Bot as OB11Bot,
)
from nonebot.adapters.onebot.v11 import (
    Message as OB11Message,
)
from nonebot.adapters.onebot.v11 import (
    MessageEvent as OB11MessageEvent,
)
from nonebot.adapters.onebot.v11 import (
    MessageSegment as OB11Segment,
)
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent as OB11GroupMessageEvent,
)
from nonebot.adapters.onebot.v11 import (
    PrivateMessageEvent as OB11PrivateMessageEvent,
)
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent
from nonebot.adapters.telegram.message import (
    File,
    Entity,
)
from nonebot.adapters.telegram.message import (
    Message as TGMessage,
)

from .config import Config

config: Config

# 运行时临时开关（重启后失效）
_bridge_tg_to_qq_paused: bool = False
_bridge_qq_to_tg_paused: bool = False


async def get_tg_bot() -> TGBot | None:
    try:
        adapter = get_adapter("Telegram")
        for bot in adapter.bots.values():
            if isinstance(bot, TGBot):
                return bot
    except Exception as e:
        logger.warning(f"获取 Telegram Bot 失败: {e}")
    return None


async def get_ob11_bot() -> OB11Bot | None:
    try:
        adapter = get_adapter("OneBot V11")
        for bot in adapter.bots.values():
            if isinstance(bot, OB11Bot):
                return bot
    except Exception as e:
        logger.warning(f"获取 OneBot V11 Bot 失败: {e}")
    return None


def _ob11_display_name(event: OB11MessageEvent) -> str:
    sender = event.sender
    return sender.card or sender.nickname or event.get_user_id()


def _tg_display_name(event: TGMessageEvent) -> str:
    user = getattr(event, "from_", None)
    if user:
        return user.username or user.first_name or event.get_user_id()
    return event.get_user_id()


# ============================================================
#  下载 TG 文件（走代理）
# ============================================================
async def _download_tg_file(tg_bot: TGBot, file_id: str) -> bytes | None:
    """通过代理下载 TG 文件"""
    try:
        file_info = await tg_bot.get_file(file_id=file_id)
        if not file_info.file_path:
            return None
        api_server = tg_bot.bot_config.api_server.rstrip("/")
        url = f"{api_server}/file/bot{tg_bot.bot_config.token}/{file_info.file_path}"
        adapter = tg_bot.adapter
        proxy = getattr(adapter, "adapter_config", None)
        proxy_url = proxy.proxy if proxy else None
        request = Request("GET", url, proxy=proxy_url)
        response = await adapter.request(request)
        if response.status_code == 200 and response.content:
            content = response.content
            if isinstance(content, str):
                return content.encode("utf-8")
            return content
        logger.warning(f"下载 TG 文件失败，状态码: {response.status_code}")
        return None
    except Exception as e:
        logger.warning(f"下载 TG 文件失败: {e}")
        return None


# ============================================================
#  TG Message → OneBot V11 Message
# ============================================================
async def _tg_message_to_ob11(tg_bot: TGBot, event: TGMessageEvent) -> OB11Message:
    segments: list[OB11Segment] = []

    for seg in event.get_message():
        if seg.type == "text":
            segments.append(OB11Segment.text(seg.data.get("text", "")))
        elif seg.type == "photo":
            file_id = seg.data.get("file", "")
            if file_id:
                data = await _download_tg_file(tg_bot, file_id)
                if data:
                    segments.append(OB11Segment.image(data))
                else:
                    segments.append(OB11Segment.text("[图片]"))
            else:
                segments.append(OB11Segment.text("[图片]"))
        elif seg.type == "sticker":
            file_id = seg.data.get("file", "")
            if file_id:
                data = await _download_tg_file(tg_bot, file_id)
                if data:
                    segments.append(OB11Segment.image(data))
                else:
                    segments.append(OB11Segment.text("[贴纸]"))
            else:
                segments.append(OB11Segment.text("[贴纸]"))
        elif seg.type == "animation":
            segments.append(OB11Segment.text("[动图]"))
        elif seg.type == "document":
            segments.append(OB11Segment.text("[文件]"))
        elif seg.type == "video":
            segments.append(OB11Segment.text("[视频]"))
        elif seg.type == "voice":
            segments.append(OB11Segment.text("[语音]"))
        else:
            segments.append(OB11Segment.text(f"[{seg.type}]"))

    return OB11Message(segments)


# ============================================================
#  OneBot V11 Message → TG Message
# ============================================================
async def _ob11_message_to_tg(
    bot: OB11Bot, event: OB11MessageEvent
) -> tuple[str, list]:
    caption_parts: list[str] = []
    file_segments: list = []

    for seg in event.get_message():
        if seg.type == "text":
            caption_parts.append(seg.data.get("text", ""))
        elif seg.type == "image":
            try:
                file_info = await bot.get_image(file=seg.data.get("file", ""))
                url = file_info.get("url", "")
                if url:
                    file_segments.append(File.photo(url))
                else:
                    caption_parts.append("[图片]")
            except Exception as e:
                logger.warning(f"获取图片失败: {e}")
                caption_parts.append("[图片]")
        elif seg.type == "face":
            caption_parts.append(f"[表情:{seg.data.get('id', '')}]")
        elif seg.type == "at":
            at_qq = seg.data.get("qq", "")
            at_name = at_qq
            try:
                stranger_info = await bot.get_stranger_info(user_id=int(at_qq))
                at_name = stranger_info.get("nickname", at_qq)
            except Exception:
                pass
            caption_parts.append(f"@{at_name}")
        elif seg.type == "reply":
            pass
        else:
            caption_parts.append(f"[{seg.type}]")

    return "".join(caption_parts), file_segments


async def _send_to_tg(
    tg_bot: TGBot,
    chat_id: str | int,
    display_name: str,
    caption: str,
    file_segments: list,
    mode: str,
):
    if file_segments:
        first_seg = file_segments[0]
        full_caption = f"{display_name}:\n{caption}" if caption else f"{display_name}:"

        if len(file_segments) == 1:
            try:
                await tg_bot.send_to(
                    chat_id=chat_id,
                    message=TGMessage([first_seg])
                    + TGMessage([Entity.text(full_caption)]),
                )
            except Exception as e:
                logger.error(f"[{mode}] 发送图片到 TG 失败: {e}")
        else:
            try:
                await tg_bot.send_to(
                    chat_id=chat_id,
                    message=TGMessage([first_seg])
                    + TGMessage([Entity.text(full_caption)]),
                )
                for seg in file_segments[1:]:
                    await tg_bot.send_to(chat_id=chat_id, message=seg)
            except Exception as e:
                logger.error(f"[{mode}] 发送多张图片到 TG 失败: {e}")
    else:
        text = f"{display_name}:\n{caption}"
        try:
            await tg_bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            logger.error(f"[{mode}] 发送文本到 TG 失败: {e}")


# ============================================================
#  TG 命令：/ruler 临时关闭 TG → QQ
# ============================================================
tg_ruler = on_command("ruler", rule=is_type(TGMessageEvent), aliases={"Ruler"})


@tg_ruler.handle()
async def handle_tg_ruler(event: TGMessageEvent):
    global _bridge_tg_to_qq_paused
    if not config.onebot2tg_enable_bridge:
        return
    chat_id = str(event.chat.id) if hasattr(event, "chat") else ""
    if chat_id != str(config.onebot2tg_bridge_tg_chat_id):
        return
    _bridge_tg_to_qq_paused = not _bridge_tg_to_qq_paused
    tg_bot = await get_tg_bot()
    if tg_bot is not None:
        if _bridge_tg_to_qq_paused:
            await tg_bot.send_message(
                chat_id=chat_id, text="乳了！已临时关闭 TG→QQ 转发"
            )
        else:
            await tg_bot.send_message(chat_id=chat_id, text="已恢复 TG→QQ 转发")


# ============================================================
#  QQ 命令：/sese 临时关闭 QQ → TG
# ============================================================
ob_sese = on_command("sese", rule=is_type(OB11MessageEvent), aliases={"Sese"})


@ob_sese.handle()
async def handle_ob_sese(event: OB11MessageEvent):
    global _bridge_qq_to_tg_paused
    if not config.onebot2tg_enable_bridge:
        return
    is_group = isinstance(event, OB11GroupMessageEvent)
    group_id = str(event.group_id) if is_group else ""
    if is_group and group_id != str(config.onebot2tg_bridge_group_id):
        return
    _bridge_qq_to_tg_paused = not _bridge_qq_to_tg_paused
    ob11_bot = await get_ob11_bot()
    if ob11_bot is not None:
        if _bridge_qq_to_tg_paused:
            msg = OB11Message([OB11Segment.text("涩涩时间！已临时关闭 QQ→TG 转发")])
        else:
            msg = OB11Message([OB11Segment.text("已恢复 QQ→TG 转发")])
        if is_group:
            await ob11_bot.send_group_msg(group_id=event.group_id, message=msg)
        else:
            await ob11_bot.send_private_msg(user_id=event.user_id, message=msg)


# ============================================================
#  TG 消息处理器（仅互通模式）
# ============================================================
tg_msg = on_message(rule=is_type(TGMessageEvent))


@tg_msg.handle()
async def handle_tg_message(event: TGMessageEvent):
    if not config.onebot2tg_enable_bridge:
        return
    if _bridge_tg_to_qq_paused:
        return
    if not config.onebot2tg_bridge_group_id:
        return

    chat_id = str(event.chat.id) if hasattr(event, "chat") else ""
    if chat_id != str(config.onebot2tg_bridge_tg_chat_id):
        return

    tg_bot = await get_tg_bot()
    if tg_bot is None:
        return

    ob11_bot = await get_ob11_bot()
    if ob11_bot is None:
        return

    display_name = _tg_display_name(event)
    ob11_msg = await _tg_message_to_ob11(tg_bot, event)
    prefix = OB11Segment.text(f"{display_name}:\n")
    final_msg = OB11Message([prefix]) + ob11_msg

    try:
        await ob11_bot.send_group_msg(
            group_id=int(config.onebot2tg_bridge_group_id),
            message=final_msg,
        )
        logger.debug("[互通] 已转发 TG 消息到 QQ群")
    except Exception as e:
        logger.error(f"[互通] 转发 TG 消息到 QQ群失败: {e}")


# ============================================================
#  OneBot 消息处理器（互通 + 转发模式）
# ============================================================
ob11_msg = on_message(rule=is_type(OB11MessageEvent))


@ob11_msg.handle()
async def handle_ob11_message(event: OB11MessageEvent):
    tg_bot = await get_tg_bot()
    if tg_bot is None:
        return

    ob11_bot = await get_ob11_bot()
    if ob11_bot is None:
        return

    is_group = isinstance(event, OB11GroupMessageEvent)
    group_id = str(event.group_id) if is_group else ""
    display_name = _ob11_display_name(event)

    # ---------- 互通模式 ----------
    if config.onebot2tg_enable_bridge and config.onebot2tg_bridge_tg_chat_id:
        if is_group and group_id == str(config.onebot2tg_bridge_group_id):
            if not _bridge_qq_to_tg_paused:
                caption, file_segments = await _ob11_message_to_tg(ob11_bot, event)
                await _send_to_tg(
                    tg_bot,
                    config.onebot2tg_bridge_tg_chat_id,
                    display_name,
                    caption,
                    file_segments,
                    "互通",
                )
            return

    # ---------- 转发模式（QQ → TG 单向） ----------
    if config.onebot2tg_enable_forward and config.onebot2tg_forward_target_chat_id:
        user_id = str(event.user_id)

        # 黑白名单过滤
        filter_mode = str(config.onebot2tg_forward_filter_mode).lower()
        filter_set = {str(x) for x in config.onebot2tg_forward_filter_list}
        if filter_mode == "blacklist":
            if user_id in filter_set or (is_group and group_id in filter_set):
                return
        elif filter_mode == "whitelist":
            if user_id not in filter_set and not (is_group and group_id in filter_set):
                return

        if is_group:
            group_name = ""
            try:
                group_info = await ob11_bot.get_group_info(group_id=event.group_id)
                group_name = group_info.get("group_name", "")
            except Exception as e:
                logger.warning(f"获取群信息失败: {e}")
            source = f"[群:{group_name or event.group_id}] {display_name}"
        elif isinstance(event, OB11PrivateMessageEvent):
            source = f"[私聊] {display_name}"
        else:
            source = f"[QQ] {display_name}"

        caption, file_segments = await _ob11_message_to_tg(ob11_bot, event)
        await _send_to_tg(
            tg_bot,
            config.onebot2tg_forward_target_chat_id,
            source,
            caption,
            file_segments,
            "转发",
        )
