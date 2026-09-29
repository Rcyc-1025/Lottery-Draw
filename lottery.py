# -*- coding: utf-8 -*-
"""
抽奖程序
功能：
  1. 导入 txt 抽奖名单（一行一个选项）
  2. 抽奖（滚动动画），支持设置每次抽取数量
  3. 淘汰模式：中奖者从奖池移除，不会重复中奖
  4. 抽奖记录查询与导出（CSV，可用 Excel 打开）
运行：python lottery.py
"""

import csv
import os
import random
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

RECORD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lottery_records.csv")


class LotteryApp:
    def __init__(self, root):
        self.root = root
        root.title("抽奖程序")
        root.geometry("900x600")
        root.minsize(800, 500)

        self.name_list = []      # 原始名单
        self.pool = []           # 当前奖池（淘汰模式下会减少）
        self.records = []        # [(时间, 轮次, 结果)]
        self.round_no = 0
        self.rolling = False     # 是否正在滚动抽奖

        self._build_ui()
        self._load_records()

    # ---------------- UI ----------------
    def _build_ui(self):
        # 顶部工具栏
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=tk.X)

        ttk.Button(top, text="导入名单(txt)", command=self.import_list).pack(side=tk.LEFT)
        ttk.Button(top, text="手动添加", command=self.add_manual).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(top, text="清空名单", command=self.clear_list).pack(side=tk.LEFT, padx=(6, 0))

        self.lbl_count = ttk.Label(top, text="名单: 0 人 | 奖池剩余: 0 人")
        self.lbl_count.pack(side=tk.LEFT, padx=16)

        ttk.Label(top, text="每次抽取:").pack(side=tk.LEFT)
        self.spin_count = ttk.Spinbox(top, from_=1, to=100, width=5)
        self.spin_count.set(1)
        self.spin_count.pack(side=tk.LEFT, padx=(4, 12))

        self.var_eliminate = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="淘汰模式(中奖后移出奖池)", variable=self.var_eliminate).pack(side=tk.LEFT)

        # 中部：抽奖显示区
        mid = ttk.LabelFrame(self.root, text="抽奖区", padding=10)
        mid.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 4))

        self.lbl_display = tk.Label(mid, text="请先导入名单", font=("微软雅黑", 36, "bold"),
                                    fg="#333", bg="#fff", relief=tk.SUNKEN)
        self.lbl_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.btn_draw = ttk.Button(mid, text="开始抽奖", command=self.draw)
        self.btn_draw.pack()

        # 底部：记录区
        bottom = ttk.LabelFrame(self.root, text="抽奖记录", padding=8)
        bottom.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        cols = ("time", "round", "result")
        self.tree = ttk.Treeview(bottom, columns=cols, show="headings", height=8)
        self.tree.heading("time", text="时间")
        self.tree.heading("round", text="轮次")
        self.tree.heading("result", text="中奖结果")
        self.tree.column("time", width=160, anchor=tk.CENTER)
        self.tree.column("round", width=60, anchor=tk.CENTER)
        self.tree.column("result", width=560, anchor=tk.W)
        sb = ttk.Scrollbar(bottom, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.LEFT, fill=tk.Y)

        btns = ttk.Frame(bottom)
        btns.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 0))
        ttk.Button(btns, text="导出记录", command=self.export_records).pack(fill=tk.X)
        ttk.Button(btns, text="清空记录", command=self.clear_records).pack(fill=tk.X, pady=(6, 0))

    # ---------------- 名单 ----------------
    def import_list(self):
        path = filedialog.askopenfilename(
            title="选择抽奖名单",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
        )
        if not path:
            return
        try:
            # 依次尝试常见编码，兼容 GBK/UTF-8 的 txt
            names = None
            for enc in ("utf-8-sig", "gbk", "utf-8"):
                try:
                    with open(path, "r", encoding=enc) as f:
                        names = [line.strip() for line in f]
                    break
                except UnicodeDecodeError:
                    continue
            if names is None:
                raise ValueError("无法识别文件编码")
            # 去空行、去重并保持顺序
            seen = set()
            names = [n for n in names if n and not (n in seen or seen.add(n))]
            if not names:
                messagebox.showwarning("提示", "名单为空，请检查文件内容（一行一个选项）。")
                return
            self.name_list = names
            self.pool = list(names)
            self._refresh_count()
            self.lbl_display.config(text=f"已导入 {len(names)} 项，点击开始抽奖")
        except Exception as e:
            messagebox.showerror("导入失败", str(e))

    def add_manual(self):
        """弹出输入窗口，手动逐行添加抽奖项。"""
        win = tk.Toplevel(self.root)
        win.title("手动添加抽奖项")
        win.geometry("400x350")
        win.transient(self.root)
        win.grab_set()

        ttk.Label(win, text="每行输入一个抽奖项，点确认后添加到奖池：").pack(anchor=tk.W, padx=10, pady=(8, 4))
        text = tk.Text(win, height=15, wrap=tk.NONE)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))

        def on_confirm():
            raw = text.get("1.0", tk.END).strip()
            if not raw:
                messagebox.showwarning("提示", "请输入至少一个抽奖项。", parent=win)
                return
            lines = [l.strip() for l in raw.splitlines() if l.strip()]
            # 去重：跳过已存在于名单中的项
            existing = set(self.name_list)
            added = [l for l in lines if l not in existing and not existing.add(l)]
            if not added:
                messagebox.showinfo("提示", "输入的项均已存在于名单中。", parent=win)
                return
            self.name_list.extend(added)
            self.pool.extend(added)
            self._refresh_count()
            self.lbl_display.config(text=f"已添加 {len(added)} 项，当前共 {len(self.name_list)} 项")
            win.destroy()

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text="确认添加", command=on_confirm).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="取消", command=win.destroy).pack(side=tk.RIGHT, padx=(0, 8))
        win.bind("<Return>", lambda e: on_confirm())

    def clear_list(self):
        if messagebox.askyesno("确认", "确定清空名单和奖池吗？"):
            self.name_list = []
            self.pool = []
            self._refresh_count()
            self.lbl_display.config(text="请先导入名单")

    def _refresh_count(self):
        self.lbl_count.config(text=f"名单: {len(self.name_list)} 人 | 奖池剩余: {len(self.pool)} 人")

    # ---------------- 抽奖 ----------------
    def draw(self):
        if self.rolling:
            return
        if not self.pool:
            messagebox.showwarning("提示", "奖池为空！请导入名单，或奖池已被抽完。")
            return
        try:
            count = int(self.spin_count.get())
        except ValueError:
            count = 1
        count = max(1, count)
        if count > len(self.pool):
            messagebox.showwarning("提示", f"奖池仅剩 {len(self.pool)} 项，少于抽取数量 {count}。")
            return

        self.rolling = True
        self.btn_draw.config(state=tk.DISABLED, text="抽奖中...")
        self._roll_start = datetime.now()
        self._roll_step()

    def _roll_step(self):
        """滚动动画：快速随机切换显示内容，约 2 秒后停止。"""
        elapsed = (datetime.now() - self._roll_start).total_seconds()
        if elapsed < 2.0:
            sample = random.sample(self.pool, min(5, len(self.pool)))
            self.lbl_display.config(text="  |  ".join(sample), fg="#888")
            self.root.after(60, self._roll_step)
        else:
            self._finish_draw()

    def _finish_draw(self):
        try:
            count = max(1, int(self.spin_count.get()))
        except ValueError:
            count = 1
        count = min(count, len(self.pool))
        winners = random.sample(self.pool, count)

        # 淘汰模式：中奖者移出奖池
        if self.var_eliminate.get():
            for w in winners:
                self.pool.remove(w)

        self.round_no += 1
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_str = "、".join(winners)
        self.records.append((time_str, self.round_no, result_str))
        self.tree.insert("", 0, values=(time_str, self.round_no, result_str))
        self._save_record_row(time_str, self.round_no, result_str)

        self.lbl_display.config(text=result_str, fg="#d40000")
        self._refresh_count()
        self.rolling = False
        self.btn_draw.config(state=tk.NORMAL, text="开始抽奖")

    # ---------------- 记录 ----------------
    def _load_records(self):
        """启动时加载历史记录。"""
        if not os.path.exists(RECORD_FILE):
            return
        try:
            with open(RECORD_FILE, "r", encoding="utf-8-sig", newline="") as f:
                for row in csv.reader(f):
                    if len(row) >= 3 and row[0] != "时间":
                        self.records.append((row[0], int(row[1]), row[2]))
                        self.tree.insert("", tk.END, values=(row[0], row[1], row[2]))
            if self.records:
                self.round_no = max(r[1] for r in self.records)
        except Exception:
            pass

    def _save_record_row(self, time_str, round_no, result_str):
        """追加写入记录文件。"""
        need_header = not os.path.exists(RECORD_FILE) or os.path.getsize(RECORD_FILE) == 0
        with open(RECORD_FILE, "a", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            if need_header:
                w.writerow(["时间", "轮次", "中奖结果"])
            w.writerow([time_str, round_no, result_str])

    def export_records(self):
        if not self.records:
            messagebox.showwarning("提示", "暂无抽奖记录。")
            return
        path = filedialog.asksaveasfilename(
            title="导出抽奖记录",
            defaultextension=".csv",
            initialfile=f"抽奖记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            filetypes=[("CSV 文件", "*.csv")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow(["时间", "轮次", "中奖结果"])
                w.writerows(self.records)
            messagebox.showinfo("导出成功", f"记录已导出到：\n{path}")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    def clear_records(self):
        if not self.records:
            return
        if messagebox.askyesno("确认", "确定清空所有抽奖记录吗？（同时删除本地记录文件）"):
            self.records.clear()
            self.round_no = 0
            for item in self.tree.get_children():
                self.tree.delete(item)
            if os.path.exists(RECORD_FILE):
                os.remove(RECORD_FILE)


if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()
