import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.filename = "weather_data.json"
        self.data = self.load_data()

        # UI Elements
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.ent_date = tk.Entry(frame)
        self.ent_date.grid(row=0, column=1)

        tk.Label(frame, text="Температура (°C):").grid(row=1, column=0)
        self.ent_temp = tk.Entry(frame)
        self.ent_temp.grid(row=1, column=1)

        tk.Label(frame, text="Описание:").grid(row=2, column=0)
        self.ent_desc = tk.Entry(frame)
        self.ent_desc.grid(row=2, column=1)

        self.var_precip = tk.BooleanVar()
        tk.Checkbutton(frame, text="Осадки", variable=self.var_precip).grid(row=3, column=1)

        tk.Button(frame, text="Добавить запись", command=self.add_entry).grid(row=4, columnspan=2, pady=5)

        # Filter Frame
        f_frame = tk.Frame(root, padx=10)
        f_frame.pack()
        tk.Label(f_frame, text="Мин. темп:").grid(row=0, column=0)
        self.ent_filter_temp = tk.Entry(f_frame, width=5)
        self.ent_filter_temp.grid(row=0, column=1)
        tk.Button(f_frame, text="Фильтр", command=self.filter_data).grid(row=0, column=2)
        tk.Button(f_frame, text="Сброс", command=self.show_all).grid(row=0, column=3)

        # Treeview
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Темп.")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.pack(padx=10, pady=10)

        self.show_all()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_entry(self):
        try:
            date_str = self.ent_date.get()
            datetime.strptime(date_str, "%d.%m.%Y")
            temp = float(self.ent_temp.get())
            desc = self.ent_desc.get()
            if not desc: raise ValueError("Описание пустое")
            
            entry = {
                "date": date_str,
                "temp": temp,
                "desc": desc,
                "precip": self.var_precip.get()
            }
            self.data.append(entry)
            self.save_data()
            self.show_all()
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверный ввод: {e}")

    def show_all(self):
        self.update_tree(self.data)

    def filter_data(self):
        try:
            min_t = float(self.ent_filter_temp.get())
            filtered = [d for d in self.data if d['temp'] > min_t]
            self.update_tree(filtered)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число для фильтра")

    def update_tree(self, items):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in items:
            self.tree.insert("", "end", values=(item['date'], item['temp'], item['desc'], "Да" if item['precip'] else "Нет"))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
