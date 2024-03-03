import tkinter as tk
import UI.login_screen as login_screen
import UI.landing_screen as landing_screen
import Back_End.Users.VolunteerController as volunteer_controller
import Back_End.Users.Volunteer as Volunteer


class RegisterScreen:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title('Refugee System | Register')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def return_back(self):
        self.clear_window()
        landing_screen.LandingScreen(self.root, self.connection).render()

    def register(self, user_name, first_name, last_name, phone_number, availability, password, confirm_password):
        if not first_name or not last_name or not user_name or not phone_number \
                or not availability or not password or not confirm_password:
            tk.messagebox.showinfo(
                "Error!", "Make sure all the mandatory fields are filled!")
            return
        if len(availability) != 7 or any(c not in 'TF' for c in availability):
            tk.messagebox.showinfo(
                "Error!",
                "Make sure availability field contains only T and F and each letter represents 7 days in a week!")
            return
        try:
            int(phone_number)
        except ValueError:
            tk.messagebox.showinfo(
                "Error!", "Phone Number format is incorrect!")
            return
        if password != confirm_password:
            tk.messagebox.showinfo(
                "Error!", "Passwords don't match")
            return
        v = Volunteer.Volunteer(user_name, password, 0, first_name, last_name, 1,
                                phone_number, None, None, availability)
        vc = volunteer_controller.VolunteerController(self.connection)
        try:
            res = vc.add_volunteer(v)
            if res == False:
                tk.messagebox.showinfo(
                    "Error!", "Username cannot be blank!")
                return
            else:
                self.clear_window()
                login_screen.LoginScreen(self.root, self.connection).render()
        except:
            tk.messagebox.showinfo(
                "Error!", "Username cannot be blank!")
            return

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=5, rowspan=10)

        label = tk.Label(text="Register as a volunteer:", justify="center")
        label.config(font=("Roboto", 32))
        label.grid(column=2, row=0)

        tk.Label(text="First Name:").grid(column=1, row=1)
        first_name_input = tk.Entry(width=25)
        first_name_input.grid(row=1, column=2)

        tk.Label(text="Last Name:").grid(column=1, row=2)
        last_name_input = tk.Entry(width=25)
        last_name_input.grid(row=2, column=2)

        tk.Label(text="Username:").grid(column=1, row=3)
        username_input = tk.Entry(width=25)
        username_input.grid(row=3, column=2)

        def IntValidation(S):
            if S.isdigit():
                return True
            else:
                self.root.bell()
                return False

        vcmd = (self.root.register(IntValidation), '%S')
        tk.Label(text="Phone Number:").grid(column=1, row=4)
        phone_input = tk.Entry(width=25, validate='key', validatecommand=vcmd)
        phone_input.grid(column=2, row=4)

        tk.Label(text="Availablity (e.g. TTTTTFF):").grid(column=1, row=5)
        availability = tk.Entry(width=25)
        availability.grid(column=2, row=5)

        tk.Label(text="Password:").grid(column=1, row=6)
        password_input = tk.Entry(width=25, show="*")
        password_input.grid(column=2, row=6)

        tk.Label(
            text="Confirm Password:").grid(column=1, row=7)
        password2_input = tk.Entry(width=25, show="*")
        password2_input.grid(column=2, row=7)

        return_button = tk.Button(
            text="Return", padx=20, pady=10, command=self.return_back)
        return_button.grid(column=1, row=9)

        register_button = tk.Button(text="Register", padx=20, pady=10,
                                    command=lambda: self.register(
                                        username_input.get(), first_name_input.get(), last_name_input.get(),
                                        phone_input.get(), availability.get(), password_input.get(),
                                        password2_input.get()))
        register_button.grid(column=3, row=9)
