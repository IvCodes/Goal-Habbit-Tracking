import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import os
import json

# File to save the progress data
DATA_FILE = 'goal_tracker_data.json'
COMPLETED_FILE = 'completed_goals.json'

class GoalTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Goal Tracker")
        self.root.geometry("800x600")
        
        self.container = tk.Frame(self.root)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.goal_frame = tk.Frame(self.canvas)
        
        self.goal_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.goal_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.container.pack(fill="both", expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        tk.Button(self.root, text="Set New Goal", command=self.create_or_edit_goal).pack(pady=10)
        
        self.display_goals()
        
    def load_data(self, file):
        if os.path.exists(file):
            with open(file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self, file, data):
        with open(file, 'w') as f:
            json.dump(data, f)

    def load_progress(self):
        return self.load_data(DATA_FILE)
    
    def save_progress(self, progress):
        self.save_data(DATA_FILE, progress)
    
    def load_completed_goals(self):
        return self.load_data(COMPLETED_FILE)
    
    def save_completed_goals(self, completed_goals):
        self.save_data(COMPLETED_FILE, completed_goals)

    def create_or_edit_goal(self, goal_desc=None):
        goal_window = tk.Toplevel(self.root)
        goal_window.title("Set New Goal" if goal_desc is None else "Edit Goal")
        goal_window.geometry("400x200")
        
        tk.Label(goal_window, text="Goal Description:").pack(pady=(10, 0))
        goal_desc_entry = tk.Entry(goal_window, width=40)
        goal_desc_entry.pack(pady=(0, 10))
        
        tk.Label(goal_window, text="Number of Days:").pack(pady=(10, 0))
        days_spinbox = tk.Spinbox(goal_window, from_=1, to=365, width=5)
        days_spinbox.pack(pady=(0, 10))
        
        if goal_desc:
            progress = self.load_progress()
            goal_data = progress[goal_desc]
            goal_desc_entry.insert(0, goal_desc)
            days_spinbox.delete(0, 'end')
            days_spinbox.insert(0, goal_data['days'])
        
        def save_goal():
            new_goal_desc = goal_desc_entry.get()
            try:
                num_days = int(days_spinbox.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number of days.")
                return
            
            start_date = datetime.date.today().isoformat()
            end_date = (datetime.date.today() + datetime.timedelta(days=num_days)).isoformat()
            
            progress = self.load_progress()
            if goal_desc:
                del progress[goal_desc]
            
            progress[new_goal_desc] = {
                'start_date': start_date,
                'end_date': end_date,
                'days': num_days,
                'completed': [False] * num_days
            }
            self.save_progress(progress)
            goal_window.destroy()
            self.display_goals()
        
        tk.Button(goal_window, text="Save Goal", command=save_goal).pack(pady=10)

    def delete_goal(self, goal_desc):
        progress = self.load_progress()
        if goal_desc in progress:
            del progress[goal_desc]
            self.save_progress(progress)
            self.display_goals()

    def mark_goal_completed(self, goal_desc, data):
        completed_goals = self.load_completed_goals()
        completed_goals[goal_desc] = data
        self.save_completed_goals(completed_goals)

    def update_progress(self, goal, day, var):
        progress = self.load_progress()
        data = progress[goal]
        data['completed'][day] = var.get()
        self.save_progress(progress)
        self.display_goals()
        if var.get() and all(data['completed']):
            self.mark_goal_completed(goal, data)
            messagebox.showinfo("Goal Completed", f"Good job! You've completed the goal: {goal}")

    def display_goals(self):
        for widget in self.goal_frame.winfo_children():
            widget.destroy()

        progress = self.load_progress()
        row = 0
        for goal_desc, data in progress.items():
            goal_container = tk.Frame(self.goal_frame, bd=2, relief=tk.RIDGE)
            goal_container.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
            
            header_frame = tk.Frame(goal_container)
            header_frame.pack(fill="x")
            
            tk.Label(header_frame, text=f"Goal: {goal_desc}", font=("Arial", 14)).pack(side="left", padx=(10, 0))
            tk.Label(header_frame, text=f"Days Completed: {sum(data['completed'])}/{data['days']}", font=("Arial", 12)).pack(side="right", padx=(0, 10))
            tk.Button(header_frame, text="Edit", command=lambda goal=goal_desc: self.create_or_edit_goal(goal)).pack(side="right", padx=(0, 10))
            tk.Button(header_frame, text="Delete", command=lambda goal=goal_desc: self.delete_goal(goal)).pack(side="right", padx=(0, 10))
            
            sub_frame = tk.Frame(goal_container)
            sub_frame.pack(fill="both", expand=True)
            
            canvas = tk.Canvas(sub_frame)
            scroll_y = tk.Scrollbar(sub_frame, orient="vertical", command=canvas.yview)
            inner_frame = tk.Frame(canvas)

            inner_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=inner_frame, anchor="nw")
            canvas.configure(yscrollcommand=scroll_y.set)
            
            for i in range(data['days']):
                date_label = tk.Label(inner_frame, text=(datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
                date_label.grid(row=i, column=0, padx=10, pady=2)
                
                var = tk.BooleanVar(value=data['completed'][i])
                cb = tk.Checkbutton(inner_frame, variable=var)
                cb.grid(row=i, column=1, padx=10, pady=2)
                cb.var = var
                
                cb.config(command=lambda goal=goal_desc, day=i, var=var: self.update_progress(goal, day, var))
            
            canvas.pack(side="left", fill="both", expand=True)
            scroll_y.pack(side="right", fill="y")
            
            # Enable mouse wheel scrolling
            def on_mouse_wheel(event, canvas=canvas):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            inner_frame.bind("<Enter>", lambda e: inner_frame.bind_all("<MouseWheel>", on_mouse_wheel))
            inner_frame.bind("<Leave>", lambda e: inner_frame.unbind_all("<MouseWheel>"))
            
            row += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = GoalTrackerApp(root)
    root.mainloop()
