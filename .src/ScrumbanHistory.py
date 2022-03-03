"""
File: ScrumbanHistory.py

Description: This module is responsible for maintaining long term storage for the
             Virtual Scrumban System.

             It completed several tasks:

             1. Saves longerm data
             2. Loads longerm data
             3. Validates file
             4. Distributes email reports


Dependencies: None

Author(s): Nick Johnstone

Date Created: 2/16/2022

Dates Modified: 2/17/2022, 2/18/2022, 2/19/2022, 2/20/2022, 2/212022, 2/22/2022,
2/23/2022
"""

# used to send the email reports
import smtplib
# used to check file system information
from os import listdir, getcwd, mkdir, path
# used to mark files tasks with timestamps
from datetime import date
# used to valid user files
from re import search
# used to clear system data
from shutil import rmtree
# used to build the email messages
from email.message import EmailMessage
# used to check network connection
import urllib.request
# used to check network connection
import urllib.error


class ScrumbanHistory():
    """
    Encapsulate task data for the ScrumbanBoard module.

    Used By:
        VSS.py

    Members:
        Member Name:                : Type              : Default Val           -> Description
        ------------------------------------------------------------------------------------------------------------------------------------------
        self.project_backlog_path   : str               : ""                    -> Holds the absolute path of the project backlog file

        self.members_path           : str               : ""                    -> Holds the absolute path of the members file

        self.todo_backlog_path      : str               : "todo_backlog.txt"    -> Holds the absolute path of the todo_backlog file

        self.completed_tasks_path   : str               : "completed_tasks.csv" -> Holds the absolute path of the completed_tasks file

        self.agenda_path            : str               : ""                    -> Holds the agenda_path of the current agenda file

        self.project_backlog        : list[list[str]]   : []                    -> Holds the list of raw string tasks on the project backlog

        self.todo_backlog           : list[list[str]]   : []                    -> Holds the list of raw string tasks on the todo backlog

        self.members                : list[list[str]]   : []                    -> Holds the list of raw string member data

        self.completed_tasks        : list[list[str]]   : []                    -> Holds the list of raw string tasks that have been completed

        self.agenda                 : list[str]         : []                    -> Holds the list of agenda items for the current session

        self.work_in_progress_limit : int               : 4                     -> The maximum amount of tasks a member can have a one time

        self.todo_limit             : int               : 14                    -> The maximum amount of tasks that can be on the todo backlog at a time

        self.general_notes          : str               : ""                    -> Holds the general meeting notes


    Methods:

        Private:                                                                     Return:
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    _load_project_backlog(self)                                 |   -> None
                                                                                    |
        Usage:          instance._load_project_backlog(self)                        |
                                                                                    |
        Description:    Reads in data from self.project_backlog_path and assigns    |
                        it to self.project_backlog                                  |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    _load_members(self)                                         |   -> None
                                                                                    |
        Usage:          instance._load_members(self)                                |
                                                                                    |
        Description:    Reads in data from self.members_path and assigns            |
                        it to self.members                                          |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    _load_todo_backlog(self)                                    |   -> None
                                                                                    |
        Usage:          instance._load_todo_backlog(self)                           |
                                                                                    |
        Description:    Reads in data from self.todo_backlog_path and assigns       |
                        it to self.todo_backlog                                     |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    _load_completed_tasks(self)                                 |   -> None
                                                                                    |
        Usage:          instance._load_completed_tasks(self)                        |
                                                                                    |
        Description:    Reads in data from self.completed_tasks_path and assigns    |
                        it to self.completed_tasks                                  |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    _save_project_backlog(self)                                 |   -> None
                                                                                    |
        Usage:          instance._save_project_backlog(self)                        |
                                                                                    |
        Description:    Saves data from self.completed_tasks by                     |
                        writing it to self.completed_tasks_path                     |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    _save_members(self)                                         |   -> None
                                                                                    |
        Usage:          instance._save_members(self)                                |
                                                                                    |
        Description:    Saves data from self.members by                             |
                        writing it to self.members_path                             |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    _save_todo_backlog(self)                                    |   -> None
                                                                                    |
        Usage:          instance._save_members(self)                                |
                                                                                    |
        Description:    Saves data from self.members by                             |
                        writing it to self.members_path                             |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    _save_completed_tasks(self)                                 |   -> None
                                                                                    |
        Usage:          instance._save_completed_tasks(self)                        |
                                                                                    |
        Description:    Saves data from self.completed_tasks by                     |
                        writing it to self.completed_tasks_path                     |
        ----------------------------------------------------------------------------|-------------------------------------------------


        Public:                                                                      Return:
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    check_history(self)                                         |   -> True if data is found
                                                                                    |      False if no data found
        Usage:          instance.check_history()                                    |
                                                                                    |
        Description:    Checks if there is system data already stored.              |
                        If True, return True                                        |
                        If False, return False and create system data directory     |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    reset_system(self)                                          |   -> None
                                                                                    |
        Usage:          instance.reset_system()                                     |
                                                                                    |
        Description:    Resets the system data by deleting                          |
                        the system data directory                                   |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    check_valid_task_file(self, file_path: str)                 |   -> True if valid format
                                                                                    |      False if invalid format
        Usage:          instance.check_valid_task_file(str)                         |
                                                                                    |
        Description:    Static method that validates task files using regex         |
                        Opens the file whose path is stored in file_path and        |
                        validates it                                                |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_project_backlog_path(self, path: str)                   |   -> None
                                                                                    |
        Usage:          instance.set_project_backlog_path(str)                      |
                                                                                    |
        Description:    sets the class attribute project_backlog_path to be path    |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    check_valid_member_file(file_path: str)                     |   -> True if valid format
                                                                                    |      False if invalid format
        Usage:          instance.check_valid_member_file(str)                       |
                                                                                    |
        Description:    Static method that validates member file using regex        |
                        Opens the file whose path is stored in file_path and        |
                        validates it                                                |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_members_path(self, path: str)                           |   -> None
                                                                                    |
        Usage:          instance.set_members_path(str)                              |
                                                                                    |
        Description:    sets the class attribute members_path to be path            |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    save_system_data(self, work_in_progress_limit, todo_limit)  |   -> None
                                                                                    |
        Usage:          instance.save_system_data(int, int)                         |
                                                                                    |
        Description:    saves the system data into .sys_data/sys_data               |
                        Attributes that are saved:                                  |
                        self.work_in_progress_limit                                 |
                        self.todo_limit                                             |
                        self.project_backlog_path                                   |
                        self.members_path                                           |
                        self.todo_backlog_path                                      |
                        self.completed_tasks_path                                   |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    read_system_data(self)                                      |   -> None
                                                                                    |
        Usage:          instance.read_system_data()                                 |
                                                                                    |
        Description:    reads the system data from .sys_data/sys_data               |
                        Attributes that are set:                                    |
                        self.work_in_progress_limit                                 |
                        self.todo_limit                                             |
                        self.project_backlog_path                                   |
                        self.members_path                                           |
                        self.todo_backlog_path                                      |
                        self.completed_tasks_path                                   |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    load_agenda(self)                                           |   -> None
                                                                                    |
        Usage:          instance.load_agenda()                                      |
                                                                                    |
        Description:    Reads in data from self.agenda_path and assigns             |
                        it to self.agenda                                           |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    load_scrumban(self)                                         |   -> None
                                                                                    |
        Usage:          instance.load_scrumban()                                    |
                                                                                    |
        Description:    Reads the data from:                                        |
                        Attributes that are set:                                    |
                        self.project_backlog_path                                   |
                        self.members_path                                           |
                        self.todo_backlog_path                                      |
                        self.completed_tasks_path                                   |
                        self.agenda_path                                            |
                                                                                    |
                        Sets the following attributes with the read in data:        |
                        self.project_backlog                                        |
                        self.members                                                |
                        self.todo_backlog                                           |
                        self.completed_tasks                                        |
                        self.agenda                                                 |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_work_in_progress_limit(self)                            |   -> int that represents the
                                                                                    |      work in progress limit
        Usage:          instance.get_work_in_progress_limit()                       |
                                                                                    |
        Description:    returns the work_in_progress_limit attribute                |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_todo_limit(self)                                        |   -> int that represents the
                                                                                    |      todo limit
        Usage:          instance.get_todo_limit()                                   |
                                                                                    |
        Description:    returns the todo attribute                                  |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_project_backlog(self)                                   |   -> list of lists of strings that
                                                                                    |      represent tasks on the project backlog
        Usage:          instance.get_project_backlog()                              |
                                                                                    |
        Description:    returns the project_backlog attribute                       |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_member_list(self)                                       |   -> list of lists of strings that
                                                                                    |      represent team members
        Usage:          instance.get_member_list()                                  |
                                                                                    |
        Description:    returns the members attribute                               |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_todo_backlog(self)                                      |   -> list of lists of strings that
                                                                                    |      represent tasks in the todo backlog
        Usage:          instance.get_todo_backlog()                                 |
                                                                                    |
        Description:    returns the todo_backlog attribute                          |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_completed_list(self)                                    |   -> list of lists of strings that
                                                                                    |      represent tasks in the completed tasks log
        Usage:          instance.get_completed_list()                               |
                                                                                    |
        Description:    returns the completed_list attribute                        |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_agenda(self)                                            |   -> list strings that represents
                                                                                    |      the meeting agenda
        Usage:          instance.get_agenda()                                       |
                                                                                    |
        Description:    returns the agenda attribute                                |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_project_backlog_path(self)                              |   -> stirng that represents the project backlog path
                                                                                    |
        Usage:          instance.get_project_backlog_path()                         |
                                                                                    |
        Description:    returns the project_backlog_path attribute                  |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_members_path(self)                                      |   -> stirng that represents the members path
                                                                                    |
        Usage:          instance.get_members_path()                                 |
                                                                                    |
        Description:    returns the members_path attribute                          |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_project_backlog(self, project_backlog:list)             |   -> None
                                                                                    |
        Usage:          instance.set_project_backlog(list)                          |
                                                                                    |
        Description:    sets the project_backlog attribute to project_backlog       |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_members(self, members:list)                             |   -> None
                                                                                    |
        Usage:          instance.set_members(list)                                  |
                                                                                    |
        Description:    sets the members attribute to members                       |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_todo_backlog(self, todo_backlog:list)                   |   -> None
                                                                                    |
        Usage:          instance.set_todo_backlog(list)                             |
                                                                                    |
        Description:    sets the todo_backlog attribute to todo_backlog             |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_completed_tasks(self, completed_tasks:list)             |   -> None
                                                                                    |
        Usage:          instance.set_completed_tasks(list)                          |
                                                                                    |
        Description:    sets the completed_tasks attribute to completed_tasks       |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_general_notes(self, general_notes:str)                  |   -> None
                                                                                    |
        Usage:          instance.set_general_notes(list)                            |
                                                                                    |
        Description:    sets the general_notes attribute to general_notes           |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    load_scrumban(self)                                         |   -> None
                                                                                    |
        Usage:          instance.load_scrumban()                                    |
                                                                                    |
        Description:    Saves the data from:                                        |
                        Files that are written to:                                  |
                        self.project_backlog_path                                   |
                        self.members_path                                           |
                        self.todo_backlog_path                                      |
                        self.completed_tasks_path                                   |
                                                                                    |
                        Uses the following attributes to write the data to files    |
                        self.project_backlog                                        |
                        self.members                                                |
                        self.todo_backlog                                           |
                        self.completed_tasks                                        |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    send_emails(self)                                           |   -> None
                                                                                    |
        Usage:          instance.send_emails()                                      |
                                                                                    |
        Description:    Sends emails to each team member                            |
        ----------------------------------------------------------------------------|-------------------------------------------------
    """

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def __init__(self, project_backlog_path:str = "", members_path:str = "",
            todo_backlog_path:str = "todo_backlog.txt",
            completed_tasks_path:str = "completed_tasks.csv", agenda_path:str = "",
            project_backlog = [], todo_backlog = [], members = [],
            completed_tasks = [], agenda = [], work_in_progress_limit:int = 4,
            todo_limit:int = 14, general_notes = ""):
        """

        NOTE: ALL PARAMETERS HAVE DEFAULT VALUES AND WILL BE POPULATED WITH SETTERS

        Parameter:      project_backlog_path - absolute path of the project_backlog file
                        members_path - absolute path of the members file
                        todo_backlog_path - path of the todo_backlog file
                        completed_tasks_path - path of the completed_tasks file
                        agenda_path - path of the agenda file
                        project_backlog - contents of the project backlog file
                        todo_backlog - contents of the todo_backlog file
                        members - contents of the members file
                        completed_tasks - contents of the completed tasks file
                        agenda - contents of the agenda file
                        work_in_progress_limit - int for the work in progress limit
                        todo_limit - int for the todo limit
                        general_notes - string that represents the general meeting notes

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       None

        Return:         ScrumbanHistory Object

        Description:    Initialized an instance of the ScrumbanHistory Class
        """

        # set the project_backlog_path
        self.project_backlog_path = project_backlog_path
        # set the members_path
        self.members_path = members_path
        # set the todo_backlog_path
        self.todo_backlog_path = todo_backlog_path
        # set the completed_tasks_path
        self.completed_tasks_path = completed_tasks_path
        # set the agenda_path
        self.agenda_path = agenda_path

        # set the project_backlog
        self.project_backlog = project_backlog
        # set the members
        self.members = members
        # set the todo_backlog
        self.todo_backlog = todo_backlog
        # set the completed_tasks
        self.completed_tasks = completed_tasks
        # set the agenda
        self.agenda = agenda

        # set the work_in_progress_limit
        self.work_in_progress_limit = work_in_progress_limit
        # set the todo_limit
        self.todo_limit = todo_limit

        # set the general_notes
        self.general_notes = general_notes

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def check_history(self) -> bool:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       None

        Return:         boolean - True if sys_data does exist, False if sys_data
                        does not exist

        Description:    Check if the sys_data directory exists and create files
        """
        # check if the sys_data directory exists
        if ".sys_data" in listdir():
            # if it does return True
            return True
        # if not create the completed_tasks_path file
        completed = open(self.completed_tasks_path, "w")
        # close the file
        completed.close()
        # if not create the todo_backlog file
        todo = open(self.todo_backlog_path, "w")
        # close the file
        todo.close()
        # return False if the sys_data directory does not exist
        return False

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def save_system_data(self, work_in_progress_limit: int, todo_limit: int) -> None:
        """
        Parameter:      work_in_progress_limit - max amount of tasks for a member
                        todo_limit - max number of item in the todo backlog

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description:    Saves the system data into the .sys_data/sys_data in
                        order to later load the work_in_progress_limit,
                        todo_limit, project_backlog_path, and members_path
        """
        # set the work in progress limit
        self.work_in_progress_limit = work_in_progress_limit
        # set the todo limit
        self.todo_limit = todo_limit
        # grab the current working directory
        cwd = getcwd()
        # create the absolute path for the .sys_data directory
        sys_dir = cwd + "/.sys_data"
        # check that the directory does not already exist
        if ".sys_data" not in listdir():
            # create the directory
            mkdir(sys_dir)
        # open the sys_data file
        with open(sys_dir + "/sys_data.txt", "w") as sys_data:
            # write the work in progress limit to the file
            sys_data.write(f"{str(self.work_in_progress_limit)}\n")
            # write the todo limit to the file
            sys_data.write(f"{str(todo_limit)}\n")
            # write the project_backlog_path to the file
            sys_data.write(f"{str(self.project_backlog_path)}\n")
            # write the members_path to the file
            sys_data.write(f"{str(self.members_path)}\n")

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def read_system_data(self) -> None:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       self.work_in_progress_limit
                        self.todo_limit
                        self.project_backlog_path
                        self.members_path

        Return:         None

        Description:    Reads in the system data in order to load the
                        work_in_progress_limit, todo_limit, project_backlog_path,
                        and members_path
        """
        # open the sys_data file
        with open(".sys_data/sys_data.txt", "r") as sys_data:
            # read the file
            sys_data_list = sys_data.readlines()
            # set the work_in_progress_limit attribute
            self.work_in_progress_limit = int(sys_data_list[0])
            # set the todo_limit attribute
            self.todo_limit = int(sys_data_list[1])
            # set the project_backlog_path attribute
            self.project_backlog_path = sys_data_list[2].strip()
            # set the members_path attribute
            self.members_path = sys_data_list[3].strip()

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def reset_system(self) -> None:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description:    Deletes the .sys_data/ directory, in turn
                        resetting the system.
        """
        # check that the is sys_data
        if ".sys_data" in listdir():
            # remove the sys_data directory, resetting the system
            rmtree(".sys_data")

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    @staticmethod
    def check_valid_task_file(file_path:str) -> str:
        """
        Parameter:      file_path - the absolute path of the tasks file

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       None

        Return:         str - represents the error message or "VALID" if valid

        Description:    Checks that the tasks file is in the correct format
                        specified in the SRS (using regex)
        """
        # check if the file is empty
        if path.getsize(file_path) == 0:
            # return the error
            return "File is empty"
        # try the file encoding
        try:
            # open the file
            with open(file_path, "r") as f:
                # go through each line of the file
                for i, line in enumerate(f):
                    # check the regex pattern against the line
                    if not search(r"^[A-z0-9\s-]+,\s*[0-9]+,\s*[0-9]+/[0-9]+/[0-9]+\s*\n$", line):
                        # return the error message and the line number
                        return f"Error on line {i + 1} in project backlog"
                    # return that it was valid
                    return "VALID"
        # incorrect file encoding
        except UnicodeDecodeError:
            # return the error
            return "Invalid File Encoding For Project Backlog"
        # should never make it here
        return "WILL NEVER MAKE IT HERE UNLESS FATAL ERROR"

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    @staticmethod
    def check_valid_member_file(file_path: str) -> str:
        """
        Parameter:      file_path - the absolute path of the members file

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       None

        Return:         str - represents the error message or "VALID" if valid

        Description:    Checks that the members file is in the correct format
                        specified in the SRS (using regex)
        """
        # check if the file is empty
        if path.getsize(file_path) == 0:
            # return the error
            return "File is empty"
        # try the file encoding
        try:
            # open the file
            with open(file_path, "r") as f:
                # go through each line of the file
                for i, line in enumerate(f):
                    # check the regex pattern against the line
                    if not search(r"^[A-z\s-]+,\s*[A-z0-9-.]+@[A-z0-9.]+\n$", line):
                        # return the error message and the line number
                        return f"Error on line {i + 1} in members file"
                    # return that it was valid
                    return "VALID"
        # incorrect file encoding
        except UnicodeDecodeError:
            # return the error
            return "Invalid File Encoding For Member File"
        # should never make it here
        return "WILL NEVER MAKE IT HERE UNLESS FATAL ERROR"

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def _load_project_backlog(self) -> None:
        """
        Parameter:      N/A

        Called By:      load_scrumban - ScrumbanHistory.py

        Calls:          None

        Modifies:       self.project_backlog

        Return:         None

        Description:    Loads the contents of the project backlog file from the
                        project_backlog_path into the project_backlog attribute
        """
        # check that the project_backlog_path file exists
        if self.project_backlog_path != "":
            # open the project backlog file
            with open(self.project_backlog_path, "r") as project_backlog:
                # go through each task
                for task in project_backlog:
                    # add the task to the project_backlog attribute
                    self.project_backlog.append(task.strip().split(","))
            # loop through each task
            for i, task in enumerate(self.project_backlog):
                # check if it is a blank task
                if task == ['']:
                    # remove the blank task
                    self.project_backlog.pop(i)
                    # skip the blank task
                    continue
                # loop through each field of the task
                for j in range(len(task)):
                    # strip the whitespace from each field
                    task[j] = task[j].strip()

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def _load_members(self) -> None:
        """
        Parameter:      N/A

        Called By:      load_scrumban - ScrumbanHistory.py

        Calls:          None

        Modifies:       self.members

        Return:         None

        Description:    Loads the contents of the members file from the
                        members_path into the members attribute
        """
        # check that the members_path file exists
        if self.members_path != "":
            # open the members file
            with open(self.members_path, "r") as members:
                # loop through the members file
                for member in members:
                    # add each member to the members attribute
                    self.members.append(member.strip().split(","))
            # loop through each member
            for i, member in enumerate(self.members):
                # if the member does not exist
                if member == ['']:
                    # remove the member
                    self.members.pop(i)
                    # skip to the next member
                    continue
                # go through each field of the member
                for j in range(len(member)):
                    # strip the whitespace from the field
                    member[j] = member[j].strip()
                # if the member has no tasks
                if len(member) == 2:
                    # add an extra blank string
                    member.append("")
                # add the blank questions and concerns field (start of the meeting)
                member.append("")

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def _load_todo_backlog(self) -> None:
        """
        Parameter:      N/A

        Called By:      load_scrumban - ScrumbanHistory.py

        Calls:          None

        Modifies:       self.todo_backlog

        Return:         None

        Description:    Loads the todo backlog tasks from the file at
                        todo_backlog_path into the todo_backlog attribute
        """
        # checks that the todo_backlog_path file exists
        if self.todo_backlog_path != "":
            # open the todo_backlog_path file
            with open(self.todo_backlog_path, "r") as todo_log:
                # loop through the tasks
                for task in todo_log:
                    # add the tasks to the todo_backlog attribute
                    self.todo_backlog.append(task.strip().split(","))
            # go through each of the tasks
            for task in self.todo_backlog:
                # go through the fields of the tasks
                for i in range(len(task)):
                    # strip the whitespace
                    task[i] = task[i].strip()

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def _load_completed_tasks(self) -> None:
        """
        Parameter:      N/A

        Called By:      load_scrumban - ScrumbanHistory.py

        Calls:          None

        Modifies:       self.completed_tasks

        Return:         None

        Description:    Loads the completed tasks from the file at
                        completed_tasks_path into the completed_tasks attribute
        """
        # checks that the completed_tasks_path file exists
        if self.completed_tasks_path != "":
            # open the completed_tasks_path file
            with open(self.completed_tasks_path, "r") as completed_tasks:
                # skip title
                completed_tasks.readline()
                # skip headers
                completed_tasks.readline()
                # loop through the tasks
                for task in completed_tasks:
                    # add the tasks to the completed_tasks attribute
                    self.completed_tasks.append(task.strip().split(","))
            # go through each of the tasks
            for task in self.completed_tasks:
                # go through the fields of the tasks
                for i in range(len(task)):
                    # strip the whitespace
                    task[i] = task[i].strip()

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def load_scrumban(self) -> None:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          _load_project_backlog
                        _load_todo_backlog
                        _load_members
                        _load_completed_tasks

        Modifies:       self.project_backlog
                        self.todo_backlog
                        self.members
                        self.completed_tasks

        Return:         None

        Description: Calls private methods to load data in from files
        """
        # load project backlog
        self._load_project_backlog()
        # load members
        self._load_members()
        # load todo backlog
        self._load_todo_backlog()
        # load completed tasks
        self._load_completed_tasks()

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def load_agenda(self) -> None:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description: Loads the agenda from agenda_path into the agenda attribute
        """
        # make sure that the agenda file exists
        if self.agenda_path != "":
            # open the agenda file
            with open(self.agenda_path, "r") as agenda:
                # go through the agenda
                for item in agenda:
                    # add the item to the agenda attribute
                    self.agenda.append(item)

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def _save_project_backlog(self) -> None:
        """
        Parameter:      N/A

        Called By:      save_scrumban - ScrumbanHistory.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description: Saves the contents of the project_backlog attribute
                     to the file in the project_backlog_path attribute
        """
        # check if there is a project_backlog file in existence
        if self.project_backlog_path != "":
            # open the file
            with open(self.project_backlog_path, "w") as project_backlog:
                # go through each task in the completed_tasks attribute
                for task in self.project_backlog:
                    # go through each field for the task
                    for i in range(len(task)):
                        # if there is a blank
                        if task[i] == "":
                            # skip it
                            continue
                        # if the first field
                        elif i == 0:
                            # write the task
                            project_backlog.write(f"{task[i].strip()}")
                        # if not the first field
                        else:
                            # write the task
                            project_backlog.write(f", {task[i].strip()}")
                    # write a new line
                    project_backlog.write("\n")

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def _save_members(self) -> None:
        """
        Parameter:      N/A

        Called By:      save_scrumban - ScrumbanHistory.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description: Saves the contents of the members attribute
                     to the file in the members_path attribute
        """
        # check if the members file is in existence
        if self.members_path != "":
            # load the data into the class from the file
            with open(self.members_path, "w") as members:
                # go through each member
                for member in self.members:
                    # write the members name
                    members.write(f"{member[0].strip()}, ")
                    # if the member does not have any tasks
                    if member[2] == "":
                        # only write the email
                        members.write(f"{member[1].strip()}\n")
                    else:
                        # write the member's tasks
                        members.write(f"{member[1].strip()}, ")
                        # write the email
                        members.write(f"{member[2]}\n")

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def _save_todo_backlog(self) -> None:
        """
        Parameter:      N/A

        Called By:      save_scrumban - ScrumbanHistory.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description: Saves the contents of the todo_backlog attribute
                     to the file in the todo_backlog_path attribute
        """
        # check if there is a todo backlog file in existence
        if self.todo_backlog_path != "":
            # open the file
            with open(self.todo_backlog_path, "w") as todo_log:
                # go through each task in the completed_tasks attribute
                for task in self.todo_backlog:
                    # go through each field for the task
                    for i in range(len(task)):
                        # if there is a blank
                        if task[i] == "":
                            # skip it
                            continue
                        # if the first field
                        elif i == 0:
                            # write the task
                            todo_log.write(f"{task[i].strip()}")
                        # if not the first field
                        else:
                            # write the task
                            todo_log.write(f", {task[i].strip()}")
                    # write a new line
                    todo_log.write("\n")

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def _save_completed_tasks(self) -> None:
        """
        Parameter:      N/A

        Called By:      save_scrumban - ScrumbanHistory.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description: Saves the contents of the completed_tasks attribute
                     to the file in the completed_tasks_path attribute
        """
        # check if there is a completed tasks file in existence
        if self.completed_tasks_path != "":
            # open the file
            with open(self.completed_tasks_path, "w") as completed_tasks:
                completed_tasks.write(f"Completed Tasks as of {date.today()}\n")
                completed_tasks.write("Task Name, Task Priority, Due Date, Completion Date\n")
                # go through each task in the completed_tasks attribute
                for task in self.completed_tasks:
                    # go through each field for the task
                    for i in range(len(task)):
                        # if there is a blank
                        if task[i] == "":
                            # skip it
                            continue
                        # if the first field
                        elif i == 0:
                            # write the task
                            completed_tasks.write(f"{task[i].strip()}")
                        # if not the first field
                        else:
                            # write the task
                            completed_tasks.write(f", {task[i].strip()}")
                    # write a new line
                    completed_tasks.write("\n")

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def save_scrumban(self) -> None:
        """
        Parameter:      N/A

        Called By:      shutdown - VSS.py

        Calls:          _save_project_backlog
                        _save_todo_backlog
                        _save_members
                        _save_completed_tasks

        Modifies:       None

        Return:         None

        Description: This method will save the state of the scrum into files
        """
        # save the project backlog
        self._save_project_backlog()
        # save the members
        self._save_members()
        # save the todo backlog
        self._save_todo_backlog()
        # save the completed tasks
        self._save_completed_tasks()
        # check if any general notes were written during the meeting
        if self.general_notes != "":
            # format date
            date_list = str(date.today()).split('-')
            formatted_date = f'{date_list[1]}-{date_list[2]}-{date_list[0]}'
            # create the file for the notes
            with open(f"General-Notes-{formatted_date}.txt", "w") as general_notes:
                # write the file header
                general_notes.write(f"General Notes for {date.today()}\n")
                # write the notes to a file
                general_notes.write(self.general_notes)

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def send_emails(self) -> None:
        """
        Parameter:      N/A

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description: Goes through each member of the team and emails them the
                     meeting data
        """
        # assume internet connection is False
        connect_internet = False
        # test the internet connection
        try:
            # test the internet connection
            urllib.request.urlopen("http://google.com")
            # if connection is successful connect_internet is now True
            connect_internet = True
        except urllib.error.URLError:
            # if connection is unsuccessful connect_internet remains False
            connect_internet = False
        # check if connection is successful
        if not connect_internet:
            # if not successful return of the function
            return
        # open the connection to the email server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            # login to the Scrumban Account
            smtp.login("scrum.board.virtual@gmail.com", "newpassword1234")
            # loop through each member
            for i, member in enumerate(self.members):
                # create the report for each member
                with open(f".sys_data/{i}.txt", "w") as report:
                    # write the heading to the file
                    report.write(f"Scrumban Meeting Report For {date.today()}\n")
                    # write who the report is generated for
                    report.write(f"Report Generated for {member[0]}\n")
                    # format line
                    report.write("*********************************************\n")
                    # Display the task breakdown heading
                    report.write("Your Task Breakdown:\n\n")
                    # if the member has tasks currently assigned
                    if member[2] != "":
                        # split the tasks line
                        member_tasks = member[2].split(";")
                        # go through each task
                        for j, task in enumerate(member_tasks):
                            # split each field of the task
                            task = task.split("\t")
                            # write the task number
                            report.write(f"Task #{j + 1}\n")
                            # write the task name
                            report.write(f"Task Name: {task[0]}\n")
                            # write the task priority
                            report.write(f"Task Priority: {task[1]}\n")
                            # write the task due date
                            report.write(f"Due Date: {task[2]}\n\n")
                    # if no tasks are currently assigned to the member
                    else:
                        # write that no tasks are currently assigned
                        report.write("No tasks currently assigned\n\n")
                    # format line
                    report.write("*********************************************\n")
                    # write questions and concerns header
                    report.write(f"{member[0]}'s Questions and Concerns:\n")
                    # write questions and concerns
                    report.write(f"{member[3]}\n")
                    # format line
                    report.write("*********************************************\n")
                    # write meeting notes header
                    report.write("General Meeting Notes:\n\n")
                    # write meeting notes
                    report.write(f"{self.general_notes}\n")
                    # format line
                    report.write("*********************************************\n")
                # create a blank email object
                message = EmailMessage()
                # fill in the subject
                message['Subject'] = f"Meeting Report {date.today()}"
                # fill in the from field
                message['From'] = "Scrumban Team"
                # fill in the to field
                message['To'] = member[1]
                # se the body contents of the message
                message.set_content(f"Scrumban Meeting Report For {date.today()}\nReport Generated for {member[0]}\n")
                # open the report file
                with open(f".sys_data/{i}.txt", "r") as file_data:
                    # attatch the report file
                    message.add_attachment(file_data.read(), filename=f"Report_{date.today()}_{member[0]}.txt")
                # open the completed tasks file
                with open("completed_tasks.csv", "r") as completed_tasks:
                    # attatch the completed tasks file
                    message.add_attachment(completed_tasks.read(), filename=f"Completed_Tasks_{date.today()}.csv")
                # send the email
                smtp.send_message(message)

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def get_work_in_progress_limit(self) -> int:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         int that represents the max amount
                        of tasks a member can have at one time

        Description: returns the self.work_in_progress_limit attribute
        """
        # return the attribute
        return self.work_in_progress_limit

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def get_todo_limit(self) -> int:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         int that represents the max amount
                        of tasks on todo at one time

        Description: returns the self.todo_limit attribute
        """
        # return the attribute
        return self.todo_limit

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #


    def get_project_backlog(self) -> list:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         list of lists of strings that represents
                        the project backlog

        Description: returns the self.project_backlog attribute
        """
        # return the attribute
        return self.project_backlog

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #


    def get_todo_backlog(self) -> list:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         list of lists of strings that represents
                        the todo backlog

        Description: returns the self.todo_backlog attribute
        """
        # return the attribute
        return self.todo_backlog

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def get_member_list(self) -> list:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         list of lists of strings that represents
                        the members

        Description: returns the self.members attribute
        """
        # return the attribute
        return self.members

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #


    def get_completed_tasks(self) -> list:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         list of lists of strings that represents
                        the completed tasks

        Description: returns the self.completed_tasks attribute
        """
        # return the attribute
        return self.completed_tasks

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def get_agenda(self) -> list:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         list of strings that represents the agenda

        Description: returns the self.agenda attribute
        """
        # return the attribute
        return self.agenda

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def get_project_backlog_path(self) -> str:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         string that represents the path to the project backlog file

        Description: returns the self.project_backlog_path attribute
        """
        # return the attribute
        return self.project_backlog_path

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def get_members_path(self) -> str:
        """
        Parameter:      N/A

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       N/A

        Return:         string that represents the path to the members file

        Description: returns the self.members_path attribute
        """
        # return the attribute
        return self.members_path

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def set_project_backlog_path(self, file_path:str) -> None:
        """
        Parameter:      file_path - the absolute path to the project backlog file

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       self.project_backlog_path

        Return:         None

        Description: Sets the self.project_backlog_path attribute with file_path
        """
        # set the attribute
        self.project_backlog_path = file_path

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def set_members_path(self, file_path:str) -> None:
        """
        Parameter:      file_path - the absolute path to the members file

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       self.members_path

        Return:         None

        Description: Sets the self.members_path attribute with file_path
        """
        # set the attribute
        self.members_path = file_path

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def set_agenda_path(self, file_path:str) -> None:
        """
        Parameter:      file_path - the absolute path to the agenda file

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       self.agenda_path

        Return:         None

        Description: Sets the self.agenda_path attribute with file_path
        """
        # set the attribute
        self.agenda_path = file_path

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def set_project_backlog(self, project_backlog:list) -> None:
        """
        Parameter:      project_backlog - list of lists of strings that
                        represents the project backlog list

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       self.project_backlog

        Return:         None

        Description: Sets the self.project_backlog attribute
                     with project_backlog
        """
        # set the attribute
        self.project_backlog = project_backlog

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def set_members(self, members:list) -> None:
        """
        Parameter:      members - list of lists of strings that
                        represents the members list

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       self.members

        Return:         None

        Description: Sets the self.members attribute with members
        """
        # set the attribute
        self.members = members

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def set_todo_backlog(self, todo_backlog:list) -> None:
        """
        Parameter:      todo_backlog - list of lists of strings that
                        represents the todo backlog

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       self.todo_backlog

        Return:         None

        Description: Sets the self.todo_backlog attribute with todo_backlog
        """
        # set the attribute
        self.todo_backlog = todo_backlog

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def set_completed_tasks(self, completed_tasks:list) -> None:
        """
        Parameter:      completed_tasks - list of lists of strings that
                        representscompleted tasks

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       self.completed_tasks

        Return:         None

        Description: Sets the self.completed_tasks attribute with completed_tasks
        """
        # set the attribute
        self.completed_tasks = completed_tasks

    # ------------------------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    def set_general_notes(self, general_notes:str) -> None:
        """
        Parameter:      general_notes - string that represents notes

        Called By:      shutdown - VSS.py

        Calls:          None

        Modifies:       self.general_notes

        Return:         None

        Description: Sets the self.general_notes attribute with general_notes
        """
        # set the attribute
        self.general_notes = general_notes
