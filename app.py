# Smart Assignment Priority System - Tkinter (window) version
# Python concepts : Classes, Functions, Lists, Loops, Recursion, Tkinter widgets
# Logic           : Priority score + Merge Sort + fit-in-free-hours plan

import tkinter as tk
from tkinter import messagebox


# ---------- CLASS ----------
class Assignment:
    def __init__(self, name, days_remaining, marks, hours_required):
        self.name = name
        self.days_remaining = days_remaining
        self.marks = marks
        self.hours_required = hours_required
        self.score = self.calculate_score()

    def calculate_score(self):
        # If due today (0 days), treat it as 1 day to avoid dividing by zero
        days = max(self.days_remaining, 1)
        marks_per_hour = self.marks / self.hours_required   # benefit per hour
        urgency = 1 / days                                  # fewer days = more urgent
        return marks_per_hour * urgency

    def get_level(self):
        if self.score >= 4:
            return "High Priority"
        elif self.score >= 1:
            return "Medium Priority"
        else:
            return "Low Priority"


# ---------- MERGE SORT (highest score first) ----------
def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i].score >= right[j].score:   # larger score goes first
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def merge_sort(items):
    if len(items) <= 1:                       # base case of recursion
        return items
    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])
    return merge(left, right)


# ---------- TODAY'S PLAN ----------
def make_todays_plan(sorted_assignments, hours_available):
    # Go through the sorted list and take every assignment that still fits.
    plan = []
    hours_left = hours_available

    for assignment in sorted_assignments:
        if assignment.hours_required <= hours_left:
            plan.append(assignment)
            hours_left = hours_left - assignment.hours_required

    return plan, hours_left


# ---------- LIST OF ALL ASSIGNMENTS ----------
assignments = []


# ---------- BUTTON FUNCTIONS ----------
def add_assignment():
    # Read the text typed in the boxes
    name = name_entry.get().strip()
    days = days_entry.get().strip()
    marks = marks_entry.get().strip()
    hours = hours_entry.get().strip()

    # Check the input
    if name == "":
        messagebox.showerror("Invalid input", "Please enter the assignment name.")
        return
    if not (days.isdigit() and marks.isdigit() and hours.isdigit()):
        messagebox.showerror("Invalid input",
                             "Days, marks and hours must be whole numbers.")
        return
    if int(marks) < 1 or int(hours) < 1:
        messagebox.showerror("Invalid input", "Marks and hours must be at least 1.")
        return

    # Create the object and store it in the list
    new_assignment = Assignment(name, int(days), int(marks), int(hours))
    assignments.append(new_assignment)

    # Show it in the "added assignments" list box
    added_list.insert(tk.END, name + "  |  " + days + " days  |  "
                      + marks + " marks  |  " + hours + " hours")

    # Clear the boxes for the next assignment
    name_entry.delete(0, tk.END)
    days_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)
    name_entry.focus()


def show_result():
    if len(assignments) == 0:
        messagebox.showwarning("No assignments", "Please add at least one assignment.")
        return

    free_hours = free_entry.get().strip()
    if not free_hours.isdigit() or int(free_hours) < 1:
        messagebox.showerror("Invalid input",
                             "Free hours must be a whole number (1 or more).")
        return
    free_hours = int(free_hours)

    # Sort with Merge Sort, then make today's plan
    sorted_assignments = merge_sort(assignments)
    plan, hours_left = make_todays_plan(sorted_assignments, free_hours)

    # Write the result in the big text box
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)

    result_box.insert(tk.END, "========== PRIORITY ORDER ==========\n")
    result_box.insert(tk.END, f"{'Rank':<6}{'Assignment':<16}{'Days':<6}"
                              f"{'Marks':<7}{'Hours':<7}{'Score':<8}Priority\n")
    result_box.insert(tk.END, "-" * 65 + "\n")

    rank = 1
    for a in sorted_assignments:
        level = a.get_level()
        if level == "High Priority":
            colour_tag = "high"
        elif level == "Medium Priority":
            colour_tag = "medium"
        else:
            colour_tag = "low"
        line = (f"{rank:<6}{a.name:<16}{a.days_remaining:<6}{a.marks:<7}"
                f"{a.hours_required:<7}{a.score:<8.2f}{level}\n")
        result_box.insert(tk.END, line, colour_tag)
        rank += 1

    result_box.insert(tk.END, "\n========== TODAY'S PLAN (" + str(free_hours)
                              + " hours available) ==========\n")
    if len(plan) == 0:
        result_box.insert(tk.END, "No assignment fits in the available time.\n")
    else:
        for a in plan:
            result_box.insert(tk.END, "- " + a.name + " (" + str(a.hours_required)
                                      + " hours)\n")
    result_box.insert(tk.END, "Hours left over: " + str(hours_left) + "\n")

    result_box.config(state="disabled")   # user cannot type inside the result box


def clear_all():
    assignments.clear()
    added_list.delete(0, tk.END)
    free_entry.delete(0, tk.END)
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.config(state="disabled")


# ---------- WINDOW AND WIDGETS ----------
window = tk.Tk()
window.title("Smart Assignment Priority System")
window.geometry("640x720")

title_label = tk.Label(window, text="Smart Assignment Priority System",
                       font=("Arial", 16, "bold"))
title_label.pack(pady=8)

# --- Part 1: enter an assignment ---
input_frame = tk.LabelFrame(window, text="1. Add an assignment", padx=10, pady=8)
input_frame.pack(padx=10, pady=5, fill="x")

tk.Label(input_frame, text="Assignment name:").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(input_frame, width=25)
name_entry.grid(row=0, column=1, padx=5, pady=3)

tk.Label(input_frame, text="Days remaining (0 if due today):").grid(row=1, column=0, sticky="w")
days_entry = tk.Entry(input_frame, width=25)
days_entry.grid(row=1, column=1, padx=5, pady=3)

tk.Label(input_frame, text="Marks / importance:").grid(row=2, column=0, sticky="w")
marks_entry = tk.Entry(input_frame, width=25)
marks_entry.grid(row=2, column=1, padx=5, pady=3)

tk.Label(input_frame, text="Estimated hours required:").grid(row=3, column=0, sticky="w")
hours_entry = tk.Entry(input_frame, width=25)
hours_entry.grid(row=3, column=1, padx=5, pady=3)

add_button = tk.Button(input_frame, text="Add Assignment", command=add_assignment)
add_button.grid(row=4, column=0, columnspan=2, pady=6)

# --- Part 2: list of added assignments ---
list_frame = tk.LabelFrame(window, text="Assignments added so far", padx=10, pady=5)
list_frame.pack(padx=10, pady=5, fill="x")

added_list = tk.Listbox(list_frame, height=5, width=75)
added_list.pack()

# --- Part 3: free hours and buttons ---
action_frame = tk.LabelFrame(window, text="2. Get the result", padx=10, pady=8)
action_frame.pack(padx=10, pady=5, fill="x")

tk.Label(action_frame, text="Free hours available today:").grid(row=0, column=0, sticky="w")
free_entry = tk.Entry(action_frame, width=10)
free_entry.grid(row=0, column=1, padx=5)

result_button = tk.Button(action_frame, text="Show Priority Order and Plan",
                          command=show_result)
result_button.grid(row=0, column=2, padx=10)

clear_button = tk.Button(action_frame, text="Clear All", command=clear_all)
clear_button.grid(row=0, column=3)

# --- Part 4: result box ---
result_box = tk.Text(window, width=78, height=16, font=("Courier New", 9),
                     state="disabled")
result_box.pack(padx=10, pady=8)

# Colours for the priority levels
result_box.tag_config("high", foreground="red")
result_box.tag_config("medium", foreground="orange")
result_box.tag_config("low", foreground="green")

window.mainloop()
