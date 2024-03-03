import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, END, NO, NSEW, W
import UI.dashboard_screen as dashboard
from Back_End.Camps.CampsController import CampsController
from Back_End.Refugee_Profile.refugee_profile_controller import RefugeeProfileController
from Back_End.Refugee_Profile.refugee_profile_class import RefugeeProfile
from Back_End.Users.VolunteerController import *


class RefugeesScreen:
    def __init__(self, root, connection, user_name, is_admin):
        self.root = root
        self.root.title('Refugee System | Refugees')
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
        '''add data to the treeview from database'''
        if self.is_admin == 1:
            refugee_list = self.refugee_controller.initialise()

            for refugee in refugee_list:           
                tree.insert('', index=tk.END, values=(
                    refugee.id, refugee.first_name, refugee.last_name,
                    refugee.camp_id, refugee.family_size, refugee.med_con))

        else:
            # get volunteer data
            self.volunteer_controller = VolunteerController(self.connection)
            volunteer = self.volunteer_controller.get_volunteer_details(self.user_name)
            self.camp = volunteer.camp_id

            refugee_list = self.refugee_controller.return_refugee_profiles_by_camp_id(self.camp)

            for refugee in refugee_list:           
                tree.insert('', index=tk.END, values=(
                    refugee.id, refugee.first_name, refugee.last_name, refugee.camp_id,
                    refugee.family_size, refugee.med_con))
                       
    def refresh_treeview(self, tree):
            tree.delete(*tree.get_children())
            self.populate_treeview(tree)

    def check_mandatory_fields(self, first_name, last_name, camp_id, family_size, med_con):
        if not first_name or not last_name or camp_id == "Select Camp" or \
                family_size == "Select Total Family Size" or med_con == "Select Medical Condition":
            tk.messagebox.showinfo(
                "Error!", "Make sure all fields are filled!")
            return False
        else:
            return True

    def render(self):
        canvas = tk.Canvas(self.root, width=800, height=500)
        canvas.grid(columnspan=10, rowspan=10) 

        label = tk.Label(text="Refugee Profiles", justify="center")
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
        columns = ('refugee_id', 'first_name', 'last_name', 'camp_id', 'family_size', 'medical')

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")

        # format columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("refugee_id", anchor=W, width=155, stretch=NO)
        tree.column("first_name", anchor=W, width=155, stretch=NO)
        tree.column("last_name", anchor=CENTER, width=155, stretch=NO) 
        tree.column("camp_id", anchor=CENTER, width=155, stretch=NO)    
        tree.column("family_size", anchor=CENTER, width=155, stretch=NO)    
        tree.column("medical", anchor=CENTER, width=155, stretch=NO)    

        # define headings
        tree.heading('refugee_id', text='ID', anchor=W)
        tree.heading('first_name', text='First Name', anchor=W)
        tree.heading('last_name', text='Last Name')
        tree.heading('camp_id', text='Camp ID')
        tree.heading('family_size', text='Family Size')
        tree.heading('medical', text='Medical Conditions')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns')

        # add data to the treeview from database
        self.populate_treeview(tree)

        ## Add record entry boxes --------------------------------------------------------------------------
        data_frame = ttk.LabelFrame(self.root, text="Refugee Record", style="Treeview")
        data_frame.grid(row = 3, column = 1, sticky=NSEW, padx=10, pady=10)

        id_label = tk.Label(data_frame, text="Refugee ID").grid(row=0, column=0, padx=10, pady=10)
        id_value = tk.StringVar(data_frame, "")
        id_print = tk.Label(data_frame, textvariable=id_value).grid(row=0, column=1, padx=10, pady=10, sticky=W)

        first_name_label = tk.Label(data_frame, text="First Name").grid(row=0, column=2, padx=10, pady=10)
        first_name_entry = tk.Entry(data_frame)
        first_name_entry.grid(row=0, column=3, padx=10, pady=10)

        last_name_label = tk.Label(data_frame, text="Last Name").grid(row=0, column=4, padx=10, pady=10)
        last_name_entry = tk.Entry(data_frame)
        last_name_entry.grid(row=0, column=5, padx=10, pady=10)
    
        OPTIONS = self.camps_controller.get_list_of_camp_ids()
        if OPTIONS == []:
            OPTIONS = ["No camps"]

        camp_entry = tk.StringVar(data_frame)
        camp_entry.set("Select Camp") # default value

        camp_label = tk.Label(data_frame, text="Camp").grid(row=0, column=6, padx=10, pady=10)
        camp_menu = tk.OptionMenu(data_frame, camp_entry, *OPTIONS)
        camp_menu.grid(row=0, column=7, padx=10, pady=10)
        camp_menu.config(width=15)

        OPTIONS3 = [1,2,3,4,5,6,7,8,9,10]
        
        family_size_entry = tk.StringVar(data_frame)
        family_size_entry.set("Select Total Family Size") 
        family_size_label = tk.Label(data_frame, text="Family Size").grid(row=1, column=0, padx=10, pady=10)
        family_size_menu = tk.OptionMenu(data_frame,family_size_entry, *OPTIONS3) # new 
        family_size_menu.grid(row=1, column=1, padx=10, pady=10)
        family_size_menu.config(width=15)

        OPTIONS2 = ["None","Medical","Surgical","Psychiatric","Multiple"]

        medical_entry = tk.StringVar(data_frame)
        medical_entry.set("Select Medical Condition") 
        medical_label = tk.Label(data_frame, text="Medical condition").grid(row=1, column=2, padx=10, pady=10)
        medical_menu = tk.OptionMenu(data_frame,medical_entry, *OPTIONS2) # new 
        medical_menu.grid(row=1, column=3, padx=10, pady=10)
        medical_menu.config(width=15)

        ## configure the treeview functions --------------------------------------------------------------------------
        def clear_entries():
            '''Treeview command: Clear entry boxes'''
            id_value.set("")
            first_name_entry.delete(0, END)
            last_name_entry.delete(0, END)
            camp_entry.set("Select Camp") # default value
            family_size_entry.set("Select Family Size")
            medical_entry.set("Select Medical Condition")
        
        def select_refugee(e):
            '''Treeview function: Select records + print to entry boxes'''
            # clear entry boxes
            clear_entries()

            # store selected record number
            selected = tree.focus()

            # get record values
            values = tree.item(selected, 'values')

            #output to entry boxes
            id_value.set(values[0])
            first_name_entry.insert(0, values[1])
            last_name_entry.insert(0, values[2])
            camp_entry.set(values[3])
            family_size_entry.set(values[4])
            medical_entry.set(values[5])

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
            '''Treeview command: Remove selected refugees'''
            # check selections
            selected = tree.selection()
            
            if not selected:
                tk.messagebox.showinfo("Error!", "You have not selected any refugees!")
                return

            # Confirm delete from user
            response = tk.messagebox.askyesno("Caution!", "Are you sure you want to remove these Refugees?")

            if response == 1:
                # loop over selected records and delete
                for refugee in selected:
                    values = tree.item(refugee, 'values')

                    refugee_id = values[0]
                    
                    result = self.refugee_controller.delete_refugee_profile_from_database(refugee_id)
                    self.refugee_controller.delete_refugee_profile_from_database(refugee_id)

                    # If any of the deletions failed, notify admin
                    if result != True:
                        # error message
                        tk.messagebox.showinfo("Error!", result)
                        self.refresh_treeview(tree)
                        return

                # confirmation message
                tk.messagebox.showinfo("Deleted!", "Refugee(s) deleted from database")

                # refresh the treeview
                self.refresh_treeview(tree)

        def update_refugee():
            '''Treeview command: Updates records from entry box input'''
            # get refugee ID
            selected = tree.focus()
            values = tree.item(selected, 'values')

            if values:
                refugee_id = str(values[0])
            else:
                tk.messagebox.showinfo("Error!", "Please select a refugee to update!")
                return

            # get updated inputs
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            camp = camp_entry.get()
            if camp != "None":
                camp = int(camp)
            family_size = int(family_size_entry.get())
            medical = medical_entry.get()

            if self.check_mandatory_fields(first_name, last_name, camp, family_size, medical) == False:
                return

            # update object
            refugee = RefugeeProfile(refugee_id, first_name, last_name, camp, family_size, medical)
            result = self.refugee_controller.update_refugee_profile(refugee)
            self.refugee_controller.update_refugee_profile(refugee)

            if result != True:
                # error message
                    tk.messagebox.showinfo("Error!", result)
                    self.refresh_treeview(tree)

            # update tree
            self.refresh_treeview(tree)

            # clear entry boxes
            clear_entries()

        def add_refugee():
            '''Treeview command: Adds records from entry box input'''
            # get updated inputs
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            if camp_entry.get() == "None":
                camp = None
            else:
                camp = int(camp_entry.get())
            family_size = int(family_size_entry.get())
            medical = medical_entry.get()

            if self.check_mandatory_fields(first_name, last_name, camp, family_size, medical) == False:
                return

            # add object
            refugee = RefugeeProfile(None, first_name, last_name, camp, family_size, medical)
            result = self.refugee_controller.save(refugee)

            # Confirmation/error message
            if result !=True:
                tk.messagebox.showinfo("Error!", {result})
            else:
                tk.messagebox.showinfo("Added!", "Refugee added to database")

            # refresh the treeview
            self.refresh_treeview(tree)

             # clear entry boxes
            clear_entries()

        def remove_from_camp():
            # get refugee ID
            selected = tree.focus()
            
            if not selected:
                tk.messagebox.showinfo("Error!", "You have not selected any refugees!")
                return

            values = tree.item(selected, 'values')
            refugee_id = str(values[0])

            # get camp ID
            camp = camp_entry.get()

            if camp == "None":
                tk.messagebox.showinfo("Error!", "This refugee is not assigned to a camp")
                return
            
            camp = int(camp)

            # unassign the camp
            self.refugee_controller.remove_refugee_profile_from_camp(refugee_id, camp)

            # refresh the treeview
            self.refresh_treeview(tree)

            # clear entry boxes
            clear_entries()

            # Confirmation message
            tk.messagebox.showinfo("Added!", "Refugee removed from this camp")

        # command buttons -------------------------------------------------------------------------------
        
        command_frame = ttk.LabelFrame(self.root, text="Commands", style="Treeview")
        command_frame.grid(row = 4, column = 1, sticky=NSEW, padx=10, pady=10)

        update_button = tk.Button(command_frame, text="Update Refugee Profile", command=update_refugee)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(command_frame, text="Add Refugee", command=add_refugee)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        remove_refugee_button = tk.Button(command_frame, text="Remove Refugee From Camp", command=remove_from_camp)
        remove_refugee_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = tk.Button(command_frame, text="Move Record Up", command=move_up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = tk.Button(command_frame, text="Move Record Down", command=move_down)
        move_down_button.grid(row=0, column=5, padx=10, pady=10)
 
        edit_button = tk.Button(command_frame, text="Clear", command=clear_entries)
        edit_button.grid(row=0, column=6, padx=10, pady=10)

        if self.is_admin == 1:
            remove_button = tk.Button(command_frame, text="Remove Selected Refugee(s)", command=remove_selected)
            remove_button.grid(row=0, column=7, padx=10, pady=10)

        # return button --------------------------------------------------------------------------------
        return_button = tk.Button(text="Return", command=self.return_back)
        return_button.grid(column=1, row=5, padx=20, pady=10)

        # display tree  --------------------------------------------------------------------------------
        tree.bind("<ButtonRelease-1>", select_refugee)
        tree.grid(row=2, column=1, sticky ='n')
