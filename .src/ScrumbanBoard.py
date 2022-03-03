"""
Scrumban Board
Author: Sam Gebhardt
Date:   02/16/2022
Last Edit: 02/16/   Sam Gebhardt    Created File
"""
from ScrumbanMember import ScrumbanMember, Task


class Board():
    """
    Class that contains the data used throughout the program.

    Used By:
        VSS.py
        ScrumbanInterface.py

    Members:
        Member Name:            : Type          : Default Val  -> Description
        ------------------------------------------------------------------------------------------------------------------------------------------
        self.project_backlog    : list[Task]    : -             -> a list of Task objects representing the tasks

        self.todo_backlog       : list[Task]    : -             -> a list of Tasl objects that represent tasks that must
                                                                   be completed, but aren't assigned to a member

        self.completed_backlog  : list[Task]    : -             -> a list of task objects that represent tasks that have been completed

        self.members            : list[ScrumbanMembers] : -     -> a list of ScrumbanMember objects that represent each
                                                                   member on the team

        self.agenda             : list[Str]     : -             -> a list of strings where each item is a new task to discuss
                                                                   in the meering

        self.notes              : Str           : ""            -> a string that contains all the notes taken during the course
                                                                   of the meeting

        self.max_todo_size      : int           : 4             -> the max number of tasks that can be in the todo backlog

        self.task_member_limit  : int           : 4             -> the max number of tasks that can be assigned to a member

    Methods:

        Public:                                                                      Return:
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    backlog_to_todo(self)                                       |   ->  None
                                                                                    |
        Usage:          instance.backlog_to_todo(self)                              |
                                                                                    |
        Description:    Move all the tasks from the project backlog into todo       |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    assign_task(self, member_id: int, task_id: int)             |   ->  int
                                                                                    |
        Usage:          instance.assign_task(self, 2, 0)                            |
                                                                                    |
        Description:    Move the task specified by task_id from the todo backlog    |
                        into the task list for the member specified by member_id    |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    move_member_to_member(self, member1: int,                   |    -> int
                                                    member2: int, task_id: int)     |                                            |   ->  list[Student]
                                                                                    |
        Usage:          instance.move_member_to_member(0, 1, 3)                     |
                                                                                    |                                                                |
        Description:    Move the task specified by task_id from member1 to member2  |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    member_to_todo(self, member_id: int, task_id: int)          |   -> int
                                                                                    |
        Usage:          instance.member_to_todo(2, 3)                               |
                                                                                    |
        Description:    Move the task specified by task_id from the member          |
                        specified by member_id to the todo backlog                  |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    complete_task(self, member: int, member_task_id: int)       |   -> None                                           |   ->  None
                                                                                    |
        Usage:          instance.complete_task(0, 3)                                |
                                                                                    |
        Description:    For the specified member, move the member's task specified  |
                        by member_task_id into the completed backlog                |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    completed_to_todo(self, index: int)                         |   -> None
                                                                                    |
        Usage:          instance.completed_to_todo(3)                               |
                                                                                    |
        Description:    Move the task specified by index from the completed backlog |
                        to the todo backlog                                         |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_agenda(self)                                            |   ->  list[Str]
                                                                                    |
        Usage:          instance.get_agenda()                                       |
                                                                                    |
        Description:    Returns the agenda (self.agenda)                            |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_agenda(self, agenda: list[Str])                         |   ->  None
                                                                                    |
        Usage:          instance.set_agenda()                                       |
                                                                                    |
        Description:    Sets the agenda attribute with agenda                       |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_todo(self)                                              |   ->  list[Task]
                                                                                    |
        Usage:          instance.get_todo()                                         |
                                                                                    |
        Description:    Returns the todo backlog (self.todo_backlog)                |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_project_backlog(self)                                   |   -> list[Task]
                                                                                    |
        Usage:          instance.get_project_backlog()                              |
                                                                                    |
        Description:    Returns the project backlog (self.project_backlog)          |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_completed(self)                                         |   ->  list[Task]
                                                                                    |
        Usage:          instance.get_completed()                                    |
                                                                                    |
        Description:    Returns the completed backlog (self.completed_backlog)      |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_notes(self)                                             |   ->  Str
                                                                                    |
        Usage:          instance.get_notes()                                        |
                                                                                    |
        Description:    Returns the notes (self.notes)                              |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_members(self)                                           |   ->  list[ScrumbanMembers]
                                                                                    |
        Usage:          instance.get_members()                                      |
                                                                                    |
        Description:    Returns the list of members (self.members)                  |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_string_project_backlog(self)                            |   -> list[list[Str]]
                                                                                    |
        Usage:          instance.get_string_project_backlog()                       |
                                                                                    |
        Description:    Return the project backlog as a list of strings             |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_string_members(self)                                    |   -> list[[list[Str]]
                                                                                    |
        Usage:          instance.get_string_members()                               |
                                                                                    |
        Description:    Return the members as a list of strings                     |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_string_todo(self)                                       |   -> list[list[Str]]
                                                                                    |
        Usage:          instance.get_string_todo()                                  |
                                                                                    |
        Description:    Return the todo backlog as a list of strings                |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_string_completed(self)                                  |   -> list[list[Str]]
                                                                                    |
        Usage:          instance.get_string_completed()                             |
                                                                                    |
        Description:    Return the completed backlog as a list of strings           |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_notes(self, notes: str)                                 |   -> None
                                                                                    |
        Usage:          instance.set_notes()                                        |
                                                                                    |
        Description:    Updates the self.notes attribute to equal the notes argument|
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_max_todo_size(self)                                     |
                                                                                    |
        Usage:          instance.get_max_todo_size()                                |
                                                                                    |
        Description:     Returns the max todo size                                  |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_task_member_limit(self)                                 |
                                                                                    |
        Usage:          instance.get_task_member_limit()                            |
                                                                                    |
        Description:    Returns the Task member limit                               |
        ----------------------------------------------------------------------------|-------------------------------------------------
    """

    def __init__(self, project_backlog:list, todo_backlog:list, members:list,
            completed_backlog:list, agenda:list, task_limit=4, todo_limit=4):

        # list of tasks for the project backlog
        self.project_backlog = []

        # list of tasks for the todo backlog
        self.todo_backlog = []

        # list of tasks for the completed backlog
        self.completed_backlog = []

        # list of ScrumbanMembers for each member of the team
        self.members = []

        # Holds the agenda for the meeting
        self.agenda = agenda

        # Holds any notes made during the course of the meeting
        self.notes = ""

        # the max number of tasks that can be stored in the todo backlog
        self.max_todo_size = todo_limit

        # The max number of task each member can work on
        self.task_member_limit = task_limit

        # member: each item in the members argument
        # For each inputted user,create a Task object for each task
        # assigned to the user, then create a Scrumban Member object
        # for the team member
        for member in members:

            # tasks:A list of task objects from each member
            tasks = []

            # If the user has at least one task
            if member[2] != "":
                # tasks are delimited by ;
                # task: Each task in the master list of tasks for each member
                for task in member[2].split(';'):
                    # task_fields: A list of each field of the task
                    task_fields = task.split('\t')

                    # Create a task object using the indiviudal task fields
                    tasks.append(Task(task_fields[0], task_fields[1], task_fields[2], ""))

            # new_member: A ScrumbanMember object that has the members email, name
            # list of task objects and any questions or concerns
            new_member = ScrumbanMember(member[0], member[1], tasks, member[3])
            self.members.append(new_member)

        # task: each task from the inputted project_backlog
        for task in project_backlog:
            # Create a task object with the following arguments:
            # task name,  priority, due date, completed date
            # Then add it to the class attribute
            self.project_backlog.append(Task(task[0], task[1], task[2], ""))

        # sort the project backlog on priority
        task_bubble_sort(self.project_backlog)

        # task: each task from the inputted project_backlog
        for task in todo_backlog:
            # Create a task object with the following arguments:
            # task name,  priority, due date, completed date
            # Then add it to the class attribute
            self.todo_backlog.append(Task(task[0], task[1], task[2], ""))

        # _: temp var that is only for iteration
        # Add the tasks from the project backlog to
        # the todo backlog without going over the todo_limit
        for _ in range(len(self.todo_backlog), todo_limit):

            # if the project backlog is empty stop
            if not self.project_backlog:
                break

            # Move the task from project to todo backlog
            self.todo_backlog.append(self.project_backlog.pop(0))

        # task: each task from the inputted project_backlog
        for task in completed_backlog:
            # Create a task object with the following arguments:
            # task name,  priority, due date, completed date
            # Then add it to the class attribute
            self.completed_backlog.append(Task(task[0], task[1], task[2], task[3]))

    def backlog_to_todo(self) -> None:
        """
        Parameter:
            None

        Called By:
            refresh_todo_button_clicked - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            self.project_backlog
            self.todo_backlog

        Return:
            None

        Description:
            - Add tasks to the todo backlog from the project backlog till max
                todo size is reached
        """
        # _: temp var that is only for iteration
        # Add the tasks from the project backlog to
        # the todo backlog without going over the todo_limit
        for _ in range(len(self.todo_backlog), self.max_todo_size):

            # if the project backlog is empty stop
            if not self.project_backlog:
                break

            # Move the task from project to todo backlog
            self.todo_backlog.append(self.project_backlog.pop(0))

    def assign_task(self, member_id: int, task_id: int) -> int:
        """
        Parameters:
            member_id: The index of the member that is getting assigned a task
            task_id: The index of the task (from todo backlog) that is getting
                assigned to the member

        Called By:
            todo_to_member - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            self.project_backlog
            self.todo_backlog

        Return:
            int

        Description:
            - Move task from todo backlog to member. If WIP limit is met,
                then do not assign task and return 1 for error, else 0
        """

        # if the member currently has the max number of tasks return error to caller
        if len(self.members[member_id].get_tasks()) == self.task_member_limit:
            return 1

        if not len(self.todo_backlog) == 0:
            # task: The task being moved from todo to the member
            # Remove the correct task and add it to the specified member
            task = self.todo_backlog.pop(task_id)
            self.members[member_id].add_task(task)

        # Return 0 as the operation was successful
        return 0

    def move_member_to_member(self, member1: int, member2: int,
                              task_id: int) -> int:
        """
        Parameters:
            member1: The index of the member that is losing a task
            member2: The index of the member that is getting assigned a task
            task_id: The index of the task (from member1) that is getting
                assigned to the member

        Called By:
            member_to_member - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            self.members

        Return:
            int

        Description:
            - Move a task from a member to another member
        """

        # if the member currently has the max number of tasks return error to caller
        if len(self.members[member2].get_tasks()) == self.task_member_limit:
            return 1

        # task: The task being moved from member1 to member2
        # Remove the task from member1 and add it to member2
        task = self.members[member1].current_tasks.pop(task_id)
        self.members[member2].current_tasks.append(task)

        # Return 0 as the operation was successful
        return 0

    def member_to_todo(self, member_id: int, task_id: int) -> int:
        """
        Parameters:
            member_id: The index of the member that is losing a task
            task_id: The index of the task (from member_id) that is getting
                assigned to the todo backlog

        Called By:
            member_to_todo - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            self.members
            self.todo_backlog

        Return:
            int

        Description:
            Move a task from a member to the todo backlog
        """

        # if the member currently has the max number of tasks return error to caller
        if len(self.todo_backlog) == self.max_todo_size or self.members[member_id].get_tasks() == []:
            return 1

        # task: The task being moved from member to todo
        # Remove the task from member and add it to the todo backlog
        task = self.members[member_id].remove_task(task_id)
        self.todo_backlog.append(task)

        # Return 0 as the operation was successful
        return 0

    def complete_task(self, member: int, member_task_id: int) -> None:
        """
        Parameters:
            member: The index of the member that is losing a task
            member_task_id: The index of the task (from member_id) that is getting
                assigned to the todo backlog

        Called By:
            member_to_complete - ScrumbanInterface.py

        Calls:
           [Task].set_completed_date()

        Modifies:
            self.members
            self.completed_backlog

        Return:
            int

        Description:
            Move a task from a member to the completed backlog
        """

        # task: The task being moved from member to completed
        # Remove the task from member
        task = self.members[member].remove_task(member_task_id)

        # Set the date of task completion
        task.set_completed_date()

        # Add the task to completed
        self.completed_backlog.append(task)

    def completed_to_todo(self, index:int) -> int:
        """
        Parameters:
            index: The index of the task that is moving from
                the completed backlog to the todo backlog

        Called By:
            completed_to_todo - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            self.todo_backlog
            self.completed_backlog

        Return:
            int

        Description:
            Move a task from the completed backlog to the todo backlog
        """
        if len(self.todo_backlog) == self.max_todo_size:
            return 1

        task = self.completed_backlog.pop(index)
        self.todo_backlog.append(task)
        return 0

    def set_agenda(self, agenda: list) -> None:
        """
        Parameters:
            agenda: A list of strings that where each string is an agenda item

        Called By:
            import_agenda_clicked - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            self.agenda

        Return:
            None

        Description:
            Sets the agenda attribute with agenda
        """
        self.agenda = agenda

    def get_agenda(self) -> list:
        """
        Parameters:
            None

        Called By:
            agenda_button_clicked - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            None

        Return:
            list[str]

        Description:
            Returns agenda as list of strings
        """
        return self.agenda

    def get_todo(self) -> list:
        """
        Parameters:
            None

        Called By:
            refresh_todo_button_clicked, fill_todo_data - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            None

        Return:
            list[Task]

        Description:
            Returns todo as a list of strings"""
        return self.todo_backlog

    def get_project_backlog(self) -> list:
        """
        Parameters:
            None

        Called By:
            refresh_todo_button_clicked, project_backlog_button_clicked - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            None

        Return:
            list[Task]

        Description:
            Returns the project backlog
        """
        return self.project_backlog

    def get_completed(self) -> list:
        """
        Parameters:
            None

        Called By:
            get_completed_log_as_strings - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            None

        Return:
            list[Task]

        Description:
            Returns the completed backlog
        """
        return self.completed_backlog

    def get_notes(self) -> str:
        """
        Parameters:
            None

        Called By:
            fill_notes_data - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            None

        Return:
            string

        Description:
            Returns the notes
        """
        return self.notes

    def get_members(self) -> list:
        """
        Parameters:
            None

        Called By:
            save_text, todo_to_member, member_to_member, set_up_members -  ScrumbanInterface.py

        Calls:
           None

        Modifies:
            None

        Return:
            list[ScrumbanMembers]

        Description:
            Returns a list of member objects
        """
        return self.members

    def get_string_project_backlog(self) -> list: #UNUSED
        """
        Parameters:
            None

        Called By:
            shutdown - VSS.py

        Calls:
           [Task].listify()

        Modifies:
            None

        Return:
            list[str]

        Description:
            Return project backlog as a list of strings
        """

        # project_backlog_list: A list to hold the list of
        # strings that will be returned from the function
        project_backlog_list = []

        # task: Each task object in the project backlog
        # Turn each task from an object into a list of strings
        # that contain the attributes of the Task class
        for task in self.project_backlog:
            project_backlog_list.append(task.listify())

        # return the list of list of strings
        return project_backlog_list

    def get_string_members(self) -> list:
        """
        Parameters:
            None

        Called By:
            shutdown - VSS.py

        Calls:
           [ScrumbanMember].stringify()

        Modifies:
            None

        Return:
            list[str]

        Description:
            Return members as a list of string
        """

        # member_list: Holds the strings representation of the members
        member_list = []

        # member: Each member object in self.members
        # Add the string representation of a member to the member_list
        for member in self.members:
            member_list.append(member.stringify().split(","))

        # return the list of list of strings
        return member_list

    def get_string_todo(self) -> list:
        """
        Parameters:
            None

        Called By:
            shutdown - VSS.py

        Calls:
           [Task].listify()

        Modifies:
            None

        Return:
            list

        Description:
            Return todo backlog as a string"""

        # todo_list: Holds the strings representation of the todo backlog
        todo_list = []

        # task: Each task object in self.todo_backlog
        # Add the string representation of a task to the todo_list
        for task in self.todo_backlog:
            todo_list.append(task.listify())

        # return the list of list of strings
        return todo_list

    def get_string_completed(self) -> list:
        """
        Parameters:
            None

        Called By:
            shutdown - VSS.py

        Calls:
           [Task].listify()

        Modifies:
            None

        Return:
            list[str]

        Description:
            Return completed backlog as a list of strings
        """

        # todo_list: Holds the strings representation of the completed backlog
        completed_backlog = []

        # task: Each task object in self.completed_backlog
        # Add the string representation of a task to the completed_backlog
        for task in self.completed_backlog:
            completed_backlog.append(task.listify())

        # return the list of list of strings
        return completed_backlog

    def set_notes(self, notes: str) -> None:
        """
        Parameters:
            notes: A string that holds the new notes for the meeting

        Called By:
            save_text - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            self.notes

        Return:
            None

        Description:
            Updates the notes
        """
        self.notes = notes

    def get_max_todo_size(self) -> int:
        """
        Parameters:
            None

        Called By:
            maximums_button_clicked - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            None

        Return:
            int

        Description:
            Returns the max todo size
        """
        return self.max_todo_size

    def get_task_member_limit(self) -> int:
        """
        Parameters:
            None

        Called By:
            get_task_member_limit - ScrumbanInterface.py

        Calls:
           None

        Modifies:
            None

        Return:
            int

        Description:
            Returns the Task member limit
        """
        return self.task_member_limit


def task_bubble_sort(lst: list) -> None:
    """
    Parameters:
        lst: The project backlog

    Called By:
        Board.__init__()

    Calls:
        None

    Modifies:
        lst

    Return:
        None

    Description:
        A helper function to sort the backlog by priority
    """

    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            if int(lst[j].get_priority()) > int(lst[j+1].get_priority()):
                temp = lst[j]
                lst[j] = lst[j + 1]
                lst[j+1] = temp
