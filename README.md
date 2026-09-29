# Lottery 抽奖程序

<div align="center">

**English** | [中文](#中文)

A lightweight desktop lottery / raffle tool built with Python Tkinter.
No third-party dependencies — runs with the standard library only.

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-blue.svg)](https://opensource.org/licenses/MPL-2.0)
[![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![Release](https://img.shields.io/badge/release-v1.0-green.svg)](https://github.com/Rcyc-1025/Lottery-Draw/releases)

</div>

---

## English

### 1. Problem Solved

When you need to run a raffle / lucky draw in an offline environment (office party, team event, classroom), you want a tool that:

- does not require signing up or logging into any online service
- does not depend on third-party packages that need `pip` installation
- can import an existing name list without retyping
- supports elimination-style draws (no repeat winners) and plain random draws
- keeps a searchable, exportable record of every draw

### 2. Features

- **Import name list (txt)** — one entry per line; auto-removes blank lines and duplicates; compatible with UTF-8 / GBK encodings
- **Manual entry** — add entries one per line via a popup dialog, with auto deduplication
- **Draw with rolling animation** — configurable number of winners per draw (1–100), with a ~2 second scrolling animation
- **Elimination mode** — winners are removed from the pool and cannot be drawn again; can be toggled off to allow repeat winners
- **Record history** — every draw (time / round / result) is shown in a table and persisted locally, restored on restart
- **Export records** — one-click export to CSV (utf-8-sig, opens correctly in Excel)

### 3. Installation

#### Prerequisites

- Python 3.x
- Tkinter (bundled with the official Python installer on Windows and macOS; on Debian/Ubuntu install `python3-tk`)

#### Steps

No installation needed — just clone or download the repository:

```bash
git clone https://github.com/Rcyc-1025/Lottery-Draw.git
cd Lottery-Draw
```

That's it. No `pip install` required.

### 4. Usage

```bash
python lottery.py
```

1. Click **导入名单(txt)** and select a txt file with one entry per line (see `names_example.txt`), **or** click **手动添加** to type entries directly.
2. Set **每次抽取** (draw count) and toggle **淘汰模式** (elimination mode) as needed.
3. Click **开始抽奖** to draw. The display scrolls for ~2 seconds then shows the winner(s).
4. View history in the records table; click **导出记录** to export CSV.

### 5. Input / Output Example

#### Input (`names_example.txt`)

```
Alice
Bob
Carol
David
Emma
```

#### GUI Interaction

| Step | Action |
|---|---|
| 1 | Import `names_example.txt` → display shows "已导入 5 项" |
| 2 | Set draw count = 1, elimination mode ON |
| 3 | Click **开始抽奖** → rolling animation → result shown in red |

#### Output

After 3 draws with elimination mode ON:

| Time | Round | Result |
|---|---|---|
| 2026-09-29 10:00:01 | 1 | Carol |
| 2026-09-29 10:00:08 | 2 | Alice |
| 2026-09-29 10:00:15 | 3 | David |

Pool remaining: Bob, Emma (2).

#### Exported CSV

```csv
时间,轮次,中奖结果
2026-09-29 10:00:01,1,Carol
2026-09-29 10:00:08,2,Alice
2026-09-29 10:00:15,3,David
```

### 6. Project Structure

```
Lottery-Draw/
├── lottery.py            # Main program
├── names_example.txt     # Example name list
├── README.md             # Documentation
├── LICENSE               # Mozilla Public License 2.0
└── .gitignore            # Ignore local artifacts
```

Run-time generated files (not tracked by git):

- `lottery_records.csv` — local draw history

### 7. Tech Stack

- **Language**: Python 3
- **GUI**: Tkinter (standard library)
- **Persistence**: CSV (utf-8-sig)

### 8. Notes

- Draw history is stored locally in `lottery_records.csv` next to the script. This file is not uploaded to the repository.
- The random selection uses Python's `random` module (Mersenne Twister), which is **not** cryptographically secure. Not recommended for high-stakes gambling.

### License

This project is licensed under the **Mozilla Public License 2.0** — see the [LICENSE](LICENSE) file for details.

---

## 中文

<div align="right">

[English](#english) | **中文**

</div>

一个轻量的桌面抽奖工具，纯 Python 标准库实现（Tkinter 界面），无需安装任何第三方依赖。

### 1. 解决什么问题

当你需要在离线环境（年会、团建、课堂）进行抽奖时，希望有一个工具：

- 不需要注册或登录任何在线服务
- 不依赖需要 `pip` 安装的第三方包
- 可以直接导入已有名单，无需重新输入
- 同时支持淘汰式抽奖（不重复中奖）和普通随机抽奖
- 对每次抽奖保留可查询、可导出的记录

### 2. 主要功能

- **导入 txt 名单**：一行一个选项，自动去空行、去重，兼容 UTF-8 / GBK 编码
- **手动添加**：通过弹窗逐行输入抽奖项，自动去重
- **滚动动画抽奖**：可设置每次抽取数量（1–100），带约 2 秒滚动动画
- **淘汰模式**：中奖者自动移出奖池不重复中奖；取消勾选则允许重复中奖
- **抽奖记录**：每次抽奖（时间 / 轮次 / 结果）实时展示，并自动保存到本地文件，重启后自动恢复
- **导出记录**：一键导出 CSV（utf-8-sig 编码，Excel 打开不乱码）

### 3. 安装方法

#### 环境要求

- Python 3.x
- Tkinter（Windows 和 macOS 的官方 Python 安装包已自带；Debian/Ubuntu 需安装 `python3-tk`）

#### 安装步骤

无需安装，克隆或下载仓库即可：

```bash
git clone https://github.com/Rcyc-1025/Lottery-Draw.git
cd Lottery-Draw
```

不需要 `pip install`。

### 4. 使用方法

```bash
python lottery.py
```

1. 点击 **导入名单(txt)** 选择 txt 文件（一行一个选项，参考 `names_example.txt`），**或** 点击 **手动添加** 直接输入。
2. 设置 **每次抽取** 数量，按需勾选 **淘汰模式**。
3. 点击 **开始抽奖**，显示区滚动约 2 秒后揭晓中奖者。
4. 在下方记录表格查看历史，点击 **导出记录** 导出 CSV。

### 5. 输入输出示例

#### 输入（`names_example.txt`）

```
Alice
Bob
Carol
David
Emma
```

#### 界面操作

| 步骤 | 操作 |
|---|---|
| 1 | 导入 `names_example.txt` → 显示"已导入 5 项" |
| 2 | 设置每次抽取 = 1，开启淘汰模式 |
| 3 | 点击 **开始抽奖** → 滚动动画 → 红色显示中奖结果 |

#### 输出

开启淘汰模式抽奖 3 次后：

| 时间 | 轮次 | 中奖结果 |
|---|---|---|
| 2026-09-29 10:00:01 | 1 | Carol |
| 2026-09-29 10:00:08 | 2 | Alice |
| 2026-09-29 10:00:15 | 3 | David |

奖池剩余：Bob, Emma（2 项）。

#### 导出的 CSV

```csv
时间,轮次,中奖结果
2026-09-29 10:00:01,1,Carol
2026-09-29 10:00:08,2,Alice
2026-09-29 10:00:15,3,David
```

### 6. 项目结构

```
Lottery-Draw/
├── lottery.py            # 主程序
├── names_example.txt     # 示例名单
├── README.md             # 说明文档
├── LICENSE               # Mozilla Public License 2.0
└── .gitignore            # 忽略本地生成文件
```

运行时自动生成（不纳入版本控制）：

- `lottery_records.csv` — 本地抽奖记录

### 7. 技术栈

- **语言**：Python 3
- **GUI**：Tkinter（标准库）
- **持久化**：CSV（utf-8-sig）

### 8. 注意事项

- 抽奖记录保存在脚本同目录的 `lottery_records.csv`，不会上传到仓库。
- 随机抽取使用 Python `random` 模块（Mersenne Twister），**非**密码学安全，不建议用于高赌注博彩。

### 许可证

本项目采用 **Mozilla Public License 2.0** 许可证，详见 [LICENSE](LICENSE) 文件。
