import csv
import tkinter as tk
from tkinter import ttk, filedialog

RESOURCE_NODES = ["鉄鉱石", "銅鉱石", "石灰岩", "石炭", "カテリウム鉱石", "未加工石英", "硫黄", "原油", "SAM", "間欠泉", "ボーキサイト", "水", "窒素ガス", "ウラン", "石英", "菌糸", "バイオマス", "合成樹脂", "廃重油", "固体バイオ燃料", "コンクリート", "ゴム", "プラスチック", "ヘビー・モジュ・フレ", "アルミナ溶液", "鉄ロッド", "強化鉄板", "ローター", "固定子", "スパコン", "高速コネクター", "電磁制御棒", "水晶発振器", "コンピュータ", "AIリミッタ", "多目的フレーム", "自動ワイヤー", "回路基板", "クイックワイヤー", "ケーブル", "ワイヤー", "鋼梁", "コンクリート", "石英結晶", "シリカ", "アルミインゴット", "鉄インゴット", "銅インゴット", "鋼鉄インゴット"]
PURITY_MAP = {"低純度": 0.5, "中純度": 1.0, "高純度": 2.0}
NODE_MACHINES = {"採鉱機Mk1": 60, "採鉱機Mk2": 120, "採鉱機Mk3": 180, "原油抽出機": 120, "資源抽出機": 60, "地熱発電機": 200}
RECIPE_TABLES = {
    "製錬炉": [
        {"生産物": "鉄インゴット", "生産量": 30, "副産物":"", "副産物量": 0, "消費": [("鉄鉱石", 30)]},
        {"生産物": "銅インゴット", "生産量": 30, "副産物":"", "副産物量": 0, "消費": [("銅鉱石", 30)]},
        {"生産物": "カテリウムインゴット", "生産量": 45, "副産物":"", "副産物量": 0, "消費": [("カテリウム鉱石", 15)]}
    ],
    "鋳造炉": [
        {"生産物": "鋼鉄インゴット", "生産量": 45, "副産物":"", "副産物量": 0, "消費": [("鉄鉱石", 45), ("石炭", 45)]},
        {"生産物": "アルミインゴット", "生産量": 60, "副産物":"", "副産物量": 0, "消費": [("アルミスクラップ", 90), ("シリカ", 75)]}
    ],
    "製作機": [
        {"生産物": "鉄板", "生産量": 20, "副産物":"", "副産物量": 0, "消費": [("鉄インゴット", 30)]},
        {"生産物": "鉄のロッド", "生産量": 15, "副産物":"", "副産物量": 0, "消費": [("鉄インゴット", 15)]},
        {"生産物": "ネジ", "生産量": 40, "副産物":"", "副産物量": 0, "消費": [("鉄ロッド", 10)]},
        {"生産物": "代替:鋳造ネジ", "生産量": 50, "副産物":"", "副産物量": 0, "消費": [("鉄インゴット", 12.5)]},
        {"生産物": "代替:鋼鉄ネジ", "生産量": 260, "副産物":"", "副産物量": 0, "消費": [("鋼梁", 5)]},
        {"生産物": "代替:鋼管", "生産量": 25, "副産物":"", "副産物量": 0, "消費": [("鉄インゴット", 100)]},
        {"生産物": "鋼梁", "生産量": 15, "副産物":"", "副産物量": 0, "消費": [("鋼鉄インゴット", 60)]},
        {"生産物": "鋼管", "生産量": 20, "副産物":"", "副産物量": 0, "消費": [("鋼鉄インゴット", 30)]},
        {"生産物": "銅板", "生産量": 10, "副産物":"", "副産物量": 0, "消費": [("銅インゴット", 20)]},
        {"生産物": "ワイヤー", "生産量": 30, "副産物":"", "副産物量": 0, "消費": [("銅インゴット", 15)]},
        {"生産物": "代替:ワイヤー", "生産量": 120, "副産物":"", "副産物量": 0, "消費": [("カテ・インゴット", 15)]},
        {"生産物": "ケーブル", "生産量": 30, "副産物":"", "副産物量": 0, "消費": [("ワイヤー", 60)]},
        {"生産物": "クイックワイヤー", "生産量": 60, "副産物":"", "副産物量": 0, "消費": [("カテ・インゴット", 12)]},
        {"生産物": "活性SAM", "生産量": 30, "副産物":"", "副産物量": 0, "消費": [("SAM", 120)]},
        {"生産物": "コンクリート", "生産量": 15, "副産物":"", "副産物量": 0, "消費": [("石灰岩", 45)]},
        {"生産物": "石英結晶", "生産量": 22.5, "副産物":"", "副産物量": 0, "消費": [("石英", 37.5)]},
        {"生産物": "シリカ", "生産量": 37.5, "副産物":"", "副産物量": 0, "消費": [("石英", 22.5)]},
        {"生産物": "空容器", "生産量": 60, "副産物":"", "副産物量": 0, "消費": [("プラスチック", 30)]},
        {"生産物": "代替:空容器", "生産量": 40, "副産物":"", "副産物量": 0, "消費": [("鋼鉄インゴット", 40)]},
        {"生産物": "アルミ筐体", "生産量": 60, "副産物":"", "副産物量": 0, "消費": [("アルミインゴット", 90)]},
        {"生産物": "空の液体タンク", "生産量": 60, "副産物":"", "副産物量": 0, "消費": [("アルミインゴット", 60)]}
    ],
    "組立機": [
        {"生産物": "ロータ", "生産量": 4, "副産物":"", "副産物量": 0, "消費": [("鉄ロット", 20), ("ネジ", 100)]},
        {"生産物": "代替:鋼鉄ロータ", "生産量": 5, "副産物":"", "副産物量": 0, "消費": [("鋼管", 10), ("ワイヤー", 30)]},
        {"生産物":"固定子", "生産量": 5, "副産物":"", "副産物量": 0, "消費": [("鋼管", 15), ("ワイヤー", 40)]},
        {"生産物":"モーター", "生産量": 5, "副産物":"", "副産物量": 0, "消費": [("ローター", 10), ("固定子", 10)]},
        {"生産物":"布地", "生産量": 15, "副産物":"", "副産物量": 0, "消費": [("菌糸", 15), ("バイオマス", 75)]},
        {"生産物":"圧縮石炭", "生産量": 25, "副産物":"", "副産物量": 0, "消費": [("石炭", 25), ("硫黄", 25)]},
        {"生産物":"代替:圧縮石炭", "生産量": 25, "副産物":"", "副産物量": 0, "消費": [("石炭", 25), ("硫黄", 25)]},
        {"生産物":"強化鉄板", "生産量": 5, "副産物":"", "副産物量": 0, "消費": [("鉄板", 30), ("ネジ", 60)]},
        {"生産物":"代替:強化鉄板", "生産量": 5.625, "副産物":"", "副産物量": 0, "消費": [("鉄板", 18.75), ("ワイヤー", 37.5)]},
        {"生産物":"モジュ・フレーム", "生産量": 2, "副産物":"", "副産物量": 0, "消費": [("強化鉄板", 3), ("鉄ロッド", 12)]},
        {"生産物":"被覆型銅梁", "生産量": 6, "副産物":"", "副産物量": 0, "消費": [("鋼梁", 18), ("コンクリート", 36)]},
        {"生産物":"スマ・プレート", "生産量": 2, "副産物":"", "副産物量": 0, "消費": [("強化鉄板", 2), ("ローター", 2)]},
        {"生産物":"多目的フレーム", "生産量": 5, "副産物":"", "副産物量": 0, "消費": [("鋼梁", 30), ("モジュ・フレーム", 2.5)]},
        {"生産物":"自動ワイヤー", "生産量": 2.5, "副産物":"", "副産物量": 0, "消費": [("固定子", 2.5), ("ケーブル", 50)]},
        {"生産物":"回路基板", "生産量": 7.5, "副産物":"", "副産物量": 0, "消費": [("銅板", 15), ("プラスチック", 30)]},
        {"生産物":"代替:回路基板", "生産量": 8.75, "副産物":"", "副産物量": 0, "消費": [("プラスチック", 12.5), ("クイックワイヤー", 37.5)]},
        {"生産物":"AIリミッタ", "生産量": 5, "副産物":"", "副産物量": 0, "消費": [("銅板", 25), ("クイックワイヤー", 100)]},
        {"生産物":"代替:コンピュータ", "生産量": 3.333, "副産物":"", "副産物量": 0, "消費": [("回路基板", 5), ("水晶発振器", 1.667)]},
        {"生産物":"アルクラッド・アルミ", "生産量": 30, "副産物":"", "副産物量": 0, "消費": [("アルミインゴット", 30), ("銅インゴット", 10)]},
        {"生産物":"ヒートシンク", "生産量": 7.5, "副産物":"", "副産物量": 0, "消費": [("アルクラッド・アルミ", 37.5), ("銅板", 22.5)]},
        {"生産物":"電磁制御棒", "生産量": 4, "副産物":"", "副産物量": 0, "消費": [("固定子", 6), ("AIリミッタ", 4)]},
        {"生産物":"磁界発生装置", "生産量": 1, "副産物":"", "副産物量": 0, "消費": [("多目的フレーム", 2.5), ("電磁制御棒", 1)]},
        {"生産物":"組立指揮システム", "生産量": 0.75, "副産物":"", "副産物量": 0, "消費": [("自律制御ユニット", 1.5), ("スパコン", 0.75)]},
        {"生産物":"黒色火薬", "生産量": 30, "副産物":"", "副産物量": 0, "消費": [("石炭", 15), ("硫黄", 15)]}
    ],
    "製造機": [
        {"生産物":"代替:多目的フレーム", "生産量": 7.5, "副産物":"", "副産物量": 0, "消費": [("モジュ・フレーム", 3.75), ("鋼梁", 22.5), ("ゴム", 30)]},
        {"生産物":"代替:自動ワイヤー", "生産量": 7.5, "副産物":"", "副産物量": 0, "消費": [("固定子", 3.75), ("ワイヤー", 75), ("高速コネクター", 1.875)]},
        {"生産物":"モジュラエンジン", "生産量": 1, "副産物":"", "副産物量": 0, "消費": [("モーター", 2), ("スマ・プレート", 2), ("ゴム", 15)]},
        {"生産物":"自律制御ユニット", "生産量": 1, "副産物":"", "副産物量": 0, "消費": [("自動ワイヤー", 5), ("回路基板", 5), ("ヘビーモジュラー", 1), ("コンピュータ", 1)]},
        {"生産物":"ヘビーモジュラー", "生産量": 2, "副産物":"", "副産物量": 0, "消費": [("モジュ・フレーム", 10), ("鋼管", 40), ("被覆型銅梁", 10), ("ネジ", 240)]},
        {"生産物":"高速コネクタ", "生産量": 3.75, "副産物":"", "副産物量": 0, "消費": [("クイックワイヤ", 210), ("ケーブル", 37.5), ("回路基板", 3)]},
        {"生産物":"コンピュータ", "生産量": 2.5, "副産物":"", "副産物量": 0, "消費": [("回路基板", 10), ("ケーブル", 20), ("プラスチック", 40)]},
        {"生産物":"水晶発振器", "生産量": 1, "副産物":"", "副産物量": 0, "消費": [("石英結晶", 18), ("ケーブル", 14), ("強化鉄板", 2.5)]},
        {"生産物":"代替:水晶発振器", "生産量": 1.875, "副産物":"", "副産物量": 0, "消費": [("石英結晶", 18.75), ("ゴム", 13.125), ("AIリミッタ", 1.875)]},
        {"生産物":"スパコン", "生産量": 1.875, "副産物":"", "副産物量": 0, "消費": [("コンピュータ", 7.5), ("AIリミッタ", 3.75), ("高速コネクタ", 5.625), ("プラスチック", 20)]},
        {"生産物":"無線制御ユニット", "生産量": 2.5, "副産物":"", "副産物量": 0, "消費": [("アルミ筐体", 40), ("水晶発振器", 1.25), ("コンピュータ", 2.5)]},
        {"生産物":"SAM変動器", "生産量": 10, "副産物":"", "副産物量": 0, "消費": [("活性SAM", 60), ("ワイヤー", 50), ("鋼管", 30)]},
        {"生産物":"ウラン燃料棒", "生産量": 0.4, "副産物":"", "副産物量": 0, "消費": [("被覆型ウラン・セル", 20), ("コンクリート被覆型", 1.2), ("電磁制御棒", 2)]}
    ],
    "精製機": [
        {"生産物":"プラスチック", "生産量": 20, "副産物":"廃重油", "副産物量": 10, "消費": [("原油", 30)]},
        {"生産物":"残留プラスチック", "生産量": 20, "副産物":"", "副産物量": 0, "消費": [("合成樹脂", 60), ("水", 20)]},
        {"生産物":"代替:合成樹脂", "生産量": 130, "副産物":"廃重油", "副産物量": 20, "消費": [("原油", 60)]},
        {"生産物":"ゴム", "生産量": 20, "副産物":"廃重油", "副産物量": 20, "消費": [("原油", 30)]},
        {"生産物":"残留ゴム", "生産量": 20, "副産物":"", "副産物量": 0, "消費": [("合成樹脂", 40), ("水", 40)]},
        {"生産物":"石油コークス", "生産量": 120, "副産物":"", "副産物量": 0, "消費": [("廃重油", 40)]},
        {"生産物":"アルミナ溶液", "生産量": 120, "副産物":"シリカ", "副産物量": 50, "消費": [("ボーキサイト", 120), ("水", 180)]},
        {"生産物":"アルミスクラップ", "生産量": 360, "副産物":"水", "副産物量": 120, "消費": [("アルミナ溶液", 240), ("石炭", 120)]},
        {"生産物":"硫酸", "生産量": 50, "副産物":"", "副産物量": 0, "消費": [("硫黄", 50), ("水", 50)]},
        {"生産物":"燃料-橙", "生産量": 40, "副産物":"合成樹脂", "副産物量": 30, "消費": [("原油", 60)]},
        {"生産物":"残留燃料-橙", "生産量": 40, "副産物":"", "副産物量": 0, "消費": [("廃重油", 60)]},
        {"生産物":"液体バイオ燃料", "生産量": 60, "副産物":"", "副産物量": 0, "消費": [("固体バイオ燃料", 90), ("水", 45)]},
        {"生産物":"ターボ燃料", "生産量": 18.75, "副産物":"", "副産物量": 0, "消費": [("残留燃料-橙", 22.5), ("圧縮石炭", 15)]},
        {"生産物":"布地", "生産量": 30, "副産物":"", "副産物量": 0, "消費": [("合成樹脂", 30), ("水", 30)]},
        {"生産物":"無煙火薬", "生産量": 20, "副産物":"黒色火薬", "副産物量": 20, "消費": [("廃重油", 10)]}
    ],
    "混合機": [
        {"生産物":"冷却システム", "生産量": 6, "副産物":"", "副産物量": 0, "消費": [("ヒートシンク", 12), ("ゴム", 12), ("水", 30), ("窒素ガス", 150)]},
        {"生産物":"溶融モジュ・フレ", "生産量": 1.5, "副産物":"", "副産物量": 0, "消費": [("ヘビー・モジュ・フレ", 1.5), ("アルミ筐体", 75), ("窒素ガス", 37.5)]},
        {"生産物":"バッテリ", "生産量": 20, "副産物":"", "副産物量": 0, "消費": [("硫酸", 50), ("アルミナ溶液", 40), ("アルミ筐体", 20)]},
        {"生産物":"被覆型ウランセル", "生産量": 25, "副産物":"", "副産物量": 0, "消費": [("ウラン", 50), ("コンクリート", 15), ("硫酸", 40)]}
    ]
}
ALL_MACHINES = list(NODE_MACHINES.keys()) + list(RECIPE_TABLES.keys())
COLUMNS = ("machine", "purity", "target", "amount", "fuku", "fuku_num", "cons_mat1", "cons_num1", "cons_mat2", "cons_num2", "cons_mat3", "cons_num3", "cons_mat4", "cons_num4")
HEADERS = {"machine": "設置機", "purity": "ノード純度", "target": "生産物", "amount": "生産量/分", "fuku": "副産物", "fuku_num": "副産物量", "cons_mat1": "消費物1", "cons_num1": "消費量1", "cons_mat2": "消費物2", "cons_num2": "消費量2", "cons_mat3": "消費物3", "cons_num3": "消費量3", "cons_mat4": "消費物4", "cons_num4": "消費量4"}


class SatisfactoryProductionPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Satisfactory 生産ライン計算機")
        self.root.geometry("1280x580")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.input_frame = ttk.LabelFrame(self.root, text=" 編集コントロール ", padding="10")
        self.input_frame.pack(fill=tk.X, padx=15, pady=10)

        self.cb_machine = ttk.Combobox(self.input_frame, values=ALL_MACHINES, state="readonly", width=15)
        self.cb_machine.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_dynamic1 = ttk.Label(self.input_frame, text="生産物/ノード:")
        self.lbl_dynamic1.grid(row=0, column=2, padx=5, pady=5)

        self.cb_dynamic1 = ttk.Combobox(self.input_frame, state="readonly", width=18)
        self.cb_dynamic1.grid(row=0, column=3, padx=5, pady=5)

        self.lbl_purity = ttk.Label(self.input_frame, text="")
        self.lbl_purity.grid(row=0, column=4, padx=5, pady=5)

        self.cb_purity = ttk.Combobox(self.input_frame, values=list(PURITY_MAP.keys()), state="readonly", width=10)
        self.cb_purity.grid(row=0, column=5, padx=5, pady=5)

        self.table_frame = ttk.Frame(self.root, padding="10")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL)
        self.scrollbar_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=COLUMNS,
            show="headings",
            selectmode="browse",
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set,
        )
        self.scrollbar_y.config(command=self.tree.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x.config(command=self.tree.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in COLUMNS:
            self.tree.heading(col, text=HEADERS[col], anchor=tk.CENTER)
            self.tree.column(col, width=95, anchor=tk.CENTER)

        self.cb_machine.bind("<<ComboboxSelected>>", self.on_machine_selected)

        ttk.Button(self.input_frame, text="追加", command=self.add_row).grid(row=0, column=6, padx=5)
        ttk.Button(self.input_frame, text="▲上へ", command=self.move_up).grid(row=0, column=7, padx=2)
        ttk.Button(self.input_frame, text="▼下へ", command=self.move_down).grid(row=0, column=8, padx=2)
        ttk.Button(self.input_frame, text="削除", command=self.delete_row).grid(row=0, column=9, padx=5)
        ttk.Button(self.input_frame, text="💾保存", command=self.save_csv).grid(row=0, column=10, padx=5)
        ttk.Button(self.input_frame, text="📂読込", command=self.load_csv).grid(row=0, column=11, padx=5)

    def on_machine_selected(self, event=None):
        m = self.cb_machine.get()
        self.cb_dynamic1.set("")
        self.cb_purity.set("")
        if m in NODE_MACHINES:
            self.lbl_dynamic1.config(text="資源ノード:")
            self.cb_dynamic1.config(values=RESOURCE_NODES)
            self.lbl_purity.config(text="純度:")
            self.cb_purity.config(state="readonly")
        else:
            self.lbl_dynamic1.config(text="生産物:")
            self.cb_dynamic1.config(values=[r["生産物"] for r in RECIPE_TABLES.get(m, [])])
            self.lbl_purity.config(text="")
            self.cb_purity.config(state="disabled")

    def add_row(self):
        m, t, p = self.cb_machine.get(), self.cb_dynamic1.get(), self.cb_purity.get()
        if not m or not t:
            return

        row = {
            "m": m,
            "p": p if p else "",
            "t": t,
            "a": "",
            "f": "",
            "fn": "",
            "m1": "",
            "n1": "",
            "m2": "",
            "n2": "",
            "m3": "",
            "n3": "",
            "m4": "",
            "n4": "",
        }

        if m in NODE_MACHINES:
            if not p:
                return
            row["a"] = str(NODE_MACHINES[m] * PURITY_MAP[p])
        else:
            rcp = next((r for r in RECIPE_TABLES.get(m, []) if r["生産物"] == t), None)
            if rcp:
                row["a"] = str(rcp["生産量"])
                row["f"] = str(rcp["副産物"])
                row["fn"] = "" if row["f"] == "" else str(rcp["副産物量"])
                c_list = rcp.get("消費", [])
                for i in range(min(4, len(c_list))):
                    row[f"m{i + 1}"], row[f"n{i + 1}"] = c_list[i][0], str(c_list[i][1])

        self.tree.insert(
            "",
            tk.END,
            values=(
                row["m"],
                row["p"],
                row["t"],
                row["a"],
                row["f"],
                row["fn"],
                row["m1"],
                row["n1"],
                row["m2"],
                row["n2"],
                row["m3"],
                row["n3"],
                row["m4"],
                row["n4"],
            ),
        )

    def delete_row(self):
        for item in self.tree.selection():
            self.tree.delete(item)

    def move_up(self):
        for item in self.tree.selection():
            idx = self.tree.index(item)
            if idx > 0:
                self.tree.move(item, self.tree.parent(item), idx - 1)

    def move_down(self):
        for item in reversed(self.tree.selection()):
            idx = self.tree.index(item)
            if idx < len(self.tree.get_children()) - 1:
                self.tree.move(item, self.tree.parent(item), idx + 1)

    def save_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        with open(path, mode="w", encoding="utf_8_sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([HEADERS[c] for c in COLUMNS])
            for x in self.tree.get_children():
                writer.writerow(self.tree.item(x)["values"])

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path:
            return
        for x in self.tree.get_children():
            self.tree.delete(x)
        with open(path, mode="r", encoding="utf_8_sig") as f:
            rdr = csv.reader(f)
            next(rdr, None)
            for r in rdr:
                if r:
                    self.tree.insert("", tk.END, values=r)


if __name__ == "__main__":
    root = tk.Tk()
    app = SatisfactoryProductionPlanner(root)
    root.mainloop()
