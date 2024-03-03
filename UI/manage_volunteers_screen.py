import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, END, NO, NSEW, W
import UI.dashboard_screen as dashboard
from Back_End.Camps.CampsController import CampsController
from Back_End.Users.VolunteerController import VolunteerController
from Back_End.Users.Volunteer import Volunteer
from Back_End.Refugee_Profile.refugee_profile_controller import RefugeeProfileController

class VolunteersScreen:
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.root.title('Refugee System | Volunteers')
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
        '''add data from database to the treeview'''
        volunteers_list = self.volunteer_controller.initialise()

        for volunteer in volunteers_list:
            tree.insert('', index=tk.END, values=(
                volunteer.username, volunteer.first_name, volunteer.last_name,volunteer.camp_id, \
                volunteer.availability, volunteer.phone_number, volunteer.address, volunteer.is_active))
    
    def refresh_treeview(self, tree):
        tree.delete(*tree.get_children())
        self.populate_treeview(tree)

    def check_mandatory_fields(self, first_name, last_name, phone, address, camp_id, availability):
        if not first_name or not last_name or not phone or not address or camp_id == "Select Camp" or not availability:
            tk.messagebox.showinfo(
                "Error!", "Make sure all fields are filled!")
            return False
        else:
            return True

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=10, rowspan=10) 

        label = tk.Label(text="Volunteers", justify="center")
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
        columns = ('username', 'volunteer_first_name', 'volunteer_last_name', 'camp',
                   'availability', 'phone', 'address', 'status')

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")

        # format columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("username", anchor=W, width=155, stretch=NO)
        tree.column("volunteer_first_name", anchor=W, width=155, stretch=NO)
        tree.column("volunteer_last_name", anchor=W, width=155, stretch=NO)
        tree.column("camp", anchor=CENTER, width=155, stretch=NO)    
        tree.column("availability", anchor=CENTER, width=155, stretch=NO)    
        tree.column("phone", anchor=CENTER, width=155, stretch=NO)  
        tree.column("address", anchor=CENTER, width=155, stretch=NO)    
        tree.column("status", anchor=CENTER, width=155, stretch=NO)    

        # define headings
        tree.heading('username', text='username', anchor=W)
        tree.heading('volunteer_first_name', text='First Name', anchor=W)
        tree.heading('volunteer_last_name', text='Last Name', anchor=W)
        tree.heading('username', text='Username')
        tree.heading('camp', text='Camp')
        tree.heading('availability', text='Availability')
        tree.heading('phone', text='Phone')
        tree.heading('address', text='Address')
        tree.heading('status', text='Status')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns')

        # add data to the treeview from database
        self.populate_treeview(tree)

        ## Add record entry boxes --------------------------------------------------------------------------
        data_frame = ttk.LabelFrame(self.root, text="Volunteer Record", style="Treeview")
        data_frame.grid(row = 3, column = 1, sticky=NSEW, padx=10, pady=10)

        def IntValidation(S):
            if S.isdigit():
                return True
            else:
                data_frame.bell()
                return False

        username_label = tk.Label(data_frame, text="Username").grid(row=0, column=0, padx=10, pady=10)
        username_var = tk.StringVar(data_frame, "")
        username_print = tk.Label(
            data_frame, textvariable=username_var).grid(row=0, column=1, padx=10, pady=10, sticky=W)

        first_name_label = tk.Label(data_frame, text="First Name").grid(row=0, column=2, padx=10, pady=10)
        first_name_entry = tk.Entry(data_frame)
        first_name_entry.grid(row=0, column=3, padx=10, pady=10)

        last_name_label = tk.Label(data_frame, text="Last Name").grid(row=0, column=4, padx=10, pady=10)
        last_name_entry = tk.Entry(data_frame)
        last_name_entry.grid(row=0, column=5, padx=10, pady=10)

        camp_label = tk.Label(data_frame, text="Camp").grid(row=0, column=6, padx=10, pady=10)

        OPTIONS = self.camps_controller.get_list_of_camp_ids()
        if OPTIONS == []:
            OPTIONS = ["No camps"]
        camp_entry = tk.StringVar(data_frame)
        camp_entry.set("Select Camp") # default value

        camp_menu = tk.OptionMenu(data_frame, camp_entry, *OPTIONS)
        camp_menu.grid(row=0, column=7, padx=10, pady=10)
        camp_menu.config(width=15)

        availability_label = tk.Label(
            data_frame, text="Availability e.g. TTTTTFF").grid(row=1, column=0, padx=10, pady=10)
        availability_entry = tk.Entry(data_frame)
        availability_entry.grid(row=1, column=1, padx=10, pady=10)

        vcmd = (data_frame.register(IntValidation), '%S')
        phone_label = tk.Label(data_frame, text="Phone").grid(row=1, column=2, padx=10, pady=10)
        phone_entry = tk.Entry(data_frame, validate='key', validatecommand=vcmd)
        phone_entry.grid(row=1, column=3, padx=10, pady=10)

        address_label = tk.Label(data_frame, text="Adress").grid(row=1, column=4, padx=10, pady=10)
        address_entry = tk.Entry(data_frame)
        address_entry.grid(row=1, column=5, padx=10, pady=10)
    
        ## configure the treeview functions --------------------------------------------------------------------------
        def clear_entries():
            '''Treeview command: Clear entry boxes'''
            username_var.set("")
            first_name_entry.delete(0, END)
            last_name_entry.delete(0, END)
            camp_entry.set("Select Camp") # default value
            availability_entry.delete(0, END)
            phone_entry.delete(0, END)
            address_entry.delete(0, END)

        def select_volunteer(e):
            '''Treeview function: Select records + print to entry boxes'''
            # clear entry boxes
            clear_entries()

            # store selected record number
            selected = tree.focus()

            # get record values
            values = tree.item(selected, 'values')
            username = values[0]

            #output to entry boxes
            username_var.set(username)
            first_name_entry.insert(0, values[1])
            last_name_entry.insert(0, values[2])
            camp_entry.set(values[3])
            availability_entry.insert(0, values[4])
            phone_entry.insert(0, values[5])
            address_entry.insert(0, values[6])

            return username

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
            '''Treeview command: Remove selected volunteers'''
            # check selections
            selected = tree.selection()
            
            if not selected:
                tk.messagebox.showinfo("Error!", "You have not selected any volunteers!")
                return
            
            # Confirm delete from user
            response = tk.messagebox.askyesno("Caution!", "Are you sure you want to delete these volunteers?")

            if response == 1:
                # loop over selected records and delete
                try:
                    for volunteer in selected:
                        values = tree.item(volunteer, 'values')

                        username = values[0]
                        password = None
                        is_admin = 0
                        first_name = values[1]
                        last_name = values[2]
                        is_active = 1
                        phone_number = values[5]
                        address = values[6]
                        camp = 0
                        availability  = values[4]
                        
                        volunteer = Volunteer(
                            username, password, is_admin, first_name, last_name,
                            is_active, phone_number, address, camp, availability)
                        
                        result =self.volunteer_controller.remove_volunteer(volunteer)

                        if result != True:
                            # error message
                            tk.messagebox.showinfo("Error!", result)
                            return

                    # refresh the treeview
                    self.refresh_treeview(tree)

                    # confirmation message
                    tk.messagebox.showinfo("Deleted", "Volunteer(s) deleted from database")

                except Exception as e:
                    print(f"The exception/error is: {e}")
                    return False
    
        def update_volunteer():
            '''Treeview command: Updates records from entry box input'''           
            # get selected user
            selected = tree.focus()
            
            if not selected:
                tk.messagebox.showinfo("Error!", "Please select a volunteer to update!")
                return

            values = tree.item(selected, 'values')
            username = values[0]
            is_active = values[7]
        
            # get updated inputs
            password = None
            is_admin = 0
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            phone_number = phone_entry.get()
            address = address_entry.get()
            camp = camp_entry.get()
            availability  = availability_entry.get()

            if self.check_mandatory_fields(first_name, last_name, phone_number, address, camp, availability) == False:
                return

            # create object
            volunteer = Volunteer(
                username, password, is_admin, first_name, last_name,
                is_active, phone_number, address, camp, availability)

            # update
            result = self.volunteer_controller.update_volunteer(volunteer)

            if result != True:
                # error message
                tk.messagebox.showinfo("Error!", result)
                return

            # clear entry boxes
            clear_entries()

            # refresh the treeview
            self.refresh_treeview(tree)
            return True

        def activate_deactivate_volunteer():
            '''Treeview command: Adds records from entry box input'''

            # get selected user
            selected = tree.focus()

            if not selected:
                tk.messagebox.showinfo("Error!", "You have not selected any volunteers!")
                return
            
            values = tree.item(selected, 'values')
            username = values[0]
            status = values[7]

            if status == "1":
                # deactivate volunteer
                result = self.volunteer_controller.deactivate(username)

                if result == True:
                    # error message
                    tk.messagebox.showinfo("Success!", "Volunteer deactivated")
            
            else:
                # activate volunteer
                result = self.volunteer_controller.activate(username)

                if result == True:
                    # error message
                    tk.messagebox.showinfo("Success!", "Volunteer activated")
                                    
            # clear entry boxes
            clear_entries()

            # refresh the treeview
            self.refresh_treeview(tree)

        # command buttons -------------------------------------------------------------------------------
        command_frame = ttk.LabelFrame(self.root, text="Commands", style="Treeview")
        command_frame.grid(row = 4, column = 1, sticky=NSEW, padx=10, pady=10)

        update_button = tk.Button(command_frame, text="Update Volunteer", command=update_volunteer)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        remove_multiple_button = tk.Button(command_frame, text="Remove Selected Volunteer(s)", command=remove_selected)
        remove_multiple_button.grid(row=0, column=1, padx=10, pady=10)

        move_up_button = tk.Button(command_frame, text="Move Record Up", command=move_up)
        move_up_button.grid(row=0, column=2, padx=10, pady=10)

        move_down_button = tk.Button(command_frame, text="Move Record Down", command=move_down)
        move_down_button.grid(row=0, column=3 , padx=10, pady=10)
 
        edit_button = tk.Button(command_frame, text="Clear", command=clear_entries)
        edit_button.grid(row=0, column=4, padx=10, pady=10)

        status_button = tk.Button(
            command_frame, text="Activate/Deactivate Volunteer", command=activate_deactivate_volunteer)
        status_button.grid(row=0, column=5, padx=10, pady=10)

        # return button --------------------------------------------------------------------------------
        return_button = tk.Button(text="Return", command=self.return_back)
        return_button.grid(column=1, row=5, padx=20, pady=10)

        # display tree  --------------------------------------------------------------------------------
        tree.bind("<ButtonRelease-1>", select_volunteer)
        tree.grid(row=2, column=1, sticky ='n')
