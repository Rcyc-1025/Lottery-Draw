# -*- coding: utf-8 -*-
"""
抽奖程序 / Lottery Programme
功能：
  1. 导入 txt 抽奖名单（一行一个选项）
  2. 手动添加抽奖项
  3. 抽奖（滚动动画），支持设置每次抽取数量
  4. 淘汰模式：中奖者从奖池移除，不会重复中奖
  5. 抽奖记录查询与导出（CSV，可用 Excel 打开）
  6. 三语言支持：中文、英式英语、美式英语
运行：python lottery.py
"""

import csv
import json
import os
import random
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORD_FILE = os.path.join(BASE_DIR, "lottery_records.csv")
CONFIG_FILE = os.path.join(BASE_DIR, "lottery_config.json")

# ---------------- 多语言字典 ----------------
# 英式英语(en_GB)与美式英语(en_US)的差异采用真实拼写/用词区别：
#   Programme(GB) / Program(US)
#   Draw(GB) / Drawing(US)
#   Raffle(GB) / Lottery(US)
I18N = {
    "zh": {
        "app_title": "抽奖程序",
        "btn_import": "导入名单(txt)",
        "btn_add_manual": "手动添加",
        "btn_clear_list": "清空名单",
        "lbl_count": "名单: {} 人 | 奖池剩余: {} 人",
        "lbl_draw_count": "每次抽取:",
        "chk_eliminate": "淘汰模式(中奖后移出奖池)",
        "frame_draw": "抽奖区",
        "display_init": "请先导入名单",
        "btn_draw": "开始抽奖",
        "btn_drawing": "抽奖中...",
        "frame_records": "抽奖记录",
        "col_time": "时间",
        "col_round": "轮次",
        "col_result": "中奖结果",
        "btn_export": "导出记录",
        "btn_clear_records": "清空记录",
        "lbl_language": "语言:",
        "manual_title": "手动添加抽奖项",
        "manual_label": "每行输入一个抽奖项，点确认后添加到奖池：",
        "btn_confirm": "确认添加",
        "btn_cancel": "取消",
        "dlg_select_list": "选择抽奖名单",
        "ft_text": "文本文件",
        "ft_all": "所有文件",
        "msg_empty_list": "名单为空，请检查文件内容（一行一个选项）。",
        "msg_import_failed": "导入失败",
        "msg_imported": "已导入 {} 项，点击开始抽奖",
        "msg_added": "已添加 {} 项，当前共 {} 项",
        "msg_confirm": "确认",
        "msg_clear_list": "确定清空名单和奖池吗？",
        "msg_pool_empty": "奖池为空！请导入名单，或奖池已被抽完。",
        "msg_pool_insufficient": "奖池仅剩 {} 项，少于抽取数量 {}。",
        "msg_no_records": "暂无抽奖记录。",
        "dlg_export": "导出抽奖记录",
        "ft_csv": "CSV 文件",
        "msg_export_success": "导出成功",
        "msg_exported_to": "记录已导出到：\n{}",
        "msg_export_failed": "导出失败",
        "msg_clear_records": "确定清空所有抽奖记录吗？（同时删除本地记录文件）",
        "msg_please_input": "请输入至少一个抽奖项。",
        "msg_all_exist": "输入的项均已存在于名单中。",
        "msg_encoding_error": "无法识别文件编码",
        "csv_time": "时间",
        "csv_round": "轮次",
        "csv_result": "中奖结果",
        "display_default_after_clear": "请先导入名单",
    },
    "en_GB": {
        "app_title": "Lottery Programme",
        "btn_import": "Import List (txt)",
        "btn_add_manual": "Add Manually",
        "btn_clear_list": "Clear List",
        "lbl_count": "List: {} | Pool remaining: {}",
        "lbl_draw_count": "Draw count:",
        "chk_eliminate": "Elimination mode (winners removed from pool)",
        "frame_draw": "Draw Area",
        "display_init": "Please import a name list first",
        "btn_draw": "Start Draw",
        "btn_drawing": "Drawing...",
        "frame_records": "Draw Records",
        "col_time": "Time",
        "col_round": "Round",
        "col_result": "Result",
        "btn_export": "Export Records",
        "btn_clear_records": "Clear Records",
        "lbl_language": "Language:",
        "manual_title": "Add Entries Manually",
        "manual_label": "Enter one entry per line, then confirm to add to the pool:",
        "btn_confirm": "Confirm",
        "btn_cancel": "Cancel",
        "dlg_select_list": "Select Name List",
        "ft_text": "Text files",
        "ft_all": "All files",
        "msg_empty_list": "Name list is empty, please check the file content (one entry per line).",
        "msg_import_failed": "Import Failed",
        "msg_imported": "Imported {} entries, click Start Draw",
        "msg_added": "Added {} entries, {} total",
        "msg_confirm": "Confirm",
        "msg_clear_list": "Clear the name list and pool?",
        "msg_pool_empty": "Pool is empty! Please import a name list, or the pool has been exhausted.",
        "msg_pool_insufficient": "Only {} entries left in the pool, fewer than the draw count {}.",
        "msg_no_records": "No draw records.",
        "dlg_export": "Export Draw Records",
        "ft_csv": "CSV files",
        "msg_export_success": "Export Successful",
        "msg_exported_to": "Records exported to:\n{}",
        "msg_export_failed": "Export Failed",
        "msg_clear_records": "Clear all draw records? (local record file will also be deleted)",
        "msg_please_input": "Please enter at least one entry.",
        "msg_all_exist": "All entered entries already exist in the list.",
        "msg_encoding_error": "Unrecognised file encoding",
        "csv_time": "Time",
        "csv_round": "Round",
        "csv_result": "Result",
        "display_default_after_clear": "Please import a name list first",
    },
    "en_US": {
        "app_title": "Lottery Program",
        "btn_import": "Import List (txt)",
        "btn_add_manual": "Add Manually",
        "btn_clear_list": "Clear List",
        "lbl_count": "List: {} | Pool remaining: {}",
        "lbl_draw_count": "Draw count:",
        "chk_eliminate": "Elimination mode (winners removed from pool)",
        "frame_draw": "Drawing Area",
        "display_init": "Please import a name list first",
        "btn_draw": "Start Drawing",
        "btn_drawing": "Drawing...",
        "frame_records": "Draw Records",
        "col_time": "Time",
        "col_round": "Round",
        "col_result": "Result",
        "btn_export": "Export Records",
        "btn_clear_records": "Clear Records",
        "lbl_language": "Language:",
        "manual_title": "Add Entries Manually",
        "manual_label": "Enter one entry per line, then confirm to add to the pool:",
        "btn_confirm": "Confirm",
        "btn_cancel": "Cancel",
        "dlg_select_list": "Select Name List",
        "ft_text": "Text files",
        "ft_all": "All files",
        "msg_empty_list": "Name list is empty, please check the file content (one entry per line).",
        "msg_import_failed": "Import Failed",
        "msg_imported": "Imported {} entries, click Start Drawing",
        "msg_added": "Added {} entries, {} total",
        "msg_confirm": "Confirm",
        "msg_clear_list": "Clear the name list and pool?",
        "msg_pool_empty": "Pool is empty! Please import a name list, or the pool has been exhausted.",
        "msg_pool_insufficient": "Only {} entries left in the pool, fewer than the draw count {}.",
        "msg_no_records": "No draw records.",
        "dlg_export": "Export Draw Records",
        "ft_csv": "CSV files",
        "msg_export_success": "Export Successful",
        "msg_exported_to": "Records exported to:\n{}",
        "msg_export_failed": "Export Failed",
        "msg_clear_records": "Clear all draw records? (local record file will also be deleted)",
        "msg_please_input": "Please enter at least one entry.",
        "msg_all_exist": "All entered entries already exist in the list.",
        "msg_encoding_error": "Unrecognized file encoding",
        "csv_time": "Time",
        "csv_round": "Round",
        "csv_result": "Result",
        "display_default_after_clear": "Please import a name list first",
    },
}

LANGUAGE_LABELS = {
    "zh": "中文",
    "en_GB": "English (UK)",
    "en_US": "English (US)",
}


class LotteryApp:
    def __init__(self, root):
        self.root = root
        root.geometry("900x600")
        root.minsize(800, 500)

        self.name_list = []      # 原始名单
        self.pool = []           # 当前奖池（淘汰模式下会减少）
        self.records = []        # [(时间, 轮次, 结果)]
        self.round_no = 0
        self.rolling = False     # 是否正在滚动抽奖
        self.language = self._load_language()

        self._build_ui()
        self._refresh_ui_text()
        self._load_records()

    # ---------------- 语言 ----------------
    def _load_language(self):
        """从配置文件读取语言，默认中文。"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                lang = cfg.get("language", "zh")
                if lang in I18N:
                    return lang
        except Exception:
            pass
        return "zh"

    def _save_language(self):
        try:
            cfg = {"language": self.language}
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _t(self, key):
        """获取当前语言的翻译文本。"""
        return I18N[self.language].get(key, key)

    def _on_language_change(self, event=None):
        """语言下拉框切换时触发。"""
        selected = self.language_var.get()
        # 从显示标签反查语言代码
        for code, label in LANGUAGE_LABELS.items():
            if label == selected:
                self.language = code
                break
        self._save_language()
        self._refresh_ui_text()

    def _refresh_ui_text(self):
        """根据当前语言刷新所有界面文本。"""
        t = self._t
        self.root.title(t("app_title"))
        self.btn_import.config(text=t("btn_import"))
        self.btn_add_manual.config(text=t("btn_add_manual"))
        self.btn_clear_list.config(text=t("btn_clear_list"))
        self.lbl_draw_count.config(text=t("lbl_draw_count"))
        self.chk_eliminate.config(text=t("chk_eliminate"))
        self.lbl_language.config(text=t("lbl_language"))
        self.frame_draw.config(text=t("frame_draw"))
        self.frame_records.config(text=t("frame_records"))
        self.btn_export.config(text=t("btn_export"))
        self.btn_clear_records.config(text=t("btn_clear_records"))
        self.tree.heading("time", text=t("col_time"))
        self.tree.heading("round", text=t("col_round"))
        self.tree.heading("result", text=t("col_result"))

        # 抽奖按钮文字
        if self.rolling:
            self.btn_draw.config(text=t("btn_drawing"))
        else:
            self.btn_draw.config(text=t("btn_draw"))

        # 计数标签
        self._refresh_count()

        # 初始显示文字（仅当显示区仍是默认提示时更新）
        current = self.lbl_display.cget("text")
        defaults = {I18N[l]["display_init"] for l in I18N}
        defaults.update({I18N[l]["display_default_after_clear"] for l in I18N})
        if current in defaults:
            self.lbl_display.config(text=t("display_init"))

    # ---------------- UI ----------------
    def _build_ui(self):
        # 顶部工具栏
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=tk.X)

        self.btn_import = ttk.Button(top, command=self.import_list)
        self.btn_import.pack(side=tk.LEFT)
        self.btn_add_manual = ttk.Button(top, command=self.add_manual)
        self.btn_add_manual.pack(side=tk.LEFT, padx=(6, 0))
        self.btn_clear_list = ttk.Button(top, command=self.clear_list)
        self.btn_clear_list.pack(side=tk.LEFT, padx=(6, 0))

        self.lbl_count = ttk.Label(top)
        self.lbl_count.pack(side=tk.LEFT, padx=16)

        self.lbl_draw_count = ttk.Label(top)
        self.lbl_draw_count.pack(side=tk.LEFT)
        self.spin_count = ttk.Spinbox(top, from_=1, to=100, width=5)
        self.spin_count.set(1)
        self.spin_count.pack(side=tk.LEFT, padx=(4, 12))

        self.var_eliminate = tk.BooleanVar(value=True)
        self.chk_eliminate = ttk.Checkbutton(top, variable=self.var_eliminate)
        self.chk_eliminate.pack(side=tk.LEFT)

        # 语言选择
        self.lbl_language = ttk.Label(top)
        self.lbl_language.pack(side=tk.LEFT, padx=(16, 4))
        self.language_var = tk.StringVar(value=LANGUAGE_LABELS[self.language])
        self.cmb_language = ttk.Combobox(
            top, textvariable=self.language_var, state="readonly", width=14,
            values=list(LANGUAGE_LABELS.values()),
        )
        self.cmb_language.pack(side=tk.LEFT)
        self.cmb_language.bind("<<ComboboxSelected>>", self._on_language_change)

        # 中部：抽奖显示区
        self.frame_draw = ttk.LabelFrame(self.root, padding=10)
        self.frame_draw.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 4))

        self.lbl_display = tk.Label(self.frame_draw, font=("微软雅黑", 36, "bold"),
                                    fg="#333", bg="#fff", relief=tk.SUNKEN)
        self.lbl_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.btn_draw = ttk.Button(self.frame_draw, command=self.draw)
        self.btn_draw.pack()

        # 底部：记录区
        self.frame_records = ttk.LabelFrame(self.root, padding=8)
        self.frame_records.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        cols = ("time", "round", "result")
        self.tree = ttk.Treeview(self.frame_records, columns=cols, show="headings", height=8)
        self.tree.column("time", width=160, anchor=tk.CENTER)
        self.tree.column("round", width=60, anchor=tk.CENTER)
        self.tree.column("result", width=560, anchor=tk.W)
        sb = ttk.Scrollbar(self.frame_records, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.LEFT, fill=tk.Y)

        btns = ttk.Frame(self.frame_records)
        btns.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 0))
        self.btn_export = ttk.Button(btns, command=self.export_records)
        self.btn_export.pack(fill=tk.X)
        self.btn_clear_records = ttk.Button(btns, command=self.clear_records)
        self.btn_clear_records.pack(fill=tk.X, pady=(6, 0))

    # ---------------- 名单 ----------------
    def import_list(self):
        t = self._t
        path = filedialog.askopenfilename(
            title=t("dlg_select_list"),
            filetypes=[(t("ft_text"), "*.txt"), (t("ft_all"), "*.*")],
        )
        if not path:
            return
        try:
            names = None
            for enc in ("utf-8-sig", "gbk", "utf-8"):
                try:
                    with open(path, "r", encoding=enc) as f:
                        names = [line.strip() for line in f]
                    break
                except UnicodeDecodeError:
                    continue
            if names is None:
                raise ValueError(t("msg_encoding_error"))
            seen = set()
            names = [n for n in names if n and not (n in seen or seen.add(n))]
            if not names:
                messagebox.showwarning(t("msg_confirm"), t("msg_empty_list"))
                return
            self.name_list = names
            self.pool = list(names)
            self._refresh_count()
            self.lbl_display.config(text=t("msg_imported").format(len(names)))
        except Exception as e:
            messagebox.showerror(t("msg_import_failed"), str(e))

    def add_manual(self):
        t = self._t
        win = tk.Toplevel(self.root)
        win.title(t("manual_title"))
        win.geometry("400x350")
        win.transient(self.root)
        win.grab_set()

        ttk.Label(win, text=t("manual_label")).pack(anchor=tk.W, padx=10, pady=(8, 4))
        text = tk.Text(win, height=15, wrap=tk.NONE)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))

        def on_confirm():
            raw = text.get("1.0", tk.END).strip()
            if not raw:
                messagebox.showwarning(t("msg_confirm"), t("msg_please_input"), parent=win)
                return
            lines = [l.strip() for l in raw.splitlines() if l.strip()]
            existing = set(self.name_list)
            added = [l for l in lines if l not in existing and not existing.add(l)]
            if not added:
                messagebox.showinfo(t("msg_confirm"), t("msg_all_exist"), parent=win)
                return
            self.name_list.extend(added)
            self.pool.extend(added)
            self._refresh_count()
            self.lbl_display.config(text=t("msg_added").format(len(added), len(self.name_list)))
            win.destroy()

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text=t("btn_confirm"), command=on_confirm).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text=t("btn_cancel"), command=win.destroy).pack(side=tk.RIGHT, padx=(0, 8))
        win.bind("<Return>", lambda e: on_confirm())

    def clear_list(self):
        t = self._t
        if messagebox.askyesno(t("msg_confirm"), t("msg_clear_list")):
            self.name_list = []
            self.pool = []
            self._refresh_count()
            self.lbl_display.config(text=t("display_default_after_clear"))

    def _refresh_count(self):
        self.lbl_count.config(text=self._t("lbl_count").format(len(self.name_list), len(self.pool)))

    # ---------------- 抽奖 ----------------
    def draw(self):
        t = self._t
        if self.rolling:
            return
        if not self.pool:
            messagebox.showwarning(t("msg_confirm"), t("msg_pool_empty"))
            return
        try:
            count = int(self.spin_count.get())
        except ValueError:
            count = 1
        count = max(1, count)
        if count > len(self.pool):
            messagebox.showwarning(t("msg_confirm"), t("msg_pool_insufficient").format(len(self.pool), count))
            return

        self.rolling = True
        self.btn_draw.config(state=tk.DISABLED, text=t("btn_drawing"))
        self._roll_start = datetime.now()
        self._roll_step()

    def _roll_step(self):
        elapsed = (datetime.now() - self._roll_start).total_seconds()
        if elapsed < 2.0:
            sample = random.sample(self.pool, min(5, len(self.pool)))
            self.lbl_display.config(text="  |  ".join(sample), fg="#888")
            self.root.after(60, self._roll_step)
        else:
            self._finish_draw()

    def _finish_draw(self):
        t = self._t
        try:
            count = max(1, int(self.spin_count.get()))
        except ValueError:
            count = 1
        count = min(count, len(self.pool))
        winners = random.sample(self.pool, count)

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
        self.btn_draw.config(state=tk.NORMAL, text=t("btn_draw"))

    # ---------------- 记录 ----------------
    def _load_records(self):
        if not os.path.exists(RECORD_FILE):
            return
        try:
            with open(RECORD_FILE, "r", encoding="utf-8-sig", newline="") as f:
                for row in csv.reader(f):
                    if len(row) >= 3 and row[0] != I18N["zh"]["csv_time"] and row[0] != I18N["en_GB"]["csv_time"] and row[0] != I18N["en_US"]["csv_time"]:
                        self.records.append((row[0], int(row[1]), row[2]))
                        self.tree.insert("", tk.END, values=(row[0], row[1], row[2]))
            if self.records:
                self.round_no = max(r[1] for r in self.records)
        except Exception:
            pass

    def _save_record_row(self, time_str, round_no, result_str):
        t = self._t
        need_header = not os.path.exists(RECORD_FILE) or os.path.getsize(RECORD_FILE) == 0
        with open(RECORD_FILE, "a", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            if need_header:
                w.writerow([t("csv_time"), t("csv_round"), t("csv_result")])
            w.writerow([time_str, round_no, result_str])

    def export_records(self):
        t = self._t
        if not self.records:
            messagebox.showwarning(t("msg_confirm"), t("msg_no_records"))
            return
        path = filedialog.asksaveasfilename(
            title=t("dlg_export"),
            defaultextension=".csv",
            initialfile=f"lottery_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            filetypes=[(t("ft_csv"), "*.csv")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow([t("csv_time"), t("csv_round"), t("csv_result")])
                w.writerows(self.records)
            messagebox.showinfo(t("msg_export_success"), t("msg_exported_to").format(path))
        except Exception as e:
            messagebox.showerror(t("msg_export_failed"), str(e))

    def clear_records(self):
        t = self._t
        if not self.records:
            return
        if messagebox.askyesno(t("msg_confirm"), t("msg_clear_records")):
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
