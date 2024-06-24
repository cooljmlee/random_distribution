import tkinter as tk
from tkinter import messagebox
import random

class MemberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Member Management")
        self.members = []
        
        self.gender_var = tk.StringVar(value="Male")
        
        self.create_widgets()
        
    def create_widgets(self):
        gender_frame = tk.Frame(self.root)
        gender_frame.pack(pady=10)
        
        tk.Label(gender_frame, text="Gender:").pack(side=tk.LEFT)
        self.male_radio = tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male")
        self.male_radio.pack(side=tk.LEFT)
        self.female_radio = tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female")
        self.female_radio.pack(side=tk.LEFT)
        
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Enter Member Name:").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.pack(side=tk.LEFT)
        self.name_entry.bind("<Return>", self.add_member)
        
        self.member_listbox = tk.Listbox(self.root, width=50)
        self.member_listbox.pack(pady=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.edit_button = tk.Button(button_frame, text="Edit", command=self.edit_member)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_member)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.team_button = tk.Button(self.root, text="Divide Teams", command=self.divide_teams)
        self.team_button.pack(pady=10)
        
    def add_member(self, event=None):
        name = self.name_entry.get().strip()
        gender = self.gender_var.get()
        
        if name:
            self.members.append((name, gender))
            self.update_member_listbox()
            self.name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Member name cannot be empty")
            
    def update_member_listbox(self):
        self.member_listbox.delete(0, tk.END)
        for member in self.members:
            self.member_listbox.insert(tk.END, f"{member[1]}: {member[0]}")
            
    def edit_member(self):
        selected_index = self.member_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            old_member = self.members[selected_index]
            new_name = self.name_entry.get().strip()
            if new_name:
                self.members[selected_index] = (new_name, old_member[1])
                self.update_member_listbox()
                self.name_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Input Error", "Member name cannot be empty")
        else:
            messagebox.showwarning("Selection Error", "No member selected")
            
    def delete_member(self):
        selected_index = self.member_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            del self.members[selected_index]
            self.update_member_listbox()
        else:
            messagebox.showwarning("Selection Error", "No member selected")
    
    def divide_teams(self):
        if len(self.members) < 2:
            messagebox.showwarning("Team Division Error", "Not enough members to divide into teams")
            return
        
        random.shuffle(self.members)
        mid_point = len(self.members) // 2
        team1 = self.members[:mid_point]
        team2 = self.members[mid_point:]
        
        team1_names = [member[0] for member in team1]
        team2_names = [member[0] for member in team2]
        
        messagebox.showinfo("Teams Divided", f"Team 1: {', '.join(team1_names)}\nTeam 2: {', '.join(team2_names)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemberApp(root)
    root.mainloop()
