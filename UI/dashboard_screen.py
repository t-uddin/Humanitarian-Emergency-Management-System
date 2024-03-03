import tkinter as tk
from tkinter.constants import W
import UI.camp_personnel_screen as personnel_screen
import UI.camp_resources_screen as resources_screen
import UI.manage_plans_screen as plans_screen
import UI.manage_refugees_screen as refugees_screen
import UI.manage_volunteers_screen as volunteers_screen
import UI.manage_camps_screen as camps_screen
import UI.volunteer_info_screen as volunteer_info_screen
import UI.volunteer_analytics_screen as volunteer_analytics_screen
import UI.admin_analytics_screen as admin_analytics_screen
import UI.manage_notice_board_screen_admin as notice_admin
import UI.manage_notice_board_screen_volunteer as notice_vol
import UI.landing_screen as landing_screen
import Back_End.Maps.maps as maps
from Back_End.Users.VolunteerController import *
from Back_End.Camps.CampsController import *

class DashboardScreen:
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.connection = connection
        self.user_name = user_name
        self.is_admin = is_admin
        self.root.title('Refugee System | Home')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def logout(self):
        self.clear_window()
        landing_screen.LandingScreen(self.root, self.connection).render()

    def openPlans(self):
        self.clear_window()
        plans_screen.PlansScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openRefugees(self):
        self.clear_window()
        refugees_screen.RefugeesScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openVolunteers(self):
        self.clear_window()
        volunteers_screen.VolunteersScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openCamps(self):
        self.clear_window()
        camps_screen.CampsScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openEditMyInfo(self):
        self.clear_window()
        volunteer_info_screen.VolunteerInfoScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openCampsResources(self):
        self.clear_window()
        resources_screen.ResourcesScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openCampsPersonnel(self):
        self.clear_window()
        personnel_screen.PersonnelScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openMap(self):
        maps.MapsController(self.connection).generate_map()

    def openNoticeAdmin(self):
        self.clear_window()
        notice_admin.NoticeAdminScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openNoticeVol(self):
        self.clear_window()
        notice_vol.NoticeVolunteerScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openAnalyticsVol(self):
        self.clear_window()
        volunteer_analytics_screen.VolAnalyticsScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def openAnalyticsAdmin(self):
        self.clear_window()
        admin_analytics_screen.AdminAnalyticsScreen(
            self.root, self.connection, self.user_name, self.is_admin).render()

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=5, rowspan=10)

        if self.is_admin == True:
            heading = tk.Label(text="Admin Home", justify="center")
            heading.config(font=("Roboto", 32))
            heading.grid(column=2, row=1)

            plans_button = tk.Button(
                text="Emergency Plans", padx=20, pady=10, command=self.openPlans)
            plans_button.grid(column=1, row=3)

            refugee_button = tk.Button(
                text="Refugees", padx=20, pady=10, command=self.openRefugees)
            refugee_button.grid(column=1, row=4)

            volunteer_button = tk.Button(
                text="Volunteers", padx=20, pady=10, command=self.openVolunteers)
            volunteer_button.grid(column=1, row=5)

            camps_button = tk.Button(
                text="Camps", padx=20, pady=10, command=self.openCamps)
            camps_button.grid(column=1, row=6)

            admin_insights_button = tk.Button(
                text="Camp Analytics", padx=20, pady=10, command=self.openAnalyticsAdmin)
            admin_insights_button.grid(column=3, row=3)

            admin_insights_button = tk.Button(
                text="Map of Camps", padx=20, pady=10, command=self.openMap)
            admin_insights_button.grid(column=3, row=4)

            notice_button = tk.Button(
                text="Notice Board", padx=20, pady=10, command=self.openNoticeAdmin)
            notice_button.grid(column=3, row=5)

            logout_button = tk.Button(text="Log out", command=self.logout)
            logout_button.grid(column=2, row=8, padx=20, pady=10)

        elif self.is_admin == False:
            # get volunteer data
            self.volunteer_controller = VolunteerController(self.connection)
            volunteer = self.volunteer_controller.get_volunteer_details(self.user_name)
            self.camp = volunteer.camp_id
            self.availability = volunteer.availability
           
            heading = tk.Label(text="Volunteer Home", justify="center")
            heading.config(font=("Roboto", 32))
            heading.grid(column=2, row=1)

            if self.camp == "None":
                tk.Label(text="You have not yet been assigned a camp.",
                         font='Helvetica 18 bold').grid(column=2, row=3)
                tk.Label(text="My availability: %s" %
                         self.availability).grid(column=2, row=4)

                edit_info_button = tk.Button(
                    text="Edit My Info", padx=20, pady=10, command=self.openEditMyInfo)
                edit_info_button.grid(column=2, row=5)
                logout_button = tk.Button(
                    text="Log Out", padx=20, pady=10, command=self.logout)
                logout_button.grid(column=2, row=6)

            else:
                self.camps_controller = CampsController(self.connection)
                camp_name = self.camps_controller.get_camp_name(self.camp)

                self.map_controller = MapsController(self.connection)
                
                weather_api_working = True

                try:
                    weather = maps.asyncio.run(self.map_controller.getweather(self.camp))
                except:
                    weather_api_working = False

                edit_info_button = tk.Button(
                    text="Edit My Info", padx=20, pady=10, command=self.openEditMyInfo)
                edit_info_button.grid(column=1, row=6)

                logout_button = tk.Button(text="Log out", command=self.logout)
                logout_button.grid(column=2, row=8, padx=20, pady=10)

                tk.Label(text="My availability: %s" %self.availability, font='Helvetica 14 bold',
                         anchor=W).grid(column=1, row=3)
                
                if weather_api_working:         
                    tk.Label(text="My Camp: %s" % camp_name, font='Helvetica 14 bold',
                         anchor=W).grid(column=1, row=4)
                    tk.Label(text=f"Temperature: {weather[0]} degrees, Conditions: {weather[1]}",
                         anchor=W).grid(column=1, row=5)
                
                refugees_button = tk.Button(
                    text="Create Refugee Profile", padx=20, pady=10, command=self.openRefugees)
                refugees_button.grid(column=3, row=3)

                vol_insights_button = tk.Button(
                    text="Camp Insights", padx=20, pady=10, command=self.openAnalyticsVol)
                vol_insights_button.grid(column=3, row=4)

                notice_button = tk.Button(
                    text="Notice Board", padx=20, pady=10, command=self.openNoticeVol)
                notice_button.grid(column=3, row=5)
