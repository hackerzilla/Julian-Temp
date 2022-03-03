"""
VSS
Author: Sam Gebhardt/Jaegar J/Nick Johnstone/JD Paul
Date:   02/16/2022
Last Edit: 02/16/   Sam Gebhardt    Created File
"""
import sys
from os import path
from ScrumbanInterface import ScrumbanInterface, GetInitializingInfo
from ScrumbanHistory import ScrumbanHistory
from ScrumbanBoard import Board


class VSS():

    """
    Class that contains the data used throughout the program.

    Used By:
        VSS.py
        ScrumbanInterface.py

    Members:
        Member Name:            : Type              : Default Val   -> Description
        ------------------------------------------------------------------------------------------------------------------------------------------
        self.todo_limit         : int               : 0             -> The max number of tasks that can be in the todo backlog

        self.member_task_limit  : int               : 0             -> The max number of tasks that can be assigned to a member

        self.interface          : ScrumbanInterface : -             -> A singleton instance of ScrumbanInterface

        self.history            : ScrumbanHistory   : -             -> A singleton instance of ScrumbanHistory

        self.board              : ScrumbanBoard     : -             -> A singleton instance of ScrumbanBoard

    Methods:

        Public:                                                                      Return:
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    startup(self)                                               |   ->  None
                                                                                    |
        Usage:          instance.startup()                                          |
                                                                                    |
        Description:    Start the system by loading files into the program,         |
                        creating the singleton ScrumbanBoard instance and           |
                        starting the event loop for the user interface              |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_limits(self, member_task_limit, todo_limit)             |   ->  None
                                                                                    |
        Usage:          instance.set_limits(self, 4, 4)                             |
                                                                                    |
        Description:    Set the max number of tasks in the todo backlog and the     |
                        max number of tasks a member can be working on              |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    send_reports(self)                                          |   ->  None
                                                                                    |
        Usage:          instance.set_reports(self)                                  |
                                                                                    |
        Description:    Send emails to all the team members that summarizes the     |
                        meeting                                                     |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    shutdown(self)                                              |   ->  None
                                                                                    |
        Usage:          instance.shutdown(self)                                     |
                                                                                    |
        Description:    Shutdown the system by saving the information stored in     |
                        self.board, send emails to team members and close the UI    |
    """

    def __init__(self):

        # the max number of tasks in the todo backlog
        self.todo_limit = 0
        # the max number of tasks per member
        self.member_task_limit = 0

        # The ScrumbanInterface singleton instance for the program
        self.interface = ScrumbanInterface(self)

        # The ScrumbanHistory singleton instance for the program
        self.history = ScrumbanHistory()

        # The ScrumbanBoard singleton instance for the program
        self.board = Board([],[],[],[],[])

    def startup(self) -> None:
        """
        Parameter:      N/A

        Called By:      __main__ - VSS.py

        Calls:          check_history(), reset_system(), check_valid_task_file()
                        set_project_backlog_path(), check_valid_member_file(),
                        set_members_path(), load_scrumban(), get_project_backlog(),
                        get_todo_backlog(), get_member_list(), get_completed_tasks(),
                        get_agenda(), read_system_data() - ScrumbanHistory.py

                        get_project_backlog_input(), set_message_box(),
                        get_members_input(), set_board_data(), mainloop()
                        - ScrumbanInterface.py

                        __init__ - ScrumbanBoard

        Modifies:       self.history, self.board, self.interface

        Return:         None

        Description:    Start the system by loading files into the program,
                        creating the singleton ScrumbanBoard instance and
                        starting the event loop for the user interface
        """
        # intial_boot: A bool to determine if the system has been ran before
        initial_boot = self.history.check_history()

        # if the program is being booted for the first time
        if not initial_boot:
            print("INITIAL")
            # valid_project_backlog: bool value to loop over tell the user gives a valid file path
            valid_project_backlog = False

            # while the user hasn't given a valid file
            while not valid_project_backlog:

                # project_backlog_path: the path for the project backlog
                project_backlog_path = self.interface.get_project_backlog_input()

                # If the user clicks enter without selecting a file it returns
                # "" or (), check to make sure this didn't happen. Exit if it did
                if project_backlog_path == "" or isinstance(project_backlog_path, tuple):
                    self.history.reset_system()
                    sys.exit()

                # check if file is a directory (invalid)
                if path.isdir(project_backlog_path):
                    # Display error message to the user
                    self.interface.set_message_box("File Error", "Error! File is a directory")
                    # reprompt the user
                    continue

                # project_backlog_file: a file object for the given path
                # Try to open the file
                # Except if the file doesn't exist, then warn the user
                try:
                    project_backlog_file = open(project_backlog_path, "r")
                    project_backlog_file.close()
                except FileNotFoundError:
                    # Display error to the user
                    self.interface.set_message_box("File Error", "Invalid file path for project backlog")
                    continue # try again

                # valid: A string that determines if the file is in the correct format
                valid = self.history.check_valid_task_file(project_backlog_path)

                # If the file isn't valid
                if valid != "VALID":
                    # Display error to the user
                    self.interface.set_message_box("File Error", valid)
                    continue # try again

                # Set the project backlog path within the ScrumbanHistory method
                self.history.set_project_backlog_path(project_backlog_path)

                # Update to break the loop
                valid_project_backlog = True

            # reset bool for members file
            valid_memeber_file = False

            # while the user hasn't given a valid file
            while not valid_memeber_file:

                # mebers_path: The path for user inputted the members file
                members_path = self.interface.get_members_input()

                # If the user clicks enter without selecting a file it returns
                # "" or (), check to make sure this didn't happen. Exit if it did
                if members_path == "" or isinstance(members_path, tuple):
                    self.history.reset_system()
                    sys.exit()

                # make sure path isn't a dir
                if path.isdir(members_path):
                    # Display error message to the user
                    self.interface.set_message_box("File Error", "Error! File is a directory")
                    # reprompt the user

                # project_backlog_file: a file object for the given path
                # Try to open the file
                # Except if the file doesn't exist, then warn the user
                try:
                    members_file = open(members_path, "r")
                    members_file.close()
                except FileNotFoundError:
                    # Display error to the user
                    self.interface.set_message_box("File Error", "Invalid file path for members file")
                    continue # try again

                # valid: A string that determines if the file is in the correct format
                valid = self.history.check_valid_member_file(members_path)

                # if the file isn't valid
                if valid != "VALID":
                    # call method to display error message
                    self.interface.set_message_box("File Error", valid)
                    continue # try again

                # Set path to members in the ScrumbanHistory instance
                self.history.set_members_path(members_path)

                # change the bool to exit the loop
                valid_memeber_file = True

            # Load the user files given from the user
            self.history.load_scrumban()

            # input_window: A GetInitializingInfo instance to setup the display window for the program
            input_window = GetInitializingInfo(self)

            # Start the event loop for the system
            input_window.mainloop()

            # Populate the board with the data collected from the user
            self.board = Board(self.history.get_project_backlog(), self.history.get_todo_backlog(),
                               self.history.get_member_list(), self.history.get_completed_tasks(),
                               self.history.get_agenda(), self.member_task_limit, self.todo_limit)

        # if the program is not being booted for the first time
        else:
            print("SUBSEQUENT")

            # Read the saved system data
            self.history.read_system_data()

            # Try to load the saved data from the file system
            # Except If the files don't exist
            try:
                self.history.load_scrumban()
            except:
                # Display a message to the user that the files no longer exist
                file_not_found_message = "Files Were Moved! Please Move Files Back To Original Locations:"

                # backlog_path: The invalid path of the project backlog
                # mem_path: The invalid path of the members
                backlog_path = f"Project Backlog: {self.history.get_project_backlog_path()}"
                mem_path = f"Members File: {self.history.get_members_path()}"

                # Display error to the user
                self.interface.set_message_box("File Error", f"{file_not_found_message}\n\n\
                                                {backlog_path}\n\n{mem_path}")
                # exit the system
                sys.exit()

            # Populate the board with the data collected from the user
            self.board = Board(self.history.get_project_backlog(), self.history.get_todo_backlog(),
                            self.history.get_member_list(), self.history.get_completed_tasks(),
                            self.history.get_agenda(), self.history.get_work_in_progress_limit(),
                            self.history.get_todo_limit())

        # Setsup the interface based on the data in the ScrumbanBoard class
        self.interface.set_board_data(self.board)

        # Start the user interface eventloop
        self.interface.mainloop()

    def set_limits(self, member_task_limit:int, todo_limit:int) -> None:
        """
        Parameter:      member_limit: The max number of tasks a member can be working on
                        todo_limit: The max number of tasks that can be in the todo backlog

        Called By:      GetInitializingInfo.__init__() - VSS.py

        Calls:          None

        Modifies:       self.member_limit, self.todo_limit

        Return:         None

        Description:    Updates the member limit and and todo limit
        """
        self.member_task_limit = member_task_limit
        self.todo_limit = todo_limit

    def send_reports(self) -> None:
        """
        Parameter:      None

        Called By:      _send_reports_button_clicked - ScrumbanInterface.py

        Calls:          set_project_backlog(), set_todo_backlog(), set_members()
                        set_completed_tasks(), set_general_notes(), save_system_data(),
                        save_scrumban(), send_emails() - ScrumbanHistory.py

                        set_message_box() - ScrumbanInterface.py

        Modifies:       self.history

        Return:         None

        Description:    Sends the members emails with a summary of the meeting data
        """
        # call all of the setters for history

        # Set the data for the project backlog from the ScrumbanBoard instance
        self.history.set_project_backlog(self.board.get_string_project_backlog())

        # Set the data for the todo backlog from the ScrumbanBoard instance
        self.history.set_todo_backlog(self.board.get_string_todo())

        # Set the data for the members from the ScrumbanBoard instance
        self.history.set_members(self.board.get_string_members())

        # Set the data for the completed backlog from ScrumbanBoard instance
        self.history.set_completed_tasks(self.board.get_string_completed())

        # Set the data for the genral notes from ScrumbanBoard instance
        self.history.set_general_notes(self.board.get_notes())

        # Save the data that the user can't see, ie system information
        self.history.save_system_data(self.board.get_task_member_limit(),
                                      self.board.get_max_todo_size())

        # Save the data from the above setters for the next time the system is ran
        self.history.save_scrumban()

        # Try: Attempt to send the emails to each member and create a popup message that
        # informs the user of successfuly sending the emails
        # Except: There was an error in sending the emails, inform the user
        try:
            self.history.send_emails()
            self.interface.set_message_box("Alert", "Reports Sent!")
        except:
            self.interface.set_message_box("Error", "Error Sending Reports!")

    def shutdown(self) -> None:
        """
        Parameter:      None

        Called By:      __main__ - VSS.py

        Calls:          set_project_backlog(), set_todo_backlog(), set_members()
                        set_completed_tasks(), set_general_notes(), save_system_data(),
                        save_scrumban() - ScrumbanHistory.py

        Modifies:       self.history

        Return:         None

        Description:    Shutsdown the system. Saves the state of the data in board
        """

        # call all of the setters for history
        # Set the data for the project backlog from the ScrumbanBoard instance
        self.history.set_project_backlog(self.board.get_string_project_backlog())

        # Set the data for the todo backlog from the ScrumbanBoard instance
        self.history.set_todo_backlog(self.board.get_string_todo())

        # Set the data for the members from the ScrumbanBoard instance
        self.history.set_members(self.board.get_string_members())

        # Set the data for the completed backlog from ScrumbanBoard instance
        self.history.set_completed_tasks(self.board.get_string_completed())

        # Set the data for the genral notes from ScrumbanBoard instance
        self.history.set_general_notes(self.board.get_notes())

        # Save the data that the user can't see, ie system information
        self.history.save_system_data(self.board.get_task_member_limit(),
                                      self.board.get_max_todo_size())
        # Save the data from the above setters for the next time the system is ran
        self.history.save_scrumban()


if __name__ == "__main__":
    # system: Instance of VSS
    system = VSS()
    system.startup()
    system.shutdown()
