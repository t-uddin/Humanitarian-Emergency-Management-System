import tkinter as tk
import UI.register_screen as register_screen
import UI.login_screen as login_screen

class LandingScreen:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title('Refugee System | Welcome')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=5, rowspan=5)

        logo_label = tk.Label(text="Refugee System", justify="center")
        logo_label.config(font=("Roboto", 32))
        logo_label.grid(column=2, row=0)

        login_button = tk.Button(text="Login", padx=20,
                                 pady=10, width=15, command=self.openLogin)
        login_button.grid(column=1, row=2)

        register_button = tk.Button(
            text="Register", padx=20, pady=10, width=15, command=self.openRegister)
        register_button.grid(column=3, row=2)

    def openLogin(self):
        self.clear_window()
        login_screen.LoginScreen(self.root, self.connection).render()

    def openRegister(self):
        self.clear_window()
        register_screen.RegisterScreen(self.root, self.connection).render()
