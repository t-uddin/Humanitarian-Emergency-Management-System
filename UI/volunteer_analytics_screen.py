import tkinter as tk
from Back_End.notice_board.notice_controller import NoticeBoardController
from Back_End.Users.VolunteerController import VolunteerController
from Back_End.Charts.charts import ChartsController
import UI.dashboard_screen as dashboard

class VolAnalyticsScreen():
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

    def open_volunteers_camp_capacity_chart(self):
        notice = NoticeBoardController(self.connection)
        camp_id = notice.get_volunteer_camp(self.user_name)
        charts = ChartsController(self.connection)
        return charts.volunteer_camp_capacity_status(camp_id)

    def open_active_inactive_volunteers_chart(self):
        notice = NoticeBoardController(self.connection)
        camp_id = notice.get_volunteer_camp(self.user_name)
        charts = ChartsController(self.connection)
        return charts.active_inactive_volunteer_camp_status(camp_id)

    def open_volunteer_camp_medical_needs_chart(self):
        notice = NoticeBoardController(self.connection)
        camp_id = notice.get_volunteer_camp(self.user_name)
        charts = ChartsController(self.connection)
        return charts.volunteer_camp_medical_needs(camp_id)

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=5, rowspan=10)

        # get volunteer data
        self.volunteer_controller = VolunteerController(self.connection)
        volunteer = self.volunteer_controller.get_volunteer_details(self.user_name)
        self.camp = volunteer.camp_id

        heading = tk.Label(text="My Camp Insights", justify="center")
        heading.config(font=("Roboto", 32))
        heading.grid(column=2, row=1)

        tk.Label(text="Camp ID: %s" % self.camp).grid(column=2, row=3)

        # buttons
        volunteer_camp_capacity_status_button = tk.Button(text="Camp capacity status", padx=20, pady=10,
                                                command=self.open_volunteers_camp_capacity_chart)
        volunteer_camp_capacity_status_button.grid(column=2, row=4)

        active_inactive_volunteers_chart_button = tk.Button(text="Chart of active & inactive volunteers", padx=20,
                                                            pady=10, command=self.open_active_inactive_volunteers_chart)
        active_inactive_volunteers_chart_button.grid(column=2, row=5)

        open_volunteer_camp_medical_needs_chart_button = tk.Button(text="Camp medical status", padx=20, pady=10,
                                                            command=self.open_volunteer_camp_medical_needs_chart)
        open_volunteer_camp_medical_needs_chart_button.grid(column=2, row=6)

        # return button
        return_button = tk.Button(text="Return", command=self.return_back)
        return_button.grid(column=2, row=8, padx=20, pady=10)
