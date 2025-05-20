import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import json
import os
from difflib import SequenceMatcher
import sqlite3
from datetime import datetime

class HomeworkChecker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("作业检查系统")
        self.window.geometry("800x600")
        
        # 存储数据
        self.standard_answer = None
        self.student_answers = {}
        self.results = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标准答案部分
        ttk.Label(main_frame, text="标准答案文件:").grid(row=0, column=0, sticky=tk.W)
        self.standard_answer_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.standard_answer_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="浏览", command=self.load_standard_answer).grid(row=0, column=2)
        
        # 学生作业部分
        ttk.Label(main_frame, text="学生作业文件夹:").grid(row=1, column=0, sticky=tk.W)
        self.student_folder_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.student_folder_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="浏览", command=self.load_student_answers).grid(row=1, column=2)
        
        # 导出选项
        export_frame = ttk.LabelFrame(main_frame, text="导出选项", padding="5")
        export_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Button(export_frame, text="导出为TXT", command=lambda: self.export_results('txt')).grid(row=0, column=0, padx=5)
        ttk.Button(export_frame, text="导出为CSV", command=lambda: self.export_results('csv')).grid(row=0, column=1, padx=5)
        ttk.Button(export_frame, text="导出为JSON", command=lambda: self.export_results('json')).grid(row=0, column=2, padx=5)
        ttk.Button(export_frame, text="导出到数据库", command=self.export_to_db).grid(row=0, column=3, padx=5)
        
        # 结果显示区域
        self.result_text = tk.Text(main_frame, height=20, width=80)
        self.result_text.grid(row=3, column=0, columnspan=3, pady=10)
        
        # 开始检查按钮
        ttk.Button(main_frame, text="开始检查", command=self.check_homework).grid(row=4, column=0, columnspan=3, pady=10)
        
    def load_standard_answer(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.standard_answer_path.set(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                self.standard_answer = f.read()
                
    def load_student_answers(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.student_folder_path.set(folder_path)
            self.student_answers = {}
            for file in os.listdir(folder_path):
                if file.endswith('.txt'):
                    with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                        self.student_answers[file] = f.read()
                        
    def calculate_similarity(self, str1, str2):
        return SequenceMatcher(None, str1, str2).ratio()
    
    def check_homework(self):
        if not self.standard_answer or not self.student_answers:
            messagebox.showerror("错误", "请先加载标准答案和学生作业！")
            return
            
        results = []
        for student_file, answer in self.student_answers.items():
            similarity = self.calculate_similarity(self.standard_answer, answer)
            student_name = os.path.splitext(student_file)[0]
            results.append({
                '学生': student_name,
                '相似度': round(similarity * 100, 2),
                '得分': round(similarity * 100, 2)
            })
            
        self.results = pd.DataFrame(results)
        self.display_results()
        
    def display_results(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, self.results.to_string())
        
    def export_results(self, format_type):
        if self.results is None:
            messagebox.showerror("错误", "请先进行作业检查！")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=[(f"{format_type.upper()} files", f"*.{format_type}")]
        )
        
        if file_path:
            if format_type == 'txt':
                self.results.to_string(file_path)
            elif format_type == 'csv':
                self.results.to_csv(file_path, index=False, encoding='utf-8-sig')
            elif format_type == 'json':
                self.results.to_json(file_path, force_ascii=False, orient='records')
                
            messagebox.showinfo("成功", f"结果已导出到 {file_path}")
            
    def export_to_db(self):
        if self.results is None:
            messagebox.showerror("错误", "请先进行作业检查！")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db")]
        )
        
        if file_path:
            conn = sqlite3.connect(file_path)
            self.results.to_sql('homework_results', conn, if_exists='replace', index=False)
            conn.close()
            messagebox.showinfo("成功", f"结果已导出到数据库 {file_path}")
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = HomeworkChecker()
    app.run()
