from Database.databaseSetup import databaseSetup
from pathlib import Path
from installation import start_package_installation, connect_to_db

start_package_installation()
import tkinter as tk
import UI.landing_screen as landing_screen

if __name__ == "__main__":
    
    path_to_db = 'RFG.db'
    path = Path(path_to_db)

    # If RFG.db file does not exist
    # Would recommend deleting RFG.db file and running again to ensure db is set up with the correct dummy data
    if not path.is_file():
        print("Database file not found")
        # Connect to db
        connection = connect_to_db()
        # Setup database
        dbSetUp = databaseSetup(connection)
        # Setup all tables
        dbSetUp.setup_table()
        # Add data
        dbSetUp.add_data()
    else:
        print("Database file found")
        # Connect to db
        connection = connect_to_db()

    # Render the first screen -----------------------------------------------------------
    root = tk.Tk()

    component = landing_screen.LandingScreen(root, connection)

    component.render()
    root.mainloop()