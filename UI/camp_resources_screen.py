import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, NO, W
import UI.admin_analytics_screen as admin_analytics_screen
from Back_End.Camps.CampsStatusController import CampsStatusController

class ResourcesScreen:
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.root.title('Refugee System | Camp Resources Status')
        self.connection = connection
        self.camp_status_controller = CampsStatusController(connection)
        self.user_name = user_name
        self.is_admin = is_admin

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def return_back(self):
        self.clear_window()
        admin_analytics_screen.AdminAnalyticsScreen(self.root, self.connection, self.user_name, self.is_admin).render()

    def populate_treeview(self, tree):
    # add data to the treeview from database
        camps_list = self.camp_status_controller.initialise()

        for obj in camps_list:
            tree.insert('', index=tk.END, values=(obj.name, obj.id, obj.location, obj.capacity_status,
                                                  obj.medicine_status, obj.food_status))

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=10, rowspan=10)

        label = tk.Label(text="Camp Resources", justify="center")
        label.config(font=("Roboto", 32))
        label.grid(column=1, row=0)

        ## configure the treeview ---------------------------------------------------------------------
        tree_frame = tk.Frame()
        tree_frame.grid(row=2, column=1, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="F0F0F0", foreground="black", rowheight=25, fieldbackground="#F0F0F0")
        style.map("Treeview", background=[('selected', "#4F67F1")])

        # define columns
        columns = ('camp_name', 'camp_id', 'location', 'capacity_status', 'medicine_status', 'food_status')

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")
            
        # # format columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("camp_name", anchor=W, width=180, stretch=NO)
        tree.column("camp_id", anchor=CENTER, width=180, stretch=NO)
        tree.column("location", anchor=CENTER, width=180, stretch=NO)     
        tree.column("capacity_status", anchor=CENTER, width=180, stretch=NO)    
        tree.column("medicine_status", anchor=CENTER, width=180, stretch=NO)    
        tree.column("food_status", anchor=CENTER, width=180, stretch=NO)

        # # define headings
        tree.heading('camp_name', text='Camp Name', anchor=W)
        tree.heading('camp_id', text='Camp ID')
        tree.heading('location', text='Location')
        tree.heading('capacity_status', text='Capacity Status')
        tree.heading('medicine_status', text='Medicine Status')
        tree.heading('food_status', text='Food Status')

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
        tree.grid(row=2, column=1, sticky ='n')