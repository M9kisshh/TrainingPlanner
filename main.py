import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "training_data.json"

# ---------- Работа с JSON ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- Главное окно ----------
root = tk.Tk()
root.title("Training Planner")
root.geometry("700x500")

# Фрейм ввода
frame_input = tk.LabelFrame(root, text="Добавить тренировку", padx=10, pady=10)
frame_input.pack(fill="x", padx=10, pady=5)

tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w")
entry_date = tk.Entry(frame_input, width=15)
entry_date.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Тип тренировки:").grid(row=0, column=2, sticky="w")
combo_type = ttk.Combobox(frame_input, values=["Бег", "Плавание", "Велосипед", "Силовая", "Йога", "Растяжка"], width=12)
combo_type.grid(row=0, column=3, padx=5)
combo_type.current(0)

tk.Label(frame_input, text="Длительность (мин):").grid(row=0, column=4, sticky="w")
entry_duration = tk.Entry(frame_input, width=8)
entry_duration.grid(row=0, column=5, padx=5)

# Таблица
frame_table = tk.LabelFrame(root, text="Список тренировок", padx=10, pady=10)
frame_table.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("Дата", "Тип", "Длительность")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
tree.heading("Дата", text="Дата")
tree.heading("Тип", text="Тип тренировки")
tree.heading("Длительность", text="Длительность (мин)")
tree.column("Дата", width=120)
tree.column("Тип", width=150)
tree.column("Длительность", width=120)
tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# ---------- Функции ----------
def refresh_table(data):
    """Очистить и заполнить таблицу данными."""
    for row in tree.get_children():
        tree.delete(row)
    for record in data:
        tree.insert("", "end", values=(record["date"], record["type"], record["duration"]))

def add_training():
    date = entry_date.get().strip()
    ttype = combo_type.get().strip()
    duration_str = entry_duration.get().strip()

    # Валидация
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД (например, 2026-05-15)")
        return

    if not ttype:
        messagebox.showerror("Ошибка", "Выберите тип тренировки")
        return

    try:
        duration = int(duration_str)
        if duration <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным целым числом")
        return

    data = load_data()
    data.append({"date": date, "type": ttype, "duration": duration})
    save_data(data)
    refresh_table(data)

    # Очистка полей
    entry_date.delete(0, tk.END)
    entry_duration.delete(0, tk.END)

# Фильтрация
def apply_filter():
    filter_type = combo_filter_type.get()
    filter_date = entry_filter_date.get().strip()

    data = load_data()
    filtered = data

    if filter_type != "Все":
        filtered = [r for r in filtered if r["type"] == filter_type]

    if filter_date:
        try:
            datetime.strptime(filter_date, "%Y-%m-%d")
            filtered = [r for r in filtered if r["date"] == filter_date]
        except ValueError:
            messagebox.showerror("Ошибка", "Формат даты фильтра: ГГГГ-ММ-ДД")
            return

    refresh_table(filtered)

def reset_filter():
    combo_filter_type.set("Все")
    entry_filter_date.delete(0, tk.END)
    refresh_table(load_data())

# Кнопка "Добавить"
btn_add = tk.Button(frame_input, text="Добавить тренировку", command=add_training)
btn_add.grid(row=1, column=0, columnspan=6, pady=5)

# Фрейм фильтрации
frame_filter = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
frame_filter.pack(fill="x", padx=10, pady=5)

tk.Label(frame_filter, text="Тип:").grid(row=0, column=0, sticky="w")
combo_filter_type = ttk.Combobox(frame_filter, values=["Все", "Бег", "Плавание", "Велосипед", "Силовая", "Йога", "Растяжка"], width=12)
combo_filter_type.grid(row=0, column=1, padx=5)
combo_filter_type.current(0)

tk.Label(frame_filter, text="Дата:").grid(row=0, column=2, sticky="w")
entry_filter_date = tk.Entry(frame_filter, width=15)
entry_filter_date.grid(row=0, column=3, padx=5)

btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=5)

btn_reset = tk.Button(frame_filter, text="Сбросить", command=reset_filter)
btn_reset.grid(row=0, column=5, padx=5)

# Загрузка данных при старте
initial_data = load_data()
refresh_table(initial_data)

root.mainloop()