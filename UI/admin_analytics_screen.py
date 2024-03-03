import tkinter as tk
import UI.camp_personnel_screen as personnel_screen
import UI.camp_resources_screen as resources_screen
from Back_End.Charts.charts import ChartsController
import UI.dashboard_screen as dashboard

class AdminAnalyticsScreen():
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.connection = connection
        self.user_name = user_name
        self.is_admin = is_admin
        self.root.title('Refugee System | Camp Insights')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def return_back(self):
        self.clear_window()
        dashboard.DashboardScreen(self.root, self.connection, self.user_name, self.is_admin).render()

    def openCampsResources(self):
        self.clear_window()
        resources_screen.ResourcesScreen(self.root, self.connection, self.user_name, self.is_admin).render()

    def openCampsPersonnel(self):
        self.clear_window()
        personnel_screen.PersonnelScreen(self.root, self.connection, self.user_name, self.is_admin).render()

    def open_camps_status_chart(self):
        charts = ChartsController(self.connection)
        return charts.camps_status()

    def open_camps_medical_status_chart(self):
        charts = ChartsController(self.connection)
        return charts.updated_camp_medical_needs()

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=5, rowspan=10)

        # get volunteer data
        heading = tk.Label(text="All Camp Insights", justify="center")
        heading.config(font=("Roboto", 32))
        heading.grid(column=2, row=1)

        # buttons
        camps_resource_button = tk.Button(text="Camp Resource Status", padx=20, pady=10,
                                          command=self.openCampsResources)
        camps_resource_button.grid(column=2, row=3)

        camps_personnel_button = tk.Button(text="Camps Personnel Status", padx=20, pady=10,
                                           command=self.openCampsPersonnel)
        camps_personnel_button.grid(column=2, row=5)

        camps_status_chart_button = tk.Button(text="Camps Status chart", padx=20, pady=10,
                                                command=self.open_camps_status_chart)
        camps_status_chart_button.grid(column=2, row=4)

        camps_medical_status_chart_button = tk.Button(text="Camps Medical Status Chart", padx=20, pady=10,
                                                command=self.open_camps_medical_status_chart)
        camps_medical_status_chart_button.grid(column=2, row=6)


        # return button
        return_button = tk.Button(text="Return", command=self.return_back)
        return_button.grid(column=2, row=8, padx=20, pady=10)
