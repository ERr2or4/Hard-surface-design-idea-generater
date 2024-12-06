import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import random
import json

# 初始化关键词分类
keywords = {
    "风格": [("拟真", 1), ("近未来", 1), ("超现实", 1), ("写实", 1), ("参数化", 1), ("复古", 1), ("文化", 1), ("太空歌剧", 1)],
    "可得性": [("稀缺", 1), ("定制", 1), ("量产", 1), ("日用", 1), ("限量", 1), ("开源", 1)],
    "使用频率": [("工业耗材", 1), ("重度使用", 1), ("定期使用", 1), ("一次性", 1), ("多用途", 1), ("特定场景", 1), ("通用", 1)],
    "耐用性": [("易碎", 1), ("户外", 1), ("标准件", 1), ("展品", 1), ("实验性", 1), ("原型", 1), ("极端", 1), ("回收", 1), ("自修复", 1)],
    "类型": [("商品", 1), ("工具", 1), ("义肢", 1), ("载具", 1), ("电脑", 1), ("PPE", 1), ("防护", 1), ("装备", 1), ("医疗", 1), ("娱乐", 1), ("战术", 1)],
    "外观特征": [("透明", 1), ("复古", 1), ("重工业", 1), ("机械联动", 1), ("齿轮", 1), ("光纤", 1), ("能量场", 1), ("生物", 1), ("模拟", 1), ("EDC", 1),
              ("电路", 1), ("动态", 1), ("情绪", 1), ("混搭", 1)],
    "重点倾向": [("内构", 1), ("外饰", 1), ("功能", 1), ("隐蔽", 1), ("美学", 1), ("叙事", 1)],
    "特殊词条": [("蒙太奇", 1), ("类比", 1), ("拟物", 1), ("讽刺", 1), ("荒谬", 1), ("哲学/伦理设计", 1), ("隐喻", 1), ("跨领域", 1), ("乌托邦/反乌托邦", 1)]
}

# 保存配置到文件
def save_config():
    filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON文件", "*.json")])
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(keywords, f, ensure_ascii=False)
        messagebox.showinfo("保存成功", f"配置已保存到 {filepath}")

# 加载配置文件
def load_config():
    global keywords
    filepath = filedialog.askopenfilename(filetypes=[("JSON文件", "*.json")])
    if filepath:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                keywords = json.load(f)
            refresh_categories()
            refresh_main_categories()
            messagebox.showinfo("加载成功", f"配置已从 {filepath} 加载")
        except Exception as e:
            messagebox.showerror("加载失败", f"加载文件失败：{str(e)}")

# 刷新分类列表
def refresh_categories():
    category_tree.delete(*category_tree.get_children())
    for category, words in keywords.items():
        category_tree.insert("", "end", iid=category, text=category, values=(len(words),))
        for word, weight in words:
            category_tree.insert(category, "end", text=word, values=(weight,))

def refresh_main_categories():
    for widget in categories_frame.winfo_children():
        widget.destroy()
    for category in keywords:
        var = tk.BooleanVar()
        checkboxes[category] = var
        ttk.Checkbutton(categories_frame, text=category, variable=var).pack(anchor="w")

def add_category():
    new_category = simpledialog.askstring("添加分类", "请输入新的分类名称：")
    if new_category:
        if new_category in keywords:
            messagebox.showwarning("分类已存在", f"分类 '{new_category}' 已存在！")
        else:
            keywords[new_category] = []
            refresh_categories()
            refresh_main_categories()
            messagebox.showinfo("成功", f"分类 '{new_category}' 添加成功！")

def delete_category():
    selected_item = category_tree.selection()
    if selected_item:
        selected_category = selected_item[0]
        if selected_category in keywords:
            del keywords[selected_category]
            refresh_categories()
            refresh_main_categories()

def add_keyword():
    selected_item = category_tree.selection()
    if not selected_item:
        messagebox.showwarning("未选择分类", "请先选择一个分类！")
        return
    selected_category = selected_item[0]
    if selected_category not in keywords:
        messagebox.showwarning("无效操作", "请选择一个有效分类！")
        return
    new_keyword = simpledialog.askstring("添加关键词", f"请输入要添加到 '{selected_category}' 的关键词：")
    if new_keyword:
        weight = simpledialog.askinteger("设置权重", f"为 '{new_keyword}' 设置权重（默认1）：", initialvalue=1, minvalue=1)
        keywords[selected_category].append((new_keyword, weight))
        refresh_categories()

def delete_keyword():
    selected_item = category_tree.selection()
    if not selected_item:
        messagebox.showwarning("未选择关键词", "请先选择一个关键词！")
        return
    parent = category_tree.parent(selected_item[0])
    if parent in keywords:
        keyword = category_tree.item(selected_item[0])['text']
        keywords[parent] = [k for k in keywords[parent] if k[0] != keyword]
        refresh_categories()

def generate_keywords():
    selected_categories = [cat for cat, var in checkboxes.items() if var.get()]
    if not selected_categories:
        result_label.config(text="请选择至少一个关键词类别！")
        return
    try:
        num_keywords = int(num_keywords_entry.get())
    except ValueError:
        result_label.config(text="请输入有效的数字！")
        return

    generated = []
    for _ in range(num_keywords):
        category = random.choice(selected_categories)
        words = keywords[category]
        choices = [word for word, weight in words for _ in range(weight)]
        generated.append(random.choice(choices))

    result_label.config(text="，".join(generated))

# 主窗口设计
root = tk.Tk()
root.title("硬表面建模词条生成器")
root.geometry("800x600")

# 主布局
main_paned = ttk.PanedWindow(root, orient="horizontal")
main_paned.pack(fill="both", expand=True)

# 左侧：设置与管理
settings_frame = ttk.LabelFrame(main_paned, text="设置与管理")
main_paned.add(settings_frame, weight=1)

# 分类和关键词显示
category_tree = ttk.Treeview(settings_frame, columns=("count",), show="tree headings", selectmode="browse")
category_tree.heading("#0", text="分类 / 关键词")
category_tree.heading("count", text="权重 / 数量")
category_tree.pack(fill="both", expand=True, padx=5, pady=5)
category_count = {category: {"fixed": 3, "random": False} for category in keywords.keys()}

# 设置按钮
# 调整工具栏布局
button_frame = ttk.Frame(settings_frame)
button_frame.pack(fill="x", padx=5, pady=5)

# 工具栏按钮
ttk.Button(button_frame, text="添加分类", command=add_category).grid(row=0, column=0, padx=2, pady=2, sticky="ew")
ttk.Button(button_frame, text="删除分类", command=delete_category).grid(row=0, column=1, padx=2, pady=2, sticky="ew")
ttk.Button(button_frame, text="添加关键词", command=add_keyword).grid(row=0, column=2, padx=2, pady=2, sticky="ew")
ttk.Button(button_frame, text="删除关键词", command=delete_keyword).grid(row=0, column=3, padx=2, pady=2, sticky="ew")
ttk.Button(button_frame, text="保存配置", command=save_config).grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky="ew")
ttk.Button(button_frame, text="加载配置", command=load_config).grid(row=1, column=2, columnspan=2, padx=2, pady=2, sticky="ew")


# 右侧：生成器界面
generator_frame = ttk.LabelFrame(main_paned, text="生成器")
main_paned.add(generator_frame, weight=2)

# 类别选择
checkboxes = {}
categories_frame = ttk.Frame(generator_frame)
categories_frame.pack(anchor="w", padx=5, pady=5)
ttk.Label(generator_frame, text="选择关键词类别：").pack(anchor="w")
refresh_main_categories()

# 设置生成数量
ttk.Label(generator_frame, text="生成关键词数量：").pack(anchor="w", padx=5, pady=2)
num_keywords_entry = ttk.Entry(generator_frame)
num_keywords_entry.insert(0, "3")
num_keywords_entry.pack(anchor="w", padx=5, pady=2)

# 生成按钮与结果
generate_button = ttk.Button(generator_frame, text="生成关键词", command=generate_keywords)
generate_button.pack(pady=10)
result_label = ttk.Label(generator_frame, text="", foreground="blue", wraplength=300, justify="left")
result_label.pack(padx=5, pady=5)

refresh_categories()
root.mainloop()

# 输出格式选项
output_format_label = ttk.Label(generator_frame, text="选择输出格式：")
output_format_label.pack(anchor="w", padx=5, pady=2)
output_format = tk.StringVar(value="单行")
output_format_choices = ["单行", "逗号分隔", "多行"]
output_format_menu = ttk.OptionMenu(generator_frame, output_format, *output_format_choices)
output_format_menu.pack(anchor="w", padx=5, pady=2)

# 控制输出类别比例
balance_var = tk.BooleanVar(value=True)
ttk.Checkbutton(generator_frame, text="平衡各类别关键词比例", variable=balance_var).pack(anchor="w", padx=5, pady=2)

# 更新生成逻辑
def generate_keywords():
    selected_categories = [cat for cat, var in checkboxes.items() if var.get()]
    if not selected_categories:
        result_label.config(text="请选择至少一个关键词类别！")
        return
    try:
        num_keywords = int(num_keywords_entry.get())
    except ValueError:
        result_label.config(text="请输入有效的数字！")
        return

    generated = []
    if balance_var.get():
        # 平衡各类别输出
        count_per_category = max(1, num_keywords // len(selected_categories))
        for category in selected_categories:
            words = keywords[category]
            choices = [word for word, weight in words for _ in range(weight)]
            generated.extend(random.choices(choices, k=count_per_category))
        # 补充不足部分
        remaining = num_keywords - len(generated)
        if remaining > 0:
            additional_category = random.choice(selected_categories)
            words = keywords[additional_category]
            choices = [word for word, weight in words for _ in range(weight)]
            generated.extend(random.choices(choices, k=remaining))
    else:
        # 随机选择
        for _ in range(num_keywords):
            category = random.choice(selected_categories)
            words = keywords[category]
            choices = [word for word, weight in words for _ in range(weight)]
            generated.append(random.choice(choices))

    # 输出格式
    if output_format.get() == "单行":
        result_text = " ".join(generated)
    elif output_format.get() == "逗号分隔":
        result_text = ", ".join(generated)
    else:  # 多行
        result_text = "\n".join(generated)

    result_label.config(text=result_text)

# 统一设置生成界面控件的内边距
for widget in generator_frame.winfo_children():
    widget.pack_configure(padx=5, pady=5)

# 生成数量设置框
quantity_frame = ttk.Frame(settings_frame)
quantity_frame.pack(fill="x", padx=5, pady=5)

# 选择分类标签
selected_category_label = ttk.Label(quantity_frame, text="当前分类：无")
selected_category_label.pack(anchor="w", padx=5, pady=2)

# 固定数量输入框
ttk.Label(quantity_frame, text="固定生成数量：").pack(anchor="w", padx=5, pady=2)
fixed_quantity_entry = ttk.Entry(quantity_frame)
fixed_quantity_entry.insert(0, "3")
fixed_quantity_entry.pack(anchor="w", padx=5, pady=2)

# 随机生成选项
random_var = tk.BooleanVar(value=False)
ttk.Checkbutton(quantity_frame, text="随机数量（忽略固定值）", variable=random_var).pack(anchor="w", padx=5, pady=2)

# 更新分类的数量设置
def update_category_settings():
    selected_item = category_tree.selection()
    if not selected_item:
        messagebox.showwarning("未选择分类", "请先选择一个分类！")
        return
    selected_category = selected_item[0]
    if selected_category in keywords:
        try:
            fixed_count = int(fixed_quantity_entry.get())
            category_count[selected_category]["fixed"] = fixed_count
            category_count[selected_category]["random"] = random_var.get()
            messagebox.showinfo("更新成功", f"分类 '{selected_category}' 的设置已更新！")
        except ValueError:
            messagebox.showerror("无效输入", "固定生成数量必须为整数！")

ttk.Button(quantity_frame, text="保存设置", command=update_category_settings).pack(anchor="w", padx=5, pady=5)
def refresh_categories():
    category_tree.delete(*category_tree.get_children())
    for category, words in keywords.items():
        category_tree.insert("", "end", iid=category, text=category, values=(len(words),))
        for word, weight in words:
            category_tree.insert(category, "end", text=word, values=(weight,))
    # 更新选中的分类设置
    def on_category_select(event):
        selected_item = category_tree.selection()
        if not selected_item:
            return
        selected_category = selected_item[0]
        if selected_category in keywords:
            selected_category_label.config(text=f"当前分类：{selected_category}")
            fixed_quantity_entry.delete(0, tk.END)
            fixed_quantity_entry.insert(0, category_count[selected_category]["fixed"])
            random_var.set(category_count[selected_category]["random"])
    category_tree.bind("<<TreeviewSelect>>", on_category_select)

def generate_keywords():
    selected_categories = [cat for cat, var in checkboxes.items() if var.get()]
    if not selected_categories:
        result_label.config(text="请选择至少一个关键词类别！")
        return
    try:
        num_keywords = int(num_keywords_entry.get())
    except ValueError:
        result_label.config(text="请输入有效的数字！")
        return

    generated = []
    for category in selected_categories:
        words = keywords[category]
        choices = [word for word, weight in words for _ in range(weight)]
        if category_count[category]["random"]:
            count = random.randint(1, num_keywords)
        else:
            count = category_count[category]["fixed"]
        generated.extend(random.choices(choices, k=min(count, len(choices))))

    # 根据输出格式调整结果
    if output_format.get() == "单行":
        result_text = " ".join(generated)
    elif output_format.get() == "逗号分隔":
        result_text = ", ".join(generated)
    else:
        result_text = "\n".join(generated)

    result_label.config(text=result_text)
