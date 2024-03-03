import tkinter as tk
from Back_End.Users.VolunteerController import VolunteerController
from Back_End.Users.Volunteer import Volunteer
import UI.dashboard_screen as dashboard
from tkinter.constants import W


class VolunteerInfoScreen:
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.root.title('Refugee System | Volunteer Info')

        self.user_name = user_name
        self.is_admin = is_admin        
        self.connection = connection
        self.volunteer_controller = VolunteerController(self.connection)

        # get volunteer data
        volunteer = self.volunteer_controller.get_volunteer_details(self.user_name)

        self.password = volunteer.password
        self.first_name = volunteer.first_name
        self.last_name = volunteer.last_name
        self.phone = volunteer.phone_number
        self.is_active = volunteer.is_active
        self.address = volunteer.address
        self.camp = volunteer.camp_id
        self.availability = volunteer.availability

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def return_back(self):
        self.clear_window()
        dashboard.DashboardScreen(self.root, self.connection, self.user_name, self.is_admin).render()
        
    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=5, rowspan=10)

        # title
        label = tk.Label(text="Edit My Info", justify="center")
        label.config(font=("Roboto", 32))
        label.grid(column=2, row=0)

        # input labels
        tk.Label(text="Username", justify="right").grid(row=1, column=1)
        tk.Label(text="First Name", justify="right").grid(row=2, column=1)
        tk.Label(text="Last Name", justify="right").grid(row=3, column=1)
        tk.Label(text="Phone", justify="right").grid(row=4, column=1)
        tk.Label(text="Address", justify="right").grid(row=5, column=1)
        tk.Label(text="Availability", justify="right").grid(row=6, column=1)

        # data boxes
        username = tk.StringVar(self.root, self.user_name)
        username_print = tk.Label(textvariable=username)
        username_print.grid(row=1, column=2, columnspan=2, padx=60, pady=10, sticky=W)

        first_name_entry = tk.Entry(self.root, width=35, justify="left")
        first_name_entry.grid(row=2, column=2, columnspan=2)

        last_name_entry = tk.Entry(self.root, width=35, justify="left")
        last_name_entry.grid(row=3, column=2, columnspan=2)

        def IntValidation(S):
            if S.isdigit():
                return True
            else:
                self.root.bell()
                return False

        vcmd = (self.root.register(IntValidation), '%S')
        phone_entry = tk.Entry(self.root, width=35, justify="left", validate='key', validatecommand=vcmd)
        phone_entry.grid(row=4, column=2, columnspan=2)

        address_entry = tk.Entry(self.root, width=35, justify="left")
        address_entry.grid(row=5, column=2, columnspan=2)

        availability_entry = tk.Entry(self.root, width=35, justify="left")
        availability_entry.grid(row=6, column=2, columnspan=2)

        # pre-fill input boxes
        username.set(self.user_name)
        first_name_entry.insert(0, self.first_name)
        last_name_entry.insert(0, self.last_name)
        phone_entry.insert(0, self.phone)
        address_entry.insert(0, self.address)
        availability_entry.insert(0, self.availability)

        def update_profile():
            # get updated inputs
            username = self.user_name
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()
            availability = availability_entry.get()

            # create volunteer object
            password = self.password
            is_admin = self.is_admin
            is_active = self.is_active
            camp = self.camp

            volunteer = Volunteer(
                username, password, is_admin, first_name, last_name, is_active, phone, address, camp, availability)

            # update
            result = self.volunteer_controller.update_volunteer(volunteer)
            
            if result != True:
                # error message
                tk.messagebox.showinfo("Error!", result)
                return

            else:
                # confirmation message
                tk.messagebox.showinfo("Confirmation", "Account updated")
                self.return_back()

        # buttons
        return_button = tk.Button(text="Return", padx=20,
                                  pady=10, command=self.return_back)
        return_button.grid(column=1, row=8)

        update_button = tk.Button(text="Update", padx=20, pady=10,
                                  command=update_profile)
        update_button.grid(column=3, row=8)
