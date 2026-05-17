# nonebot-plugin-onebot2tg

 > OneBot V11 与 Telegram 消息转发插件  


## 功能

- [x] **互通模式**：指定一个 QQ 群与一个 Telegram 群/频道双向互通，消息实时同步
- [x] **转发模式**：将 QQ 所有接收到的消息单向转发到 Telegram 私聊/频道/群聊
- [x] 互通模式和转发模式可同时开启不会重复发送消息
- [x] Telegram 图片/贴纸下载会自动走适配器配置的代理
- [x] **消息类型支持**：文本、图片、贴纸
- [ ] 贴纸图片过大时自动压缩？
- [ ] GIF转发
- [ ] 显示具体表情而不是表情ID
- [ ] 显示@人的昵称而不是QQ号
- [ ] 双向转发Reply消息 这个可能需要做数据库
- [ ] 在实现Reply消息后 实现转发模式双向转发  
...

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
| `ONEBOT2TG_ENABLE_BRIDGE` | `bool` | `True` | 开启互通模式（双向转发，需配置互通群号，默认开启） |
| `ONEBOT2TG_ENABLE_FORWARD` | `bool` | `False` | 开启转发模式（QQ 所有消息单向转发到 TG） |

### 互通模式配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `ONEBOT2TG_BRIDGE_GROUP_ID` | `str \| int` | `""` | 互通模式下，要互通的 QQ 群号 |
| `ONEBOT2TG_BRIDGE_TG_CHAT_ID` | `str \| int` | `""` | 互通模式下，TG 对应的 chat_id（群或频道） |

### 转发模式配置

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `ONEBOT2TG_FORWARD_TARGET_CHAT_ID` | `str \| int` | `""` | 转发模式下，QQ 消息转发到 TG 的目标 chat_id 或 用户ID |

## 使用示例

### 场景 1：QQ 群与 Telegram 群互通

```env
ONEBOT2TG_ENABLE_BRIDGE=true
ONEBOT2TG_ENABLE_FORWARD=false
ONEBOT2TG_BRIDGE_GROUP_ID=123456789
ONEBOT2TG_BRIDGE_TG_CHAT_ID=-1001234567890
```

配置后，该 QQ 群与 Telegram 群的消息会实时双向同步。

### 场景 2：QQ 消息单向转发到 Telegram

```env
ONEBOT2TG_ENABLE_BRIDGE=false
ONEBOT2TG_ENABLE_FORWARD=true
ONEBOT2TG_FORWARD_TARGET_CHAT_ID=-1001234567890
```

配置后，QQ 群/私聊接收到的所有消息会单向转发到指定的 Telegram 聊天。

### 场景 3：互通和转发模式同时开启

## 注意事项
- 目前仅测试过QQ与TG互转，其他onebot实现欢迎提交测试结果及PR
- 互通模式为一对一配置，暂不支持多群互通
- 转发模式为单向（QQ → TG），TG 消息不会转发回 QQ

