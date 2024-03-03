import tkinter as tk
import UI.landing_screen as landing_screen
import UI.dashboard_screen as dashboard_screen
import Back_End.Users.UserController as user_controller

class LoginScreen:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title('Refugee System | Login')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=5, rowspan=5)

        label = tk.Label(text="Login", justify="center")
        label.config(font=("Roboto", 32))
        label.grid(column=2, row=0)

        tk.Label(text="Username").grid(row=1, column=1)
        tk.Label(text="Password").grid(row=2, column=1)

        user_name = tk.Entry(width=25)
        user_name.grid(row=1, column=2)
        password = tk.Entry(width=25, show="*")
        password.grid(row=2, column=2)

        return_button = tk.Button(text="Return", padx=20,
                                  pady=10, command=self.return_back)
        return_button.grid(column=1, row=3)

        login_button = tk.Button(text="Login", padx=20, pady=10,
                                 command=lambda: self.authenticate(user_name.get(), password.get()))
        login_button.grid(column=3, row=3)

    def authenticate(self, user_name, password):
        uc = user_controller.UserController(self.connection)
        if not user_name or not password:
            tk.messagebox.showinfo(
                "Error!", "Make sure all the mandatory fields are filled!")
            return

        try:
            user = uc.login_function(user_name, password)
            self.clear_window()
            dashboard_screen.DashboardScreen(
                self.root, self.connection, user["user_name"], user["is_admin"]).render()
        except Exception as e:
            tk.messagebox.showinfo(
                "Error!", str(e))
            return

    def return_back(self):
        self.clear_window()
        landing_screen.LandingScreen(self.root, self.connection).render()
