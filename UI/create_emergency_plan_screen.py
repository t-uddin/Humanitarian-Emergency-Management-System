import tkinter as tk
from tkinter import ttk

class CreateEmergencyPlanScreen:
    def __init__(self, root):
        self.root = root
        self.root.title('Refugee System | Create Emergency Plan')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=11, rowspan=11)

        # title
        label = tk.Label(text="New Emergency Plan", justify="center")
        label.config(font=("Roboto", 32))
        label.grid(column=5, row=0)

        # input labels
        tk.Label(text="Emergency Type",
                 justify="right").grid(row=1, column=4)
        tk.Label(text="Description",
                 justify="right").grid(row=2, column=4)
        tk.Label(text="Location", justify="right").grid(row=3, column=4)
        tk.Label(text="Start Date",
                 justify="right").grid(row=4, column=4)
        tk.Label(text="End Date",
                 justify="right").grid(row=5, column=4)
        tk.Label(text="Refugees",
                 justify="right").grid(row=6, column=4)
        tk.Label(text="Volunteers",
                 justify="right").grid(row=7, column=4)

        # input boxes
        emergency_type = tk.Entry(width=35, justify="left")
        emergency_type.grid(row=1, column=5, columnspan=2)

        description = tk.Entry(width=35, justify="left")
        description.grid(row=2, column=5, columnspan=2)

        location = ttk.Combobox(width=35, justify="left",
                                values=["One", "Two", "Three"])
        location.grid(row=3, column=5, columnspan=2)

        start_date = ttk.Combobox(width=35, justify="left", values=[
            "One", "Two", "Three"])
        start_date.grid(row=4, column=5, columnspan=2)

        end_date = ttk.Combobox(width=35, justify="left", values=[
            "One", "Two", "Three"])
        end_date.grid(row=5, column=5, columnspan=2)

        refugees = ttk.Combobox(width=35, justify="left", values=[
            "One", "Two", "Three"])
        refugees.grid(row=6, column=5, columnspan=2)

        volunteers = ttk.Combobox(width=35, justify="left", values=[
            "One", "Two", "Three"])
        volunteers.grid(row=7, column=5, columnspan=2)

        # buttons
        return_button = tk.Button(text="Return", padx=20,
                                  pady=10, command=self.return_back)
        return_button.grid(column=4, row=9)

        create_button = tk.Button(text="Create", padx=20, pady=10,
                                  command=lambda: self.create(
                                      emergency_type.get(), description.get(), location.get(),
                                      start_date.get(), end_date.get(), refugees.get(), volunteers.get()))
        create_button.grid(column=6, row=9)

    def create(self, emergency_type, description, location, start_date, end_date, refugees, volunteers):
        # call the login backend function
        # destroy the window
        self.clear_window()
        print(emergency_type + ' ' + description +
              ' ' + ' ' + location + ' ' + start_date + ' ' + end_date + ' ' + refugees + ' ' + volunteers)
        # redirect to emergency plan

    def return_back(self):
        self.clear_window()
        # redirect to emergency plan
