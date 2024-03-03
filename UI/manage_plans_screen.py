import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.constants import CENTER, END, NO, NSEW, W
import UI.dashboard_screen as dashboard
from Back_End.Camps.CampsController import *
from Back_End.Camps.Camps import *
from Back_End.Users.VolunteerController import *
from Back_End.Refugee_Profile.refugee_profile_controller import RefugeeProfileController
from Back_End.Emergency_Plan.EPController import EPController
from Back_End.Emergency_Plan.EmergencyPlan import Emergency
from tkcalendar import DateEntry
from datetime import date

class PlansScreen:
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.root.title('Refugee System | Emergency Plans')
        self.connection = connection
        self.camps_controller = CampsController(self.connection)   
        self.volunteer_controller = VolunteerController(self.connection)
        self.refugee_controller = RefugeeProfileController(self.connection)
        self.plan_controller = EPController(self.connection)
        self.user_name = user_name
        self.is_admin = is_admin

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def return_back(self):
        self.clear_window()
        dashboard.DashboardScreen(self.root, self.connection, self.user_name, self.is_admin).render()
    
    def populate_treeview(self, tree):
    # add data to the treeview from database
        plan_list = self.plan_controller.initialise()

        for plan in plan_list:           
            tree.insert('', index=tk.END, values=(plan.ep_id, plan.emergency_type, plan.description, plan.geog_area,
                                                  plan.camp_id, plan.start_date, plan.closing_date, plan.is_closed))

    def refresh_treeview(self, tree):
            tree.delete(*tree.get_children())
            self.populate_treeview(tree)

    def check_mandatory_fields(self, emergency_type, description, geog_area, camp_id, start_date, closing_date):
        if emergency_type == "Select Emergency Type" or not description or not geog_area or camp_id == "Select Camp" \
            or not start_date or not closing_date:
            tk.messagebox.showinfo(
                "Error!", "Make sure all fields are filled!")
            return False
        else:
            return True

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=10, rowspan=10) 

        label = tk.Label(text="Emergency Plans", justify="center")
        label.config(font=("Roboto", 32))
        label.grid(column=1, row=0)

        ## configure the treeview --------------------------------------------------------------------------
        tree_frame = tk.Frame()
        tree_frame.grid(row=2, column=1, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="F0F0F0", foreground="black", rowheight=25, fieldbackground="#F0F0F0")
        style.map("Treeview", background=[('selected', "#4F67F1")])

        # define columns
        columns = (
            'ep_id', 'emergency_type', 'description', 'location', 'camp_id', 'start_date', 'close_date', 'is_closed')

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")

        # format columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("ep_id", anchor=W, width=155, stretch=NO)
        tree.column("emergency_type", anchor=W, width=155, stretch=NO)
        tree.column("description", anchor=CENTER, width=155, stretch=NO)     
        tree.column("location", anchor=CENTER, width=155, stretch=NO)    
        tree.column("camp_id", anchor=CENTER, width=155, stretch=NO)    
        tree.column("start_date", anchor=CENTER, width=155, stretch=NO)    
        tree.column("close_date", anchor=CENTER, width=155, stretch=NO)    
        tree.column("is_closed", anchor=CENTER, width=155, stretch=NO)    

        # define headings
        tree.heading('ep_id', text='ID', anchor=W)
        tree.heading('emergency_type', text='Emergency Type', anchor=W)
        tree.heading('description', text='Description')
        tree.heading('location', text='Location')
        tree.heading('camp_id', text='Camp ID')
        tree.heading('start_date', text='Start Date')
        tree.heading('close_date', text='Close Date')
        tree.heading('is_closed', text='Is Closed')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns')

        # add data to the treeview from database
        self.populate_treeview(tree)

        ## Add record entry boxes --------------------------------------------------------------------------
        data_frame = ttk.LabelFrame(self.root, text="Emergency Record", style="Treeview")
        data_frame.grid(row = 3, column = 1, sticky=NSEW, padx=10, pady=10)

        id_label = tk.Label(data_frame, text="Plan ID").grid(row=0, column=0, padx=10, pady=10)
        plan_id_print = tk.StringVar(data_frame, "")
        id_print = tk.Label(data_frame, textvariable=plan_id_print).grid(row=0, column=1, padx=10, pady=10, sticky=W)

        OPTIONS1 = ["Flood","Earthquake","Tsunami","Tornado","Drought","Hurricane","Avalanche"]
        
        emergency_type_entry = tk.StringVar(data_frame)
        emergency_type_entry.set("Select Emergency Type") 
        emergency_type_label = tk.Label(data_frame, text="Emergency Type").grid(row=0, column=2, padx=10, pady=10)
        emergency_type_menu = tk.OptionMenu(data_frame,emergency_type_entry, *OPTIONS1)
        emergency_type_menu.grid(row=0, column=3, padx=10, pady=10, columnspan=1)
        emergency_type_menu.config(width=15)

        description_label = tk.Label(data_frame, text="Description").grid(row=0, column=4, padx=10, pady=10)
        description_entry = tk.Entry(data_frame)
        description_entry.grid(row=0, column=5, padx=10, pady=10)

        location_label = tk.Label(data_frame, text="Location").grid(row=0, column=6, padx=10, pady=10)
        location_entry = tk.Entry(data_frame)
        location_entry.grid(row=0, column=7, padx=10, pady=10)

        is_closed_label = tk.Label(data_frame, text="Is Closed").grid(row=1, column=6, padx=10, pady=10)
        is_closed_entry = tk.StringVar(data_frame, "")
        is_closed_print = tk.Label(
            data_frame, textvariable=is_closed_entry).grid(row=1, column=8, padx=10, pady=10, sticky=W)
                
        OPTIONS = self.camps_controller.get_list_of_camp_ids()
        if OPTIONS == []:
            OPTIONS = ["No camps"]

        camp_entry = tk.StringVar(data_frame)
        camp_entry.set("Select Camp") # default value

        camp_label = tk.Label(data_frame, text="Camp ID").grid(row=1, column=0, padx=10, pady=10)
        camp_menu = tk.OptionMenu(data_frame, camp_entry, *OPTIONS)
        camp_menu.grid(row=1, column=1, padx=10, pady=10)
        camp_menu.config(width=15)

        start_date_label = tk.Label(data_frame, text="Start Date").grid(row=1, column=2, padx=10, pady=10)
        start_date_entry = DateEntry(data_frame, width=12, background='darkblue',
                             foreground='white', borderwidth=2, year=2021, date_pattern='y-mm-dd')
        start_date_entry.grid(row=1, column=3, padx=10, pady=10)
        start_date_entry._top_cal.mainloop

        close_date_label = tk.Label(data_frame, text="Close Date").grid(row=1, column=4, padx=10, pady=10)
        close_date_entry = DateEntry(data_frame, width=12, background='darkblue',
                             foreground='white', borderwidth=2, year=2021, date_pattern='y-mm-dd')
        close_date_entry.grid(row=1, column=5, padx=10, pady=10)
        close_date_entry._top_cal.mainloop

        is_closed_label = tk.Label(data_frame, text="Is Closed").grid(row=1, column=6, padx=10, pady=10)
        is_closed_entry = tk.StringVar(data_frame, "")
        is_closed_print = tk.Label(
            data_frame, textvariable=is_closed_entry).grid(row=1, column=7, padx=10, pady=10, sticky=W)

    
        ## configure the treeview functions --------------------------------------------------------------------------
        def clear_entries():
            today = date.today()

            '''Treeview command: Clear entry boxes'''
            plan_id_print.set("")
            emergency_type_entry.set("Select Emergency Type") 
            description_entry.delete(0, END)
            location_entry.delete(0, END)
            camp_entry.set("Select Camp")
            start_date_entry.set_date(today)
            close_date_entry.set_date(today)
            is_closed_entry.set("")

        
        def select_plan(e):
            '''Treeview function: Select records + print to entry boxes'''
            # clear entry boxes
            clear_entries()

            # store selected record number
            selected = tree.focus()

            # get record values
            values = tree.item(selected, 'values')

            #output to entry boxes
            plan_id_print.set(values[0])
            emergency_type_entry.set(values[1])
            description_entry.insert(0, values[2])
            location_entry.insert(0, values[3])
            camp_entry.set(values[4])
            start_date_entry.set_date(values[5])
            close_date_entry.set_date(values[6])
            is_closed_entry.set(values[7])

        def move_up():
            '''Treeview command: Move row up'''
            rows = tree.selection()
            
            for row in rows:
                tree.move(row, tree.parent(row), tree.index(row)-1)

        def move_down():
            '''Treeview command: Move row down'''
            rows = tree.selection()
            
            for row in reversed(rows ):
                tree.move(row, tree.parent(row), tree.index(row)+1)
        
        def remove_selected():
            '''Treeview command: Remove selected plans'''
            # store selections
            selected = tree.selection()
            if not selected:
                tk.messagebox.showinfo("Error!", "You have not selected any plans!")
                return

            # Confirm delete from user
            response = tk.messagebox.askyesno("Caution!", "Are you sure you want to delete these Emergency Plans?")

            if response == 1:
                # loop over selected records and delete
                for plan in selected:
                    values = tree.item(plan, 'values')

                    plan_id = values[0]

                    result = self.plan_controller.delete_emergency_plan(plan_id)
                    
                    if result != True:
                        # error message
                        tk.messagebox.showinfo("Error!", result)
                        return

                # confirmation message
                tk.messagebox.showinfo("Deleted", "Plan(s) deleted from database")

                # refresh the treeview
                self.refresh_treeview(tree)
         
        
        def update_plan():
            '''Treeview command: Updates records from entry box input'''
            # get selected EP ID
            selected = tree.focus()
            values = tree.item(selected, 'values')
          
            if values:
                plan_id = str(values[0])
            else:
                tk.messagebox.showinfo("Error!", "Please select a plan to update!")
                return

            # get updated inputs
            emergency_type = emergency_type_entry.get()
            description = description_entry.get()
            location = location_entry.get()
            camp_id = camp_entry.get()
            start_date = str(start_date_entry.get_date())
            close_date = str(close_date_entry.get_date())
            is_closed_text = is_closed_entry.get()
            
            if is_closed_text == "OPEN":
                is_closed = 0
            else:
                is_closed = 1

            if self.check_mandatory_fields(
                    emergency_type, description, location, camp_id, start_date, close_date) == False:
                return

            # update object
            plan = Emergency(plan_id, emergency_type, description, location, camp_id, start_date, close_date, is_closed)

            # update plan
            result = self.plan_controller.update_ep(plan)

            if result != True:
                # error message
                tk.messagebox.showinfo("Error!", result)

            # update tree
            self.refresh_treeview(tree)

            # clear entry boxes
            clear_entries()

        def add_plan():
            '''Treeview command: Adds records from entry box input'''
            # get new inputs
            emergency_type = emergency_type_entry.get()
            description = description_entry.get()
            location = location_entry.get()
            camp_id = camp_entry.get()
            start_date = str(start_date_entry.get_date())
            close_date = str(close_date_entry.get_date())
            
            is_closed_text = is_closed_entry.get()
            
            if is_closed_text == "OPEN":
                is_closed = 0
            else:
                is_closed = 1

            if self.check_mandatory_fields(
                    emergency_type, description, location, camp_id, start_date, close_date) == False:
                return

            # add object
            plan = Emergency(None, emergency_type, description, location, camp_id, start_date, close_date, is_closed)
            result = self.plan_controller.save(plan)

            if result != True:
                # error message
                tk.messagebox.showinfo("Error!", result)

            else:
                # Confirmation message
                tk.messagebox.showinfo("Added", "Plan added to database")
        
            # clear entry boxes
            clear_entries()

            # refresh the treeview
            self.refresh_treeview(tree)

        def open_close_plan():
            # get selected plan
            selected = tree.focus()
            if not selected:
                tk.messagebox.showinfo("Error!", "You have not selected any plans!")
                return
            
            values = tree.item(selected, 'values')
            plan_id = str(values[0])

            # get updated inputs
            emergency_type = emergency_type_entry.get()
            description = description_entry.get()
            location = location_entry.get()
            camp_id = int(camp_entry.get())
            start_date = str(start_date_entry.get_date())
            close_date = str(close_date_entry.get_date())
            is_closed_text = is_closed_entry.get()

            if is_closed_text == "OPEN":
                is_closed = 0
            else:
                is_closed = 1

            # update open/closed status
            plan = Emergency(plan_id, emergency_type, description, location, camp_id, start_date, close_date, is_closed)
            self.plan_controller.open_or_close_plan(plan)
            self.refresh_treeview(tree)
            
            #clear entry boxes
            clear_entries()


        # command buttons -------------------------------------------------------------------------------
        
        command_frame = ttk.LabelFrame(self.root, text="Commands", style="Treeview")
        command_frame.grid(row = 4, column = 1, sticky=NSEW, padx=10, pady=10)

        update_button = tk.Button(command_frame, text="Update Plan", command=update_plan)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(command_frame, text="Add Plan", command=add_plan)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = tk.Button(command_frame, text="Remove Selected Plans", command=remove_selected)
        remove_one_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = tk.Button(command_frame, text="Move Record Up", command=move_up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = tk.Button(command_frame, text="Move Record Down", command=move_down)
        move_down_button.grid(row=0, column=5 , padx=10, pady=10)
 
        edit_button = tk.Button(command_frame, text="Clear", command=clear_entries)
        edit_button.grid(row=0, column=6, padx=10, pady=10)

        open_close_button = tk.Button(command_frame, text="Open/Close Plan", command=open_close_plan)
        open_close_button.grid(row=0, column=7, padx=10, pady=10)

        # return button --------------------------------------------------------------------------------
        return_button = tk.Button(text="Return", command=self.return_back)
        return_button.grid(column=1, row=5, padx=20, pady=10)

        # display tree  --------------------------------------------------------------------------------
        # tree.bind('<<TreeviewSelect>>', self.item_selected)
        tree.bind("<ButtonRelease-1>", select_plan)
        tree.grid(row=2, column=1, sticky ='n')
