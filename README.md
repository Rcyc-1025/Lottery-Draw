# Lottery 抽奖程序

A lightweight desktop lottery / raffle tool written in Python with Tkinter.
No third-party dependencies — runs with the standard library only.

一个轻量的桌面抽奖工具，纯 Python 标准库实现（Tkinter 界面），无需安装任何第三方依赖。

---

## 1. Problem Solved 解决什么问题

When you need to run a raffle / lucky draw in an offline environment (office party, team event, classroom), you want a tool that:
- does not require signing up or logging into any online service
- does not depend on third-party packages that need pip installation
- can import an existing name list without retyping
- supports elimination-style draws (no repeat winners) and plain random draws
- keeps a searchable, exportable record of every draw

当你需要在离线环境（年会、团建、课堂）进行抽奖时，希望有一个工具：
- 不需要注册或登录任何在线服务
- 不依赖需要 pip 安装的第三方包
- 可以直接导入已有名单，无需重新输入
- 同时支持淘汰式抽奖（不重复中奖）和普通随机抽奖
- 对每次抽奖保留可查询、可导出的记录

## 2. Features 主要功能

- **Import name list (txt)** — one entry per line; auto-removes blank lines and duplicates; compatible with UTF-8 / GBK encodings
  导入 txt 名单：一行一个选项，自动去空行、去重，兼容 UTF-8 / GBK 编码
- **Manual entry** — add entries one per line via a popup dialog, with auto deduplication
  手动添加：通过弹窗逐行输入抽奖项，自动去重
- **Draw with rolling animation** — configurable number of winners per draw (1–100), with a 2-second rolling animation
  抽奖带 2 秒滚动动画，可设置每次抽取数量（1–100）
- **Elimination mode** — winners are removed from the pool and cannot be drawn again; can be toggled off to allow repeat winners
  淘汰模式：中奖者自动移出奖池不重复中奖；取消勾选则允许重复中奖
- **Record history** — every draw (time / round / result) is shown in a table and persisted locally, restored on restart
  抽奖记录实时展示，并自动保存到本地文件，重启后自动恢复
- **Export records** — one-click export to CSV (utf-8-sig, opens correctly in Excel)
  一键导出 CSV 记录，Excel 打开不乱码

## 3. Installation 安装方法

### Prerequisites 环境要求

- Python 3.x
- Tkinter (bundled with the official Python installer on Windows and macOS; on Debian/Ubuntu install `python3-tk`)

### Steps 安装步骤

No installation needed — just clone or download the repository:

```bash
git clone https://github.com/<your-username>/lottery.git
cd lottery
```

That's it. No `pip install` required.

无需安装，克隆或下载仓库即可，不需要 `pip install`。

## 4. Usage 使用方法

```bash
python lottery.py
```

1. Click **导入名单(txt)** and select a txt file with one entry per line (see `names_example.txt`), OR click **手动添加** to type entries directly.
   点击 **导入名单(txt)** 选择 txt 文件（一行一个选项，参考 `names_example.txt`），或点击 **手动添加** 直接输入。
2. Set **每次抽取** (draw count) and toggle **淘汰模式** (elimination mode) as needed.
   设置 **每次抽取** 数量，按需勾选 **淘汰模式**。
3. Click **开始抽奖** to draw. The display scrolls for ~2 seconds then shows the winner(s).
   点击 **开始抽奖**，显示区滚动约 2 秒后揭晓中奖者。
4. View history in the records table; click **导出记录** to export CSV.
   在下方记录表格查看历史，点击 **导出记录** 导出 CSV。

## 5. Input / Output Example 输入输出示例

### Input (names_example.txt) 输入示例

```
Alice
Bob
Carol
David
Emma
```

### GUI Interaction 界面操作

| Step 操作 | Action |
|---|---|
| 1 | Import `names_example.txt` → display shows "已导入 5 项" |
| 2 | Set draw count = 1, elimination mode ON |
| 3 | Click **开始抽奖** → rolling animation → result shown in red |

### Output 输出示例

After 3 draws with elimination mode ON:

| Time 时间 | Round 轮次 | Result 中奖结果 |
|---|---|---|
| 2026-09-29 10:00:01 | 1 | Carol |
| 2026-09-29 10:00:08 | 2 | Alice |
| 2026-09-29 10:00:15 | 3 | David |

Pool remaining: Bob, Emma (2).

### Exported CSV 导出的 CSV

```csv
时间,轮次,中奖结果
2026-09-29 10:00:01,1,Carol
2026-09-29 10:00:08,2,Alice
2026-09-29 10:00:15,3,David
```

## 6. Project Structure 项目结构

```
lottery/
├── lottery.py            # Main program 主程序
├── names_example.txt     # Example name list 示例名单
├── README.md             # Documentation 说明文档
├── LICENSE               # Mozilla Public License 2.0
└── .gitignore            # Ignore local artifacts 忽略本地生成文件
```

Run-time generated files (not tracked by git):
运行时自动生成（不纳入版本控制）：
- `lottery_records.csv` — local draw history 本地抽奖记录

## 7. Tech Stack 技术栈

- **Language 语言**: Python 3
- **GUI**: Tkinter (standard library)
- **Persistence 持久化**: CSV (utf-8-sig)

## 8. Notes 注意事项

- Draw history is stored locally in `lottery_records.csv` next to the script. This file is not uploaded to the repository.
  抽奖记录保存在脚本同目录的 `lottery_records.csv`，不会上传到仓库。
- The random selection uses Python's `random` module (Mersenne Twister), which is NOT cryptographically secure. Not recommended for high-stakes gambling.
  随机抽取使用 Python `random` 模块（非密码学安全），不建议用于高赌注博彩。

## License 许可证

This project is licensed under the **Mozilla Public License 2.0** — see the [LICENSE](LICENSE) file for details.

本项目采用 **Mozilla Public License 2.0** 许可证，详见 [LICENSE](LICENSE) 文件。
