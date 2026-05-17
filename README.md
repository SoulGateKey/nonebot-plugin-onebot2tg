# nonebot-plugin-onebot2tg

> OneBot V11 与 Telegram 双向消息转发插件

## 功能

- **互通模式**：指定一个 QQ 群与一个 Telegram 群/频道双向互通，消息实时同步
- **转发模式**：将 QQ 消息统一转发到 Telegram，并支持在 Telegram 私聊中回复到指定 QQ 群
- **消息类型支持**：文本、图片、表情、@、贴纸等常见消息类型

## 安装

```bash
nb plugin install nonebot-plugin-onebot2tg
```

或手动安装：

```bash
pip install nonebot-plugin-onebot2tg
```

## 依赖适配器

- [nonebot-adapter-onebot](https://github.com/nonebot/adapter-onebot) (OneBot V11)
- [nonebot-adapter-telegram](https://github.com/nonebot/adapter-telegram) (Telegram)

## 配置

在 `.env` 文件中添加以下配置项：

### 模式开关

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `ONEBOT2TG_ENABLE_BRIDGE` | `bool` | `False` | 开启互通模式（双向转发，需配置互通群号） |
| `ONEBOT2TG_ENABLE_FORWARD` | `bool` | `True` | 开启转发模式（QQ 所有消息转发到 TG 私聊，默认开启） |

### 互通模式配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `ONEBOT2TG_BRIDGE_GROUP_ID` | `str \| int` | `""` | 互通模式下，要互通的 QQ 群号 |
| `ONEBOT2TG_BRIDGE_TG_CHAT_ID` | `str \| int` | `""` | 互通模式下，TG 对应的 chat_id（群或频道） |

### 转发模式配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `ONEBOT2TG_FORWARD_TARGET_CHAT_ID` | `str \| int` | `""` | 转发模式下，QQ 消息转发到 TG 的目标 chat_id（私聊或群） |
| `ONEBOT2TG_FORWARD_REPLY_CHAT_ID` | `str \| int` | `""` | 转发模式下，TG 私聊消息回复到 QQ 的目标群号 |

## 使用示例

### 场景 1：QQ 群与 Telegram 群互通

```env
ONEBOT2TG_ENABLE_BRIDGE=true
ONEBOT2TG_BRIDGE_GROUP_ID=123456789
ONEBOT2TG_BRIDGE_TG_CHAT_ID=-1001234567890
```

配置后，该 QQ 群与 Telegram 群的消息会实时双向同步。

### 场景 2：QQ 消息转发到 Telegram

```env
ONEBOT2TG_ENABLE_FORWARD=true
ONEBOT2TG_FORWARD_TARGET_CHAT_ID=123456789
ONEBOT2TG_FORWARD_REPLY_CHAT_ID=987654321
```

配置后：
- QQ 群/私聊消息会转发到指定的 Telegram 聊天
- 在 Telegram 私聊中发送消息，会回复到指定的 QQ 群

## 注意事项

- 互通模式与转发模式可同时开启，但互通消息不会重复进入转发模式
- 互通模式为一对一配置，暂不支持多群互通
- Telegram 图片/贴纸下载会自动走适配器配置的代理
