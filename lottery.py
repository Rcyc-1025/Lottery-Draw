# -*- coding: utf-8 -*-
"""
抽奖程序 / Lottery Programme
功能：
  1. 导入 txt 抽奖名单（一行一个选项），名单与奖池自动持久化、重启恢复
  2. 手动添加抽奖项，支持在名单管理中勾选多选、批量改状态/删除
  3. 抽奖（滚动动画），支持设置每次抽取数量
  4. 淘汰模式：中奖者从奖池移除，不会重复中奖
  5. 抽奖记录查询、备注，支持导出记录与剩余抽奖选项（CSV/TXT）
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
LIST_FILE = os.path.join(BASE_DIR, "lottery_list.json")

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
        "btn_manage_list": "名单管理",
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
        "btn_export_pool": "导出剩余选项",
        "btn_clear_records": "清空记录",
        "btn_export_settings": "导出设置",
        "dlg_export_dir": "选择默认导出目录",
        "dlg_export_settings": "导出设置",
        "export_target_records": "抽奖记录导出位置",
        "export_target_pool": "剩余选项导出位置",
        "btn_choose_folder": "选择文件夹",
        "btn_reset_dir": "恢复默认",
        "export_dir_default": "默认（程序目录）",
        "msg_export_dir_set": "已设置为：\n{}",
        "msg_export_dir_default": "已恢复为默认导出位置（程序目录）。",
        "dlg_export_pool": "导出剩余抽奖选项",
        "ft_txt": "文本文件",
        "msg_no_pool": "奖池为空，没有可导出的剩余选项。",
        "msg_pool_exported": "剩余抽奖选项（{} 项）已导出到：\n{}",
        "btn_edit_note": "编辑备注",
        "col_note": "备注",
        "note_title": "编辑备注",
        "note_label": "备注内容（可为空）：",
        "msg_select_record": "请先在表格中选择一条记录。",
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
        "manage_title": "名单管理",
        "col_entry": "选项",
        "col_status": "状态",
        "status_in_pool": "在奖池中",
        "status_eliminated": "已淘汰",
        "status_has_record": "有该选项记录",
        "status_eliminated_record": "已淘汰（有记录）",
        "btn_delete_selected": "删除选中",
        "btn_multi": "多选",
        "btn_multi_exit": "退出多选",
        "btn_check_all": "全选",
        "btn_uncheck_all": "取消全选",
        "col_check": "选择",
        "btn_apply_status": "应用状态",
        "lbl_set_status": "将选中项设为：",
        "msg_status_updated": "已更新 {} 个选项的状态。",
        "lbl_filter": "筛选:",
        "filter_all": "全部",
        "filter_in_pool": "在奖池中",
        "filter_eliminated": "已淘汰",
        "filter_has_record": "有该选项记录",
        "msg_select_entry": "请先在列表中选择选项。",
        "msg_confirm_delete": "确定删除选中的 {} 个选项吗？\n将同时从名单和奖池中移除。",
        "msg_entries_deleted": "已删除 {} 个选项。",
        "msg_manage_empty": "当前名单为空。",
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
        "csv_note": "备注",
        "display_default_after_clear": "请先导入名单",
    },
    "en_GB": {
        "app_title": "Lottery Programme",
        "btn_import": "Import List (txt)",
        "btn_add_manual": "Add Manually",
        "btn_manage_list": "Manage List",
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
        "btn_export_pool": "Export Remaining Entries",
        "btn_clear_records": "Clear Records",
        "btn_export_settings": "Export Settings",
        "dlg_export_dir": "Select default export folder",
        "dlg_export_settings": "Export Settings",
        "export_target_records": "Draw records export location",
        "export_target_pool": "Remaining entries export location",
        "btn_choose_folder": "Choose Folder",
        "btn_reset_dir": "Reset to Default",
        "export_dir_default": "Default (program folder)",
        "msg_export_dir_set": "Set to:\n{}",
        "msg_export_dir_default": "Restored to the default export location (program folder).",
        "dlg_export_pool": "Export Remaining Entries",
        "ft_txt": "Text files",
        "msg_no_pool": "The pool is empty; there are no remaining entries to export.",
        "msg_pool_exported": "Remaining entries ({}) exported to:\n{}",
        "btn_edit_note": "Edit Note",
        "col_note": "Note",
        "note_title": "Edit Note",
        "note_label": "Note (can be left empty):",
        "msg_select_record": "Please select a record in the table first.",
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
        "manage_title": "Manage Name List",
        "col_entry": "Entry",
        "col_status": "Status",
        "status_in_pool": "In pool",
        "status_eliminated": "Eliminated",
        "status_has_record": "Has draw record",
        "status_eliminated_record": "Eliminated (has record)",
        "btn_delete_selected": "Delete Selected",
        "btn_multi": "Multi-select",
        "btn_multi_exit": "Exit Multi-select",
        "btn_check_all": "Select All",
        "btn_uncheck_all": "Deselect All",
        "col_check": "Select",
        "btn_apply_status": "Apply Status",
        "lbl_set_status": "Set selected to:",
        "msg_status_updated": "Updated the status of {} entries.",
        "lbl_filter": "Filter:",
        "filter_all": "All",
        "filter_in_pool": "In pool",
        "filter_eliminated": "Eliminated",
        "filter_has_record": "Has draw record",
        "msg_select_entry": "Please select entries in the list first.",
        "msg_confirm_delete": "Delete the {} selected entries?\nThey will be removed from both the list and the pool.",
        "msg_entries_deleted": "Deleted {} entries.",
        "msg_manage_empty": "The name list is currently empty.",
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
        "csv_note": "Note",
        "display_default_after_clear": "Please import a name list first",
    },
    "en_US": {
        "app_title": "Lottery Program",
        "btn_import": "Import List (txt)",
        "btn_add_manual": "Add Manually",
        "btn_manage_list": "Manage List",
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
        "btn_export_pool": "Export Remaining Entries",
        "btn_clear_records": "Clear Records",
        "btn_export_settings": "Export Settings",
        "dlg_export_dir": "Select default export folder",
        "dlg_export_settings": "Export Settings",
        "export_target_records": "Draw records export location",
        "export_target_pool": "Remaining entries export location",
        "btn_choose_folder": "Choose Folder",
        "btn_reset_dir": "Reset to Default",
        "export_dir_default": "Default (program folder)",
        "msg_export_dir_set": "Set to:\n{}",
        "msg_export_dir_default": "Restored to the default export location (program folder).",
        "dlg_export_pool": "Export Remaining Entries",
        "ft_txt": "Text files",
        "msg_no_pool": "The pool is empty; there are no remaining entries to export.",
        "msg_pool_exported": "Remaining entries ({}) exported to:\n{}",
        "btn_edit_note": "Edit Note",
        "col_note": "Note",
        "note_title": "Edit Note",
        "note_label": "Note (can be left empty):",
        "msg_select_record": "Please select a record in the table first.",
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
        "manage_title": "Manage Name List",
        "col_entry": "Entry",
        "col_status": "Status",
        "status_in_pool": "In pool",
        "status_eliminated": "Eliminated",
        "status_has_record": "Has draw record",
        "status_eliminated_record": "Eliminated (has record)",
        "btn_delete_selected": "Delete Selected",
        "btn_multi": "Multi-select",
        "btn_multi_exit": "Exit Multi-select",
        "btn_check_all": "Select All",
        "btn_uncheck_all": "Deselect All",
        "col_check": "Select",
        "btn_apply_status": "Apply Status",
        "lbl_set_status": "Set selected to:",
        "msg_status_updated": "Updated the status of {} entries.",
        "lbl_filter": "Filter:",
        "filter_all": "All",
        "filter_in_pool": "In pool",
        "filter_eliminated": "Eliminated",
        "filter_has_record": "Has draw record",
        "msg_select_entry": "Please select entries in the list first.",
        "msg_confirm_delete": "Delete the {} selected entries?\nThey will be removed from both the list and the pool.",
        "msg_entries_deleted": "Deleted {} entries.",
        "msg_manage_empty": "The name list is currently empty.",
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
        "csv_note": "Note",
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
        root.geometry("1040x600")
        root.minsize(920, 500)

        self.name_list = []      # 原始名单
        self.pool = []           # 当前奖池（淘汰模式下会减少）
        self.records = []        # [(时间, 轮次, 结果, 备注)]
        self.round_no = 0
        self.rolling = False     # 是否正在滚动抽奖
        self.config = self._load_config()
        self.language = self.config.get("language", "zh")
        # 记录导出与剩余选项导出可分别指定默认目录
        self.export_dir_records = self.config.get("export_dir_records", "") or ""
        self.export_dir_pool = self.config.get("export_dir_pool", "") or ""

        self._build_ui()
        self._refresh_ui_text()
        self._load_records()
        self._load_list()

    # ---------------- 名单持久化 ----------------
    def _load_list(self):
        """启动时恢复上次的名单与奖池，避免每次重新导入。"""
        try:
            if os.path.exists(LIST_FILE):
                with open(LIST_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                names = data.get("name_list", [])
                pool = data.get("pool", [])
                # 简单校验，保证数据结构合法
                if isinstance(names, list) and isinstance(pool, list):
                    names = [str(n) for n in names]
                    names_set = set(names)
                    pool = [str(n) for n in pool if str(n) in names_set]
                    self.name_list = names
                    self.pool = pool
        except Exception:
            pass
        self._refresh_count()
        if self.name_list:
            self.lbl_display.config(text=self._t("msg_imported").format(len(self.name_list)))
        else:
            self.lbl_display.config(text=self._t("display_init"))

    def _save_list(self):
        """保存当前名单与奖池到本地。"""
        try:
            with open(LIST_FILE, "w", encoding="utf-8") as f:
                json.dump({"name_list": self.name_list, "pool": self.pool},
                          f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ---------------- 配置 ----------------
    def _load_config(self):
        """读取本地配置（语言、导出目录等）。"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                if isinstance(cfg, dict):
                    if cfg.get("language") not in I18N:
                        cfg["language"] = "zh"
                    # 兼容旧版单一 export_dir：迁移为两类导出共用同一目录
                    old_dir = cfg.get("export_dir", "") or ""
                    cfg.setdefault("export_dir_records", old_dir)
                    cfg.setdefault("export_dir_pool", old_dir)
                    return cfg
        except Exception:
            pass
        return {"language": "zh", "export_dir_records": "", "export_dir_pool": ""}

    def _save_config(self):
        """写回本地配置。"""
        try:
            self.config["language"] = self.language
            self.config["export_dir_records"] = self.export_dir_records
            self.config["export_dir_pool"] = self.export_dir_pool
            self.config.pop("export_dir", None)  # 清理旧字段
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
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
        self._save_config()
        self._refresh_ui_text()

    def _refresh_ui_text(self):
        """根据当前语言刷新所有界面文本。"""
        t = self._t
        self.root.title(t("app_title"))
        self.btn_import.config(text=t("btn_import"))
        self.btn_add_manual.config(text=t("btn_add_manual"))
        self.btn_manage_list.config(text=t("btn_manage_list"))
        self.btn_clear_list.config(text=t("btn_clear_list"))
        self.lbl_draw_count.config(text=t("lbl_draw_count"))
        self.chk_eliminate.config(text=t("chk_eliminate"))
        self.lbl_language.config(text=t("lbl_language"))
        self.frame_draw.config(text=t("frame_draw"))
        self.frame_records.config(text=t("frame_records"))
        self.btn_export.config(text=t("btn_export"))
        self.btn_export_pool.config(text=t("btn_export_pool"))
        self.btn_export_settings.config(text=t("btn_export_settings"))
        self.btn_edit_note.config(text=t("btn_edit_note"))
        self.btn_clear_records.config(text=t("btn_clear_records"))
        self.tree.heading("time", text=t("col_time"))
        self.tree.heading("round", text=t("col_round"))
        self.tree.heading("result", text=t("col_result"))
        self.tree.heading("note", text=t("col_note"))

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
        self.btn_manage_list = ttk.Button(top, command=self.manage_list)
        self.btn_manage_list.pack(side=tk.LEFT, padx=(6, 0))
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

        cols = ("time", "round", "result", "note")
        self.tree = ttk.Treeview(self.frame_records, columns=cols, show="headings", height=8)
        self.tree.column("time", width=150, anchor=tk.CENTER)
        self.tree.column("round", width=50, anchor=tk.CENTER)
        self.tree.column("result", width=380, anchor=tk.W)
        self.tree.column("note", width=200, anchor=tk.W)
        sb = ttk.Scrollbar(self.frame_records, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.bind("<Double-1>", lambda e: self.edit_note())

        btns = ttk.Frame(self.frame_records)
        btns.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 0))
        self.btn_export = ttk.Button(btns, command=self.export_records)
        self.btn_export.pack(fill=tk.X)
        self.btn_export_pool = ttk.Button(btns, command=self.export_pool)
        self.btn_export_pool.pack(fill=tk.X, pady=(6, 0))
        self.btn_export_settings = ttk.Button(btns, command=self.set_export_dir)
        self.btn_export_settings.pack(fill=tk.X, pady=(6, 0))
        self.btn_edit_note = ttk.Button(btns, command=self.edit_note)
        self.btn_edit_note.pack(fill=tk.X, pady=(6, 0))
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
            self._save_list()
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
            self._save_list()
            self._refresh_count()
            self.lbl_display.config(text=t("msg_added").format(len(added), len(self.name_list)))
            win.destroy()

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text=t("btn_confirm"), command=on_confirm).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text=t("btn_cancel"), command=win.destroy).pack(side=tk.RIGHT, padx=(0, 8))
        win.bind("<Return>", lambda e: on_confirm())

    def _recorded_names(self):
        """从抽奖记录中解析出所有曾中奖的选项名称。"""
        recorded = set()
        for record in self.records:
            result = record[2] if len(record) >= 3 else ""
            for part in result.split("、"):
                part = part.strip()
                if part:
                    recorded.add(part)
        return recorded

    def manage_list(self):
        """打开名单管理窗口：勾选式多选、按状态筛选、批量改状态/删除（同时移出奖池）。"""
        t = self._t
        if not self.name_list:
            messagebox.showinfo(t("manage_title"), t("msg_manage_empty"))
            return

        win = tk.Toplevel(self.root)
        win.title(t("manage_title"))
        win.geometry("600x520")
        win.transient(self.root)
        win.grab_set()

        multi_mode = {"on": False}
        checked = set()  # 被勾选的选项名称（跨筛选保留）

        # 顶部：状态筛选 + 多选切换
        top_bar = ttk.Frame(win, padding=(8, 8, 8, 0))
        top_bar.pack(fill=tk.X)
        ttk.Label(top_bar, text=t("lbl_filter")).pack(side=tk.LEFT)
        # 筛选项：(内部 key, 文案 key)。两个维度——是否在奖池、是否有中奖记录
        filter_keys = ["all", "in_pool", "eliminated", "has_record"]
        filter_options = [t(f"filter_{k}") for k in filter_keys]
        filter_var = tk.StringVar(value=t("filter_all"))
        cmb_filter = ttk.Combobox(top_bar, textvariable=filter_var, state="readonly",
                                  values=filter_options, width=18)
        cmb_filter.pack(side=tk.LEFT, padx=(4, 8))
        btn_multi = ttk.Button(top_bar, text=t("btn_multi"))
        btn_multi.pack(side=tk.RIGHT)

        # 第二行：批量修改勾选项状态
        status_bar = ttk.Frame(win, padding=(8, 4, 8, 0))
        status_bar.pack(fill=tk.X)
        ttk.Label(status_bar, text=t("lbl_set_status")).pack(side=tk.LEFT)
        status_var = tk.StringVar(value=t("status_in_pool"))
        cmb_status = ttk.Combobox(status_bar, textvariable=status_var, state="readonly",
                                  values=[t("status_in_pool"), t("status_eliminated")], width=14)
        cmb_status.pack(side=tk.LEFT, padx=(4, 6))

        # 中部：名单表格（首列为勾选列，仅多选模式显示）
        frame = ttk.Frame(win, padding=8)
        frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=("check", "entry", "status"),
                            show="headings", height=15, selectmode="browse")
        tree.heading("check", text=t("col_check"))
        tree.heading("entry", text=t("col_entry"))
        tree.heading("status", text=t("col_status"))
        tree.column("check", width=50, anchor=tk.CENTER, stretch=False)
        tree.column("entry", width=380, anchor=tk.W)
        tree.column("status", width=170, anchor=tk.CENTER)
        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        # 默认隐藏勾选列
        tree.configure(displaycolumns=("entry", "status"))

        def visible_rows():
            """返回当前筛选后显示的 (iid, name) 列表。"""
            return [(iid, tree.item(iid, "values")[1]) for iid in tree.get_children()]

        def rebuild(*_):
            """按筛选重建列表；多选模式下首列显示勾选框。

            状态由两个正交维度组合：是否在奖池 × 是否有中奖记录，
            避免“有记录”掩盖已被手动淘汰的事实。
            """
            for item in tree.get_children():
                tree.delete(item)
            pool_set = set(self.pool)
            recorded = self._recorded_names()
            # 当前筛选内部 key（通过文案在下拉列表中的位置反查）
            try:
                cur_key = filter_keys[filter_options.index(filter_var.get())]
            except ValueError:
                cur_key = "all"
            show_check = multi_mode["on"]
            for idx, name in enumerate(self.name_list):
                in_pool = name in pool_set
                has_record = name in recorded
                if in_pool:
                    cls = "record_in_pool" if has_record else "in_pool"
                else:
                    cls = "record_eliminated" if has_record else "eliminated"
                # 按筛选维度匹配
                if cur_key == "in_pool" and not in_pool:
                    continue
                if cur_key == "eliminated" and in_pool:
                    continue
                if cur_key == "has_record" and not has_record:
                    continue
                # 显示文案
                if cls == "in_pool":
                    status = t("status_in_pool")
                elif cls == "record_in_pool":
                    status = t("status_has_record")
                elif cls == "record_eliminated":
                    status = t("status_eliminated_record")
                else:
                    status = t("status_eliminated")
                mark = ("☑" if name in checked else "☐") if show_check else ""
                tree.insert("", tk.END, iid=str(idx), values=(mark, name, status))

        def set_multi_mode(on):
            multi_mode["on"] = on
            tree.configure(displaycolumns=("check", "entry", "status") if on else ("entry", "status"))
            btn_multi.config(text=t("btn_multi_exit") if on else t("btn_multi"))
            btn_check_all.config(state=tk.NORMAL if on else tk.DISABLED)
            btn_uncheck_all.config(state=tk.NORMAL if on else tk.DISABLED)
            btn_apply_status.config(state=tk.NORMAL if on else tk.DISABLED)
            btn_delete_selected.config(state=tk.NORMAL if on else tk.DISABLED)
            rebuild()

        def toggle_multi():
            set_multi_mode(not multi_mode["on"])

        def toggle_row(name):
            if name in checked:
                checked.discard(name)
            else:
                checked.add(name)
            rebuild()

        def check_all_visible():
            checked.update(name for _, name in visible_rows())
            rebuild()

        def uncheck_all_visible():
            for _, name in visible_rows():
                checked.discard(name)
            rebuild()

        def on_tree_click(event):
            if not multi_mode["on"]:
                return
            if tree.identify_column(event.x) != "#1":
                return
            row = tree.identify_row(event.y)
            if row:  # 点击某行的勾选框
                toggle_row(tree.item(row, "values")[1])
            elif tree.identify_region(event.x, event.y) == "heading":  # 点击表头：全选/取消
                visible = [name for _, name in visible_rows()]
                if visible and all(n in checked for n in visible):
                    uncheck_all_visible()
                else:
                    check_all_visible()

        def delete_selected():
            if not checked:
                messagebox.showwarning(t("msg_confirm"), t("msg_select_entry"), parent=win)
                return
            if not messagebox.askyesno(t("msg_confirm"),
                                       t("msg_confirm_delete").format(len(checked)), parent=win):
                return
            delete_names = set(checked)
            self.name_list = [n for n in self.name_list if n not in delete_names]
            self.pool = [n for n in self.pool if n not in delete_names]
            checked.clear()
            self._save_list()
            self._refresh_count()
            rebuild()
            if not self.name_list:
                self.lbl_display.config(text=self._t("display_default_after_clear"))
                win.destroy()

        def apply_status():
            """将所有勾选项批量设为指定状态（在奖池中 / 已淘汰）。"""
            if not checked:
                messagebox.showwarning(t("msg_confirm"), t("msg_select_entry"), parent=win)
                return
            target = status_var.get()
            pool_set = set(self.pool)
            if target == t("status_in_pool"):
                for name in checked:
                    if name not in pool_set:
                        self.pool.append(name)
                        pool_set.add(name)
            else:  # 标记为已淘汰：从奖池移除
                self.pool = [n for n in self.pool if n not in checked]
            self._save_list()
            self._refresh_count()
            rebuild()
            messagebox.showinfo(t("manage_title"),
                                t("msg_status_updated").format(len(checked)), parent=win)

        cmb_filter.bind("<<ComboboxSelected>>", rebuild)
        tree.bind("<Button-1>", on_tree_click, add="+")
        btn_multi.config(command=toggle_multi)

        # 底部：批量操作按钮
        btn_frame = ttk.Frame(win, padding=(8, 0, 8, 8))
        btn_frame.pack(fill=tk.X)
        btn_delete_selected = ttk.Button(btn_frame, text=t("btn_delete_selected"),
                                         command=delete_selected, state=tk.DISABLED)
        btn_delete_selected.pack(side=tk.RIGHT)
        btn_apply_status = ttk.Button(btn_frame, text=t("btn_apply_status"),
                                      command=apply_status, state=tk.DISABLED)
        btn_apply_status.pack(side=tk.RIGHT, padx=(0, 8))
        btn_uncheck_all = ttk.Button(btn_frame, text=t("btn_uncheck_all"),
                                     command=uncheck_all_visible, state=tk.DISABLED)
        btn_uncheck_all.pack(side=tk.RIGHT, padx=(0, 8))
        btn_check_all = ttk.Button(btn_frame, text=t("btn_check_all"),
                                   command=check_all_visible, state=tk.DISABLED)
        btn_check_all.pack(side=tk.RIGHT, padx=(0, 8))
        ttk.Button(btn_frame, text=t("btn_cancel"), command=win.destroy).pack(side=tk.LEFT)

        rebuild()
        tree.focus_set()

    def clear_list(self):
        t = self._t
        if messagebox.askyesno(t("msg_confirm"), t("msg_clear_list")):
            self.name_list = []
            self.pool = []
            self._save_list()
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
            self._save_list()  # 淘汰后奖池变化，持久化以便重启恢复

        self.round_no += 1
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_str = "、".join(winners)
        idx = len(self.records)
        self.records.append((time_str, self.round_no, result_str, ""))
        self.tree.insert("", 0, iid=str(idx), values=(time_str, self.round_no, result_str, ""))
        self._save_record_row(time_str, self.round_no, result_str, "")

        self.lbl_display.config(text=result_str, fg="#d40000")
        self._refresh_count()
        self.rolling = False
        self.btn_draw.config(state=tk.NORMAL, text=t("btn_draw"))

    # ---------------- 记录 ----------------
    def _is_header_row(self, first_cell):
        return first_cell in (I18N["zh"]["csv_time"], I18N["en_GB"]["csv_time"], I18N["en_US"]["csv_time"])

    def _load_records(self):
        if not os.path.exists(RECORD_FILE):
            return
        try:
            with open(RECORD_FILE, "r", encoding="utf-8-sig", newline="") as f:
                for row in csv.reader(f):
                    if len(row) < 3 or self._is_header_row(row[0]):
                        continue
                    try:
                        round_no = int(row[1])
                    except ValueError:
                        continue
                    note = row[3] if len(row) >= 4 else ""  # 兼容旧版3列记录
                    idx = len(self.records)
                    self.records.append((row[0], round_no, row[2], note))
                    self.tree.insert("", tk.END, iid=str(idx),
                                     values=(row[0], round_no, row[2], note))
            if self.records:
                self.round_no = max(r[1] for r in self.records)
        except Exception:
            pass

    def _save_record_row(self, time_str, round_no, result_str, note):
        t = self._t
        need_header = not os.path.exists(RECORD_FILE) or os.path.getsize(RECORD_FILE) == 0
        with open(RECORD_FILE, "a", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            if need_header:
                w.writerow([t("csv_time"), t("csv_round"), t("csv_result"), t("csv_note")])
            w.writerow([time_str, round_no, result_str, note])

    def _rewrite_records_file(self):
        """用内存中的全部记录重写文件（编辑备注后调用）。"""
        t = self._t
        with open(RECORD_FILE, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow([t("csv_time"), t("csv_round"), t("csv_result"), t("csv_note")])
            w.writerows(self.records)

    def edit_note(self):
        """为选中的中奖记录添加/修改备注（双击行或点按钮触发）。"""
        t = self._t
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(t("msg_confirm"), t("msg_select_record"))
            return
        idx = int(selection[0])
        time_str, round_no, result_str, old_note = self.records[idx]

        win = tk.Toplevel(self.root)
        win.title(t("note_title"))
        win.geometry("460x260")
        win.transient(self.root)
        win.grab_set()

        ttk.Label(win, text=f"#{round_no}  {result_str}").pack(anchor=tk.W, padx=10, pady=(10, 2))
        ttk.Label(win, text=t("note_label")).pack(anchor=tk.W, padx=10, pady=(4, 2))
        text = tk.Text(win, height=5, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))
        text.insert("1.0", old_note)
        text.focus_set()

        def on_confirm():
            note = text.get("1.0", tk.END).strip()
            self.records[idx] = (time_str, round_no, result_str, note)
            self.tree.item(str(idx), values=(time_str, round_no, result_str, note))
            self._rewrite_records_file()
            win.destroy()

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text=t("btn_confirm"), command=on_confirm).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text=t("btn_cancel"), command=win.destroy).pack(side=tk.RIGHT, padx=(0, 8))
        win.bind("<Control-Return>", lambda e: on_confirm())

    def export_records(self):
        t = self._t
        if not self.records:
            messagebox.showwarning(t("msg_confirm"), t("msg_no_records"))
            return
        opts = dict(
            title=t("dlg_export"),
            defaultextension=".csv",
            initialfile=f"lottery_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            filetypes=[(t("ft_csv"), "*.csv")],
        )
        # 抽奖记录的自定义默认导出目录
        if self.export_dir_records and os.path.isdir(self.export_dir_records):
            opts["initialdir"] = self.export_dir_records
        path = filedialog.asksaveasfilename(**opts)
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow([t("csv_time"), t("csv_round"), t("csv_result"), t("csv_note")])
                w.writerows(self.records)
            messagebox.showinfo(t("msg_export_success"), t("msg_exported_to").format(path))
        except Exception as e:
            messagebox.showerror(t("msg_export_failed"), str(e))

    def _remaining_entries(self):
        """返回仍可参与抽奖的选项：按名单顺序，仅保留当前在奖池中的项。

        已淘汰（无论是否有中奖记录）的选项不在奖池中，一律排除。
        """
        pool_set = set(self.pool)
        return [name for name in self.name_list if name in pool_set]

    def export_pool(self):
        """导出剩余抽奖选项为 txt（一行一个，可直接再次导入；不含已淘汰项）。"""
        t = self._t
        remaining = self._remaining_entries()
        if not remaining:
            messagebox.showwarning(t("msg_confirm"), t("msg_no_pool"))
            return
        opts = dict(
            title=t("dlg_export_pool"),
            defaultextension=".txt",
            initialfile=f"lottery_pool_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            filetypes=[(t("ft_text"), "*.txt"), (t("ft_all"), "*.*")],
        )
        # 剩余选项的自定义默认导出目录
        if self.export_dir_pool and os.path.isdir(self.export_dir_pool):
            opts["initialdir"] = self.export_dir_pool
        path = filedialog.asksaveasfilename(**opts)
        if not path:
            return
        try:
            # utf-8-sig 保证 Windows 记事本/Excel 正确识别，格式与导入一致（一行一个）
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                f.write("\n".join(remaining) + "\n")
            messagebox.showinfo(t("msg_export_success"),
                                t("msg_pool_exported").format(len(remaining), path))
        except Exception as e:
            messagebox.showerror(t("msg_export_failed"), str(e))

    def set_export_dir(self):
        """打开导出设置窗口：分别设置“抽奖记录”和“剩余选项”的默认保存位置。"""
        t = self._t
        win = tk.Toplevel(self.root)
        win.title(t("dlg_export_settings"))
        win.geometry("620x230")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        # 每一行：用途标题 + 当前路径 + 选择/重置按钮
        def build_row(parent, title_key, get_dir, set_dir):
            ttk.Label(parent, text=t(title_key), font=(None, 10, "bold")).pack(anchor=tk.W)
            line = ttk.Frame(parent)
            line.pack(fill=tk.X, pady=(2, 6))
            lbl_path = ttk.Label(line, text="")
            lbl_path.pack(side=tk.LEFT, fill=tk.X, expand=True)

            def refresh():
                d = get_dir()
                lbl_path.config(text=d if d and os.path.isdir(d) else t("export_dir_default"))

            def choose():
                path = filedialog.askdirectory(
                    title=t("dlg_export_dir"),
                    initialdir=get_dir() if get_dir() and os.path.isdir(get_dir()) else BASE_DIR,
                    parent=win,
                )
                if path:
                    set_dir(path)
                    self._save_config()
                    refresh()
                    messagebox.showinfo(t("dlg_export_settings"),
                                        t("msg_export_dir_set").format(path), parent=win)

            def reset():
                set_dir("")
                self._save_config()
                refresh()
                messagebox.showinfo(t("dlg_export_settings"),
                                    t("msg_export_dir_default"), parent=win)

            ttk.Button(line, text=t("btn_reset_dir"), command=reset, width=10).pack(side=tk.RIGHT)
            ttk.Button(line, text=t("btn_choose_folder"), command=choose, width=12).pack(
                side=tk.RIGHT, padx=(0, 8))
            refresh()

        body = ttk.Frame(win, padding=14)
        body.pack(fill=tk.BOTH, expand=True)
        build_row(body, "export_target_records",
                  lambda: self.export_dir_records,
                  lambda p: setattr(self, "export_dir_records", p))
        build_row(body, "export_target_pool",
                  lambda: self.export_dir_pool,
                  lambda p: setattr(self, "export_dir_pool", p))
        ttk.Button(body, text=t("btn_cancel"), command=win.destroy).pack(side=tk.RIGHT, pady=(8, 0))

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
