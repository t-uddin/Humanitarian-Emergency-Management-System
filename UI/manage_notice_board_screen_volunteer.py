import tkinter as tk
from tkinter import ttk
from tkinter.constants import NO, W
import UI.dashboard_screen as dashboard
from Back_End.Camps.CampsStatusController import CampsStatusController

from Back_End.notice_board.notice_controller import NoticeBoardController

class NoticeVolunteerScreen:
    def __init__(self, root, connection, username, is_admin):
        self.root = root
        self.root.title('Refugee System | Volunteer Notice Board')
        self.connection = connection
        self.username = username
        self.is_admin = is_admin

        self.camp_status_controller = CampsStatusController(connection)
        self.notice_controller = NoticeBoardController(connection)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def return_back(self):
        self.clear_window()
        dashboard.DashboardScreen(self.root, self.connection,self.username, self.is_admin).render()

    def populate_treeview(self, tree):
    # add data to the treeview from database
        camp_id = self.notice_controller.get_volunteer_camp(self.username)
        notice_list = self.notice_controller.get_notices(camp_id)

        for notice in notice_list:
            tree.insert('', index=tk.END, values=(notice.message_id, notice.message))

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=10, rowspan=10)

        label = tk.Label(text="Notice Board", justify="center")
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
        columns = ('message_id','message')

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")
            
        # # format columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("message_id", anchor=W, width=80, stretch=NO)
        tree.column("message", anchor=W, width=1000, stretch=NO)     


        # # define headings
        tree.heading('message_id', text='Message ID', anchor=W)
        tree.heading('message', text='Message', anchor=W)

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
        # tree.bind("<ButtonRelease-1>", select_camp)
        tree.grid(row=2, column=1, sticky ='n')
