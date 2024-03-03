import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, END, NO, NSEW, W
import UI.dashboard_screen as dashboard
from Back_End.Refugee_Profile.refugee_profile_controller import RefugeeProfileController
from Back_End.Camps.CampsController import *
from Back_End.Camps.Camps import *
from Back_End.Users.VolunteerController import *
class CampsScreen:
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.root.title('Refugee System | Camps')
        self.connection = connection
        self.camps_controller = CampsController(self.connection)
        self.volunteer_controller = VolunteerController(self.connection)
        self.refugee_controller = RefugeeProfileController(self.connection)
        self.user_name = user_name
        self.is_admin = is_admin
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def return_back(self):
        self.clear_window()
        dashboard.DashboardScreen(self.root, self.connection, self.user_name, self.is_admin).render()

    def populate_treeview(self, tree):
        #add data to the treeview from database
    
        camps_list = self.camps_controller.initialise()

        for camp in camps_list:
            camp_id = camp.id
            num_volunteers = self.volunteer_controller.get_number_volunteers_by_camp(camp_id)

            capacity_fraction = self.camps_controller.get_capacity_fraction(camp)

            tree.insert('', index=tk.END, values=(camp.id, camp.name, camp.location, num_volunteers, capacity_fraction,
                                                  camp.food, camp.medicine))

    def refresh_treeview(self, tree):
        tree.delete(*tree.get_children())
        self.populate_treeview(tree)

    def check_mandatory_fields(self, camp):
        if not camp.name or not camp.location or not camp.capacity or not camp.medicine or not camp.food:
            tk.messagebox.showinfo(
                "Error!", "Make sure all fields are filled!")
            return False
        else:
            return True

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=10, rowspan=10) 

        label = tk.Label(text="Camps", justify="center")
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
        columns = ('camp_id', 'camp_name', 'location', 'num_volunteers', 'capacity', 'food', 'num_med')

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")
            
        # format columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("camp_id", anchor=W, width=180, stretch=NO)
        tree.column("camp_name", anchor=W, width=180, stretch=NO)
        tree.column("location", anchor=CENTER, width=180, stretch=NO)     
        tree.column("num_volunteers", anchor=CENTER, width=180, stretch=NO)    
        tree.column("capacity", anchor=CENTER, width=180, stretch=NO)    
        tree.column("food", anchor=CENTER, width=180, stretch=NO)    
        tree.column("num_med", anchor=CENTER, width=180, stretch=NO)    

        # define headings
        tree.heading('camp_id', text='ID', anchor=W)
        tree.heading('camp_name', text='Camp', anchor=W)
        tree.heading('location', text='Location')
        tree.heading('num_volunteers', text='No. Volunteers')
        tree.heading('capacity', text='Capacity')
        tree.heading('food', text='Food Packs')
        tree.heading('num_med', text='Medical Kits')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns')

        # add data to the treeview from database
        self.populate_treeview(tree)
        
        ## Add record entry boxes ----------------------------------------------------------------------  
        data_frame = ttk.LabelFrame(self.root, text="Camp Record", style="Treeview")
        data_frame.grid(row = 3, column = 1, sticky=NSEW, padx=10, pady=10)

        def IntValidation(S):
            if S.isdigit():
                return True
            else:
                data_frame.bell()
                return False
        
        id_label = tk.Label(data_frame, text="Camp ID").grid(row=0, column=0, padx=10, pady=10)
        camp_id = tk.StringVar(data_frame, "")
        id_print = tk.Label(data_frame, textvariable=camp_id).grid(row=0, column=1, padx=10, pady=10, sticky=W)

        camp_name_label = tk.Label(data_frame, text="Camp Name").grid(row=0, column=2, padx=10, pady=10)
        camp_name_entry = tk.Entry(data_frame)
        camp_name_entry.grid(row=0, column=3, padx=10, pady=10)

        location_label = tk.Label(data_frame, text="Location").grid(row=0, column=4, padx=10, pady=10)
        location_entry = tk.Entry(data_frame)
        location_entry.grid(row=0, column=5, padx=10, pady=10)

        num_volunteers_label = tk.Label(data_frame, text="No. Volunteers").grid(row=0, column=6, padx=10, pady=10)
        num_volunteers_value = tk.StringVar(data_frame, "")
        num_volunteers_print = tk.Label(
            data_frame, textvariable=num_volunteers_value).grid(row=0, column=7, padx=10, pady=10, sticky=W)

        vcmd = (data_frame.register(IntValidation), '%S')

        capacity_label = tk.Label(data_frame, text="Max. Capacity").grid(row=1, column=0, padx=10, pady=10)
        capacity_entry = tk.Entry(data_frame, validate='key', validatecommand=vcmd)
        capacity_entry.grid(row=1, column=1, padx=10, pady=10)

        food_label = tk.Label(data_frame, text="No. Food Packs").grid(row=1, column=2, padx=10, pady=10)
        food_entry = tk.Entry(data_frame, validate='key', validatecommand=vcmd)
        food_entry.grid(row=1, column=3, padx=10, pady=10)

        num_med_label = tk.Label(data_frame, text="No. Medical Kits").grid(row=1, column=4, padx=10, pady=10)
        num_med_entry = tk.Entry(data_frame, validate='key', validatecommand=vcmd)
        num_med_entry.grid(row=1, column=5, padx=10, pady=10)


        ## configure the treeview functions ---------------------------------------------------------------
        def clear_entries():
            '''Treeview command: Clear entry boxes'''
            camp_id.set("")
            camp_name_entry.delete(0, END)
            location_entry.delete(0, END)
            num_volunteers_value.set("")
            capacity_entry.delete(0, END)
            food_entry.delete(0, END)
            num_med_entry.delete(0, END)
        
        def select_camp(e):
            '''Treeview function: Select records + print to entry boxes'''
            # clear entry boxes
            clear_entries()

            # store selected record number
            selected = tree.focus()

            # get record values
            values = tree.item(selected, 'values')
            selected_camp_id = values[0]

            #output to entry boxes
            camp_id.set(values[0])
            camp_name_entry.insert(0, values[1])
            location_entry.insert(0, values[2])
            num_volunteers = self.volunteer_controller.get_number_volunteers_by_camp(selected_camp_id)
            num_volunteers_value.set(num_volunteers)
            max_capacity = self.camps_controller.get_max_capacity(selected_camp_id)
            capacity_entry.insert(0, max_capacity)
            food_entry.insert(0, values[5])
            num_med_entry.insert (0, values[6])

        def move_up():
            '''Treeview command: Move row up'''
            rows = tree.selection()
            
            for row in rows:
                tree.move(row, tree.parent(row), tree.index(row)-1)

        def move_down():
            '''Treeview command: Move row down'''
            rows = tree.selection()
            
            for row in reversed(rows):
                tree.move(row, tree.parent(row), tree.index(row)+1)
                    
        def remove_selected():
            '''Treeview command: Remove many camps'''
            # check selections
            selected = tree.selection()
                    
            if not selected:
                tk.messagebox.showinfo("Error!", "You have not selected any camps!")
                return
            
            # Confirm delete from user
            response = tk.messagebox.askyesno("Caution!", "Are you sure you want to delete these camps?")

            if response == 1:
                # loop over selected records and delete
                for camp in selected:
                    values = tree.item(camp, 'values')

                    camp_id = values[0]
                    name = values[1]
                    location = values[2]
                    med = int(values[3])
                    capacity  = self.camps_controller.get_max_capacity(camp_id)
                    food = int(values[5])

                    # delete camp from camps tables
                    camp = Camps(name, camp_id, location, capacity, med, food)
                    result = self.camps_controller.delete_camp(camp)

                    if result != True:
                        # error message
                        tk.messagebox.showinfo("Error!", result)
                        return

                # confirmation message
                tk.messagebox.showinfo("Deleted", "Camp(s) deleted from database")

                # refresh the treeview
                self.refresh_treeview(tree)

                # clear entry boxes
                clear_entries()
    
        def update_camp():
            '''Treeview command: Updates records from entry box input'''

            # get selected camp ID
            selected = tree.focus()
            values = tree.item(selected, 'values')

            if values:
                selected_camp_id = values[0]
            else:
                tk.messagebox.showinfo("Error!", "Please select a camp to update!")
                return

            # get updated inputs
            name = camp_name_entry.get()
            location = location_entry.get()
            capacity = capacity_entry.get()
            if capacity:
                capacity = int(capacity)
            med = num_med_entry.get()
            if med:
                med = int(med)
            food = food_entry.get()
            if food:
                food = int(food)

            # update camp in camps and address table
            camp = Camps(name, selected_camp_id, location, capacity, med, food)
    
            if self.check_mandatory_fields(camp):        
                result = self.camps_controller.update_camp(camp)

                if result !=True:
                    # error message
                    tk.messagebox.showinfo("Error!", result)
                            
                # refresh the treeview
                self.refresh_treeview(tree)

                # clear entry boxes
                clear_entries()
        
        def add_camp():
            '''Treeview command: Adds records from entry box input'''
            # store selected record number
            selected = tree.focus()

            # get record values for ID
            values = tree.item(selected, 'values')

            # get values from entry boxes
            name = camp_name_entry.get()
            location = location_entry.get()
            capacity = capacity_entry.get()
            if capacity:
                capacity = int(capacity)
            med = num_med_entry.get()
            if med:
                med = int(med)
            food = food_entry.get()
            if food:
                food = int(food)

            camp = Camps(name, None, location, capacity, med, food)

            # add new camp
            if self.check_mandatory_fields(camp):
                result = self.camps_controller.save(camp)

                if result != True:
                    # error message
                    tk.messagebox.showinfo("Error!", result)

                else:
                    # Confirmation message
                    tk.messagebox.showinfo("Added", "Camp added to database")
            
                # clear entry boxes
                clear_entries()

                # refresh the treeview
                self.refresh_treeview(tree)

        # command buttons -------------------------------------------------------------------------------
        command_frame = ttk.LabelFrame(self.root, text="Commands", style="Treeview")
        command_frame.grid(row = 4, column = 1, sticky=NSEW, padx=10, pady=10)

        update_button = tk.Button(command_frame, text="Update Camp", command=update_camp)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(command_frame, text="Add Camp", command=add_camp)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        remove_multiple_button = tk.Button(command_frame, text="Remove Selected Camps", command=remove_selected)
        remove_multiple_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = tk.Button(command_frame, text="Move Record Up", command=move_up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = tk.Button(command_frame, text="Move Record Down", command=move_down)
        move_down_button.grid(row=0, column=5 , padx=10, pady=10)
 
        edit_button = tk.Button(command_frame, text="Clear", command=clear_entries)
        edit_button.grid(row=0, column=6, padx=10, pady=10)

        # return button --------------------------------------------------------------------------------
        return_button = tk.Button(text="Return", command=self.return_back)
        return_button.grid(column=1, row=5, padx=20, pady=10)

        # display tree  --------------------------------------------------------------------------------
        tree.bind("<ButtonRelease-1>", select_camp)
        tree.grid(row=2, column=1, sticky ='n')
