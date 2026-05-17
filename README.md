<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ nonebot-plugin-onebot2tg ✨
[![LICENSE](https://img.shields.io/github/license/SoulGateKey/nonebot-plugin-onebot2tg.svg)](./LICENSE)
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-onebot2tg.svg)](https://pypi.python.org/pypi/nonebot-plugin-onebot2tg)
[![python](https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg)](https://www.python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-black?style=flat-square&logo=uv)](https://github.com/astral-sh/uv)
<br/>
[![ruff](https://img.shields.io/badge/code%20style-ruff-black?style=flat-square&logo=ruff)](https://github.com/astral-sh/ruff)
[![pre-commit](https://results.pre-commit.ci/badge/github/SoulGateKey/nonebot-plugin-onebot2tg/main.svg)](https://results.pre-commit.ci/latest/github/SoulGateKey/nonebot-plugin-onebot2tg/main)
</div>

  OneBot V11 与 Telegram 消息转发插件  


## 📖 功能

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

## 💿 安装
<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-onebot2tg --upgrade
使用 **pypi** 源安装

    nb plugin install nonebot-plugin-onebot2tg --upgrade -i "https://pypi.org/simple"
使用**清华源**安装

    nb plugin install nonebot-plugin-onebot2tg --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple"


</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details open>
<summary>uv</summary>

    uv add nonebot-plugin-onebot2tg
安装仓库 main 分支

    uv add git+https://github.com/SoulGateKey/nonebot-plugin-onebot2tg@main
</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-onebot2tg
安装仓库 main 分支

    pdm add git+https://github.com/SoulGateKey/nonebot-plugin-onebot2tg@main
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-onebot2tg
安装仓库 main 分支

    poetry add git+https://github.com/SoulGateKey/nonebot-plugin-onebot2tg@main
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_onebot2tg"]

</details>

<details>
<summary>使用 nbr 安装(使用 uv 管理依赖可用)</summary>

[nbr](https://github.com/fllesser/nbr) 是一个基于 uv 的 nb-cli，可以方便地管理 nonebot2

    nbr plugin install nonebot-plugin-onebot2tg
使用 **pypi** 源安装

    nbr plugin install nonebot-plugin-onebot2tg -i "https://pypi.org/simple"
使用**清华源**安装

    nbr plugin install nonebot-plugin-onebot2tg -i "https://pypi.tuna.tsinghua.edu.cn/simple"

</details>

## 依赖适配器

- [nonebot-adapter-onebot](https://github.com/nonebot/adapter-onebot) (OneBot V11)
- [nonebot-adapter-telegram](https://github.com/nonebot/adapter-telegram) (Telegram)

## ⚙️ 配置

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

## 🎉 使用示例

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

