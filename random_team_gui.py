import tkinter as tk
from tkinter import messagebox, filedialog
import random
import itertools
import json
import os

class MemberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("회원 관리 프로그램")
        self.members = []
        
        self.gender_var = tk.StringVar(value="남성")
        self.team_count_var = tk.IntVar(value=2)
        
        self.create_widgets()
        
    def create_widgets(self):
        gender_frame = tk.Frame(self.root)
        gender_frame.pack(pady=10)
        
        tk.Label(gender_frame, text="성별:").pack(side=tk.LEFT)
        self.male_radio = tk.Radiobutton(gender_frame, text="남성", variable=self.gender_var, value="남성")
        self.male_radio.pack(side=tk.LEFT)
        self.female_radio = tk.Radiobutton(gender_frame, text="여성", variable=self.gender_var, value="여성")
        self.female_radio.pack(side=tk.LEFT)
        
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="회원 이름 입력:").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.pack(side=tk.LEFT)
        self.name_entry.bind("<Return>", self.add_member)
        
        self.member_frame = tk.Frame(self.root)
        self.member_frame.pack(pady=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.edit_button = tk.Button(button_frame, text="수정", command=self.edit_member)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(button_frame, text="삭제", command=self.delete_member)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_members)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        team_frame = tk.Frame(self.root)
        team_frame.pack(pady=10)
        
        tk.Label(team_frame, text="팀 수:").pack(side=tk.LEFT)
        self.team_spinbox = tk.Spinbox(team_frame, from_=2, to=10, textvariable=self.team_count_var)
        self.team_spinbox.pack(side=tk.LEFT)
        
        self.team_button = tk.Button(self.root, text="팀 나누기", command=self.divide_teams)
        self.team_button.pack(pady=10)
        
        self.save_button = tk.Button(self.root, text="회원 저장", command=self.save_members)
        self.save_button.pack(pady=5)
        
        self.load_button = tk.Button(self.root, text="회원 불러오기", command=self.load_members)
        self.load_button.pack(pady=5)
        
        self.update_member_listbox()
        
    def add_member(self, event=None):
        name = self.name_entry.get().strip()
        gender = self.gender_var.get()
        
        if name:
            self.members.append((name, gender))
            self.update_member_listbox()
            self.name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("입력 오류", "회원 이름은 비워둘 수 없습니다")
            
    def update_member_listbox(self):
        for widget in self.member_frame.winfo_children():
            widget.destroy()
        
        for idx, member in enumerate(self.members):
            label = tk.Label(self.member_frame, text=f"{member[1]}: {member[0]}", borderwidth=2, relief="groove", padx=5, pady=5)
            label.grid(row=idx, column=0, padx=5, pady=5)
            
    def edit_member(self):
        selected_index = self.get_selected_member_index()
        if selected_index is not None:
            old_member = self.members[selected_index]
            new_name = self.name_entry.get().strip()
            if new_name:
                self.members[selected_index] = (new_name, old_member[1])
                self.update_member_listbox()
                self.name_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("입력 오류", "회원 이름은 비워둘 수 없습니다")
        else:
            messagebox.showwarning("선택 오류", "선택된 회원이 없습니다")
            
    def delete_member(self):
        selected_index = self.get_selected_member_index()
        if selected_index is not None:
            del self.members[selected_index]
            self.update_member_listbox()
        else:
            messagebox.showwarning("선택 오류", "선택된 회원이 없습니다")
    
    def clear_members(self):
        self.members = []
        self.update_member_listbox()

    def get_selected_member_index(self):
        selected_index = self.member_frame.grid_slaves()
        if selected_index:
            return self.member_frame.grid_slaves()[0].grid_info()["row"]
        return None
    
    def divide_teams(self):
        num_teams = self.team_count_var.get()
        if len(self.members) < num_teams:
            messagebox.showwarning("팀 나누기 오류", "팀을 나누기에 회원 수가 부족합니다")
            return
        
        random.shuffle(self.members)
        teams = [[] for _ in range(num_teams)]
        
        # Ensure each team has at least one member of each gender
        males = [member for member in self.members if member[1] == "남성"]
        females = [member for member in self.members if member[1] == "여성"]
        
        for i in range(num_teams):
            if males:
                teams[i].append(males.pop())
            if females:
                teams[i].append(females.pop())
        
        remaining_members = males + females
        for i, member in enumerate(remaining_members):
            teams[i % num_teams].append(member)
        
        teams = self.balance_teams(teams)

        team_names = [f"팀 {i + 1}" for i in range(num_teams)]
        team_members = [", ".join([self.format_member(member) for member in team]) for team in teams]

        team_info = "\n".join([f"{team_name}: {members}" for team_name, members in zip(team_names, team_members)])
        
        result_window = tk.Toplevel(self.root)
        result_window.title("팀 나누기 결과")
        result_window.geometry("600x300")
        result_text = tk.Text(result_window, font=("Helvetica", 14))
        result_text.pack(expand=True, fill=tk.BOTH)
        result_text.insert(tk.END, team_info)
        result_text.config(state=tk.DISABLED)

    def format_member(self, member):
        return f"{member[0]} ({member[1]})"
    
    def balance_teams(self, teams):
        members = list(itertools.chain(*teams))
        num_teams = len(teams)
        ideal_size = len(members) // num_teams
        larger_teams = len(members) % num_teams
        
        balanced_teams = []
        current_index = 0
        
        for i in range(num_teams):
            team_size = ideal_size + (1 if i < larger_teams else 0)
            balanced_teams.append(members[current_index:current_index + team_size])
            current_index += team_size
        
        return balanced_teams
    
    def save_members(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.members, file)
            messagebox.showinfo("회원 저장", "회원 목록이 성공적으로 저장되었습니다")
    
    def load_members(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.members = json.load(file)
            self.update_member_listbox()
            messagebox.showinfo("회원 불러오기", "회원 목록이 성공적으로 불러와졌습니다")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemberApp(root)
    root.mainloop()
