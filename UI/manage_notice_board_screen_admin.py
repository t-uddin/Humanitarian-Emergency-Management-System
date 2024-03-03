import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, END, NO, NSEW, W
import UI.dashboard_screen as dashboard

from Back_End.Users.VolunteerController import VolunteerController
from Back_End.Refugee_Profile.refugee_profile_controller import RefugeeProfileController
from Back_End.Camps.CampsController import CampsController
from Back_End.notice_board.notice import Notice
from Back_End.notice_board.notice_controller import NoticeBoardController

class NoticeAdminScreen:
    def __init__(self, root, connection, username, is_admin):
        self.root = root
        self.root.title('Refugee System | Admin Notice Board')
        self.connection = connection
        self.notice_controller = NoticeBoardController(connection)
        self.volunteer_controller = VolunteerController(connection)
        self.refugee_controller = RefugeeProfileController(connection)
        self.camps_controller = CampsController(connection)
        self.mapping = {"Normal" : 0 ,"Pinned: (⭐)" : 1, "Priority (❗)" : 2,"Important (❗❗)" : 3, \
                        "Urgent (URGENT ❗❗)" : 4}
        self.reverse_mapping = {0 : "Normal", 1 : "Pinned: (⭐)", 2 : "Priority (❗)", 3 : "Important (❗❗)", \
                                4 : "Urgent (URGENT ❗❗)"}

        self.username = username
        self.is_admin = is_admin
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def return_back(self):
        self.clear_window()
        dashboard.DashboardScreen(self.root, self.connection,self.username, self.is_admin).render()

    def populate_treeview(self, tree):
    # add data to the treeview from database
    #get camp associated with volunteer

        notice_list = self.notice_controller.initialise()

        for notice in notice_list:
            camp_id = notice.camp_id
            tree.insert('', index=tk.END, values=(notice.message_id, camp_id,
                                                  self.camps_controller.get_camp_name(camp_id),
                                                  self.reverse_mapping[notice.priority_rating], notice.message))

    def refresh_treeview(self, tree):
            tree.delete(*tree.get_children())
            self.populate_treeview(tree)

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
        columns = ('message_id', 'camp_id', 'camp_name', 'priority_rating', 'message')

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")
            
        # format columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("message_id", anchor=W, width=70, stretch=NO)
        tree.column("camp_id", anchor=W, width=70, stretch=NO)
        tree.column("camp_name", anchor=W, width=80, stretch=NO)
        tree.column("priority_rating", anchor=CENTER, width=110, stretch=NO)
        tree.column("message", anchor=W, width=930, stretch=NO)

        # define headings
        tree.heading('message_id', text='Message ID', anchor=W)
        tree.heading('camp_id', text='Camp ID', anchor=W)
        tree.heading('camp_name', text='Camp name', anchor=W)
        tree.heading('priority_rating', text='Priority rating', anchor=CENTER)
        tree.heading('message', text='Message')
 
        # add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=2, sticky='ns')

        # add data to the treeview from database
        self.populate_treeview(tree)
        
        ## Add record entry boxes ----------------------------------------------------------------------
        data_frame = ttk.LabelFrame(self.root, text="Notice Record", style="Treeview")
        data_frame.grid(row = 3, column = 1, sticky=NSEW, padx=10, pady=10)

        id_label = tk.Label(data_frame, text="Message ID").grid(row=0, column=0, padx=10, pady=10)
        message_id = tk.StringVar(data_frame, "")
        id_print = tk.Label(data_frame, textvariable=message_id).grid(row=0, column=1, padx=10, pady=10, sticky=W)

        message_label = tk.Label(data_frame, text="Message").grid(row=0, column=4, padx=10, pady=10)
        message_entry = tk.Entry(data_frame, width=55)
        message_entry.grid(row=0, column=5, padx=10, pady=10)

        #drop down box for selecting the priority
        OPTIONS = ["Normal" ,"Pinned: (⭐)","Priority (❗)", "Important (❗❗)", "Urgent (URGENT ❗❗)"] 

        priority_label = tk.Label(data_frame, text="Priority:").grid(row=0, column=6, padx=10, pady=10)
        priority_rating_entry = tk.StringVar(data_frame)
        priority_rating_entry.set("Normal") # default value

        rating_menu = tk.OptionMenu(data_frame, priority_rating_entry, *OPTIONS)
        rating_menu.grid(row=0, column=7, padx=10, pady=10)
        rating_menu.config(width=15)

        #drop down box for selecting camp ID

        camp_id_label = tk.Label(data_frame, text="Camp ID:").grid(row=0, column=2, padx=10, pady=10)

        camps_id_list = self.camps_controller.get_list_of_camp_ids()
        if camps_id_list == []:
            camps_id_list = ["No camps"]
        
        camp_id_entry = tk.StringVar(data_frame)
        camp_id_entry.set("Select Camp") # default value

        camp_menu = tk.OptionMenu(data_frame, camp_id_entry, *camps_id_list)
        camp_menu.grid(row=0, column=3, padx=10, pady=10)        

        
        ## configure the treeview functions ---------------------------------------------------------------
        def clear_entries():
            '''Treeview command: Clear entry boxes'''
            message_id.set("")
            camp_id_entry.set("Select Camp")
            message_entry.delete(0, END)
            priority_rating_entry.set("Normal")
        
        #keeps the entry boxes values, to allow the user to make modifications
        def retain_entries(camp_id):
            message_id.set("")
            camp_id_entry.set(camp_id)
            message_entry.delete(0, END)
            priority_rating_entry.set("Normal")            

        def select_message(e):
            '''Treeview function: Select records + print to entry boxes'''
            # clear entry boxes
            clear_entries()

            # store selected record number
            selected = tree.focus()

            # get record values
            values = tree.item(selected, 'values')

            #output to entry boxes
            message_id.set(values[0])
            camp_id_entry.set(values[1])
            message_entry.insert(0, values[4])
            priority_rating_entry.set(values[3])
       
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
            '''Treeview command: Remove many messages'''
            # Confirm delete from user
            response = tk.messagebox.askyesno("Caution!", "Are you sure you want to delete this message?")

            if response == 1:
                  # store selections
                selected = tree.selection()

                # loop over selected records and delete
                for message in selected:
                    values = tree.item(message, 'values')

                    message_id = values[0]
                    camp_id = values[1]
                    message = values[2]
                    priority_rating = values[3]

                    notice = Notice(message_id,camp_id,message,priority_rating)
                    self.notice_controller.delete_message(notice)

                # refresh the treeview
                self.refresh_treeview(tree)

                # confirmation message
                tk.messagebox.showinfo("Deleted", "Message(s) deleted from database")
    

        def update_notice():
            '''Treeview command: Updates records from entry box input'''

            # get message ID
            selected = tree.focus()
            values = tree.item(selected, 'values')
            
            selected_message_id = values[0]

            is_entry_valid = True

            # get updated inputs
            
            message = message_entry.get()
            camp_id = int(camp_id_entry.get())
            priority_rating = int(self.mapping[priority_rating_entry.get()])

            # update
            notice = Notice(selected_message_id,message,camp_id,priority_rating)
            try:
                self.notice_controller.update_message(notice)
            except Exception as e:
                print(f"The exception/error is: {e}")
                return False
                        
            # refresh the treeview
            self.refresh_treeview(tree)

            # clear entry boxes
            if is_entry_valid:
                clear_entries()
        
        def add_notice():
            '''Treeview command: Adds records from entry box input'''
            # store selected record number
            selected = tree.focus()

            # get record values for ID
            values = tree.item(selected, 'values')

            #output to entry boxes
            is_entry_valid = True
            num_of_camps = self.camps_controller.number_of_camps()

            #displays an error box if there are no camps in the database,
            #alternatively asks them to select a camp, if they have not chosen one
            if (camp_id_entry.get() == "Select Camp" or camp_id_entry.get() == "No camps")  and num_of_camps == 0:
                tk.messagebox.showinfo("Error!", "Create a camp before trying to select a camp ID")
                is_entry_valid = False
            elif camp_id_entry.get() == "Select Camp":
                tk.messagebox.showinfo("Error!", "Please select a camp")
                is_entry_valid = False

            if is_entry_valid:
                camp_id = int(camp_id_entry.get())
            else:
                camp_id = 0  
            
            entered_message = message_entry.get()

            if is_entry_valid:
                is_entry_valid = __is_message_valid(entered_message)

            #diplays an error message if a message is not enetered or the message is too long
            if entered_message == "":
                tk.messagebox.showinfo("Error!", "No message has been entered")
                is_entry_valid = False
            elif len(entered_message) > 120:
                tk.messagebox.showinfo("Error!", "The message you entered is too long, please limit to 120 characters")
                is_entry_valid = False

            message = message_entry.get()           

            priority_rating = int(self.mapping[priority_rating_entry.get()])            

            notice = Notice(None,message,camp_id,priority_rating)
            # add new notce
            if is_entry_valid:
                try:
                    self.notice_controller.save(notice)
                    # Confirmation message
                    tk.messagebox.showinfo("Added", "Message added to database")
                except Exception as e:
                    tk.messagebox.showinfo("Error!", f"The message was not added as: {e}")
                
            # clear entry boxes
            if is_entry_valid:
                clear_entries()

            # refresh the treeview
            self.refresh_treeview(tree)

        def __is_message_valid(entered_message):
                        #diplays an erros message if a message is not entered or the message is too long
            if entered_message == "":
                tk.messagebox.showinfo("Error!", "No message has been entered")
                return False
            elif len(entered_message) > 120:
                return False
            return True

        # command buttons -------------------------------------------------------------------------------
        command_frame = ttk.LabelFrame(self.root, text="Commands", style="Treeview")
        command_frame.grid(row = 4, column = 1, sticky=NSEW, padx=10, pady=10)

        update_button = tk.Button(command_frame, text="Update Notice", command=update_notice)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(command_frame, text="Add Notice", command=add_notice)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        remove_multiple_button = tk.Button(command_frame, text="Remove Selected Notices", command=remove_selected)
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
        tree.bind("<ButtonRelease-1>", select_message)
        tree.grid(row=2, column=1, sticky ='n')
