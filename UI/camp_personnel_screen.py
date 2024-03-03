import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, NO, W
from Back_End.Users.VolunteerStatusController import VolunteerStatusController
import UI.admin_analytics_screen as analytics_screen

class PersonnelScreen:
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.root.title('Refugee System | Camp Volunteer Status')
        self.connection = connection
        self.volunteer_status_controller = VolunteerStatusController(
            connection)
        self.user_name = user_name
        self.is_admin = is_admin

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def return_back(self):
        self.clear_window()
        analytics_screen.AdminAnalyticsScreen(self.root, self.connection, self.user_name, self.is_admin).render()

    def populate_treeview(self, tree):
        # add data to the treeview from database
        volunteers_list = self.volunteer_status_controller.initialise()

        for obj in volunteers_list:
            tree.insert('', index=tk.END, values=(obj.camp_id, obj.monday, obj.tuesday,
                        obj.wednesday, obj.thursday, obj.friday, obj.saturday, obj.sunday))

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=10, rowspan=10)

        label = tk.Label(text="Camps", justify="center")
        label.config(font=("Roboto", 32))
        label.grid(column=1, row=0)

        label_info = tk.Label(text="Number of Volunteers needed displayed below", justify="center")
        label_info.config(font=("Roboto", 16))
        label_info.grid(column=1, row=1)

        # configure the treeview ---------------------------------------------------------------------
        tree_frame = tk.Frame()
        tree_frame.grid(row=2, column=1, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="F0F0F0",
                        foreground="black", rowheight=25, fieldbackground="#F0F0F0")
        style.map("Treeview", background=[('selected', "#4F67F1")])

        # define columns
        columns = ('camp_id', 'monday', 'tuesday', 'wednesday',
                   'thursday', 'friday', 'saturday', 'sunday')

        tree = ttk.Treeview(tree_frame, columns=columns,
                            show='headings', selectmode="extended")

        # # format columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("camp_id", anchor=W, width=180, stretch=NO)
        tree.column("monday", anchor=CENTER, width=180, stretch=NO)
        tree.column("tuesday", anchor=CENTER, width=180, stretch=NO)
        tree.column("wednesday", anchor=CENTER, width=180, stretch=NO)
        tree.column("thursday", anchor=CENTER, width=180, stretch=NO)
        tree.column("friday", anchor=CENTER, width=180, stretch=NO)
        tree.column("saturday", anchor=CENTER, width=180, stretch=NO)
        tree.column("sunday", anchor=CENTER, width=180, stretch=NO)

        # # define headings
        tree.heading('camp_id', text='Camp ID', anchor=W)
        tree.heading('monday', text='Monday')
        tree.heading('tuesday', text='Tueday')
        tree.heading('wednesday', text='Wednesday')
        tree.heading('thursday', text='Thursday')
        tree.heading('friday', text='Friday')
        tree.heading('saturday', text='Saturday')
        tree.heading('sunday', text='Sunday')

        # # add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns')

        # # add data to the treeview from database
        self.populate_treeview(tree)

        # return button --------------------------------------------------------------------------------
        return_button = tk.Button(text="Return", command=self.return_back)
        return_button.grid(column=1, row=5, padx=20, pady=10)

        # display tree  --------------------------------------------------------------------------------
        tree.grid(row=2, column=1, sticky='n')
