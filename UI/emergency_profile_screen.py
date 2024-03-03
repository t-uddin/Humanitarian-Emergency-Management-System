import tkinter as tk
from tkinter import ttk

class EmergencyProfileScreen:
    def __init__(self, root):
        self.root = root
        self.root.title('Refugee System | Emergency Profile')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=7, rowspan=7)

        # title
        label = tk.Label(text="New Refugee", justify="center")
        label.config(font=("Roboto", 32))
        label.grid(column=3, row=0)

        # input labels
        tk.Label(text="Lead Family Member",
                 justify="right").grid(row=1, column=2)
        tk.Label(text="No. of relatives",
                 justify="right").grid(row=2, column=2)
        tk.Label(text="Camp", justify="right").grid(row=3, column=2)
        tk.Label(text="Medical Condition",
                 justify="right").grid(row=4, column=2)

        # input boxes
        family_member = tk.Entry(width=35, justify="left")
        family_member.grid(row=1, column=3, columnspan=2)

        number_of_relatives = tk.Entry(width=35, justify="left")
        number_of_relatives.grid(row=2, column=3, columnspan=2)

        camp = ttk.Combobox(width=35, justify="left",
                            values=["One", "Two", "Three"])
        camp.grid(row=3, column=3, columnspan=2)

        medical_condition = ttk.Combobox(width=35, justify="left", values=[
            "One", "Two", "Three"])
        medical_condition.grid(row=4, column=3, columnspan=2)

        # buttons
        return_button = tk.Button(text="Return", padx=20,
                                  pady=10, command=self.return_back)
        return_button.grid(column=2, row=5)

        create_button = tk.Button(text="Create", padx=20, pady=10,
                                  command=lambda: self.create(family_member.get(), number_of_relatives.get(), camp.get(), medical_condition.get()))
        create_button.grid(column=4, row=5)

    def create(self, family_member, number_of_relatives, camp, medical_condition):
        # call the login backend function
        # destroy the window
        self.clear_window()
        # redirect to dashboard

    def return_back(self):
        self.clear_window()
        # redirect to dashboard
