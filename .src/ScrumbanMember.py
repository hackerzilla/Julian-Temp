"""
File:   Scrumban Member
Author: Jaeger Jochimsen
Date:   02/16/2022
Credit:
Last Edited:
    02/16/2022      Jaeger J    Initial creation
    02/18/2022      Jaeger J    Modification of methods
    02/22/2022      Jaeger J    Docs
    02/23/2022      Jaeger J    Docs Finishing
"""
from datetime import date

class Task():
    """
    Encapsulate task data for the ScrumbanBoard module.

    Used By:
        ScrumbanBoard.py

    Members:
        Member Name:        : Type      : Default Val  -> Description
        ------------------------------------------------------------------------------------------------------------------------------------------
        self.name           : str       : -            -> a name or descriptor of the task

        self.priority       : str       : -            -> the task's numeric priority (0-99+)

        self.due_date       : str       : -            -> the task's due date in the form MM/DD/YYYY

        self.complete_date  : str       : -            -> the task's completed date in the form MM/DD/YYYY

    Methods:

        Private:                                                                     Return:
        ----------------------------------------------------------------------------|-------------------------------------------------
        N/A
        ----------------------------------------------------------------------------|-------------------------------------------------


        Public:                                                                      Return:
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_name(self)                                              |   -> name of the task as a string
                                                                                    |
        Usage:          instance.get_name()                                         |
                                                                                    |
        Description:    Return the name/descriptor of the task                      |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_priority(self)                                          |   -> priority of the task as a string (0-99+)
                                                                                    |
        Usage:          instance.get_priority()                                     |
                                                                                    |
        Description:    Return the priority of the task                             |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_due(self)                                               |   -> date task must be completed by (MM/DD/YYYY)
                                                                                    |      as a string
        Usage:          instance.get_due()                                          |
                                                                                    |
        Description:    Return the due date of the task                             |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_done(self)                                              |   -> date task was completed (MM/DD/YYYY)
                                                                                    |      as a string
        Usage:          instance.get_done()                                         |
                                                                                    |
        Description:    Return the date the task was completed                      |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_completed_date(self)                                    |   -> None
                                                                                    |
        Usage:          instance.set_completed_date()                               |
                                                                                    |
        Description:    Set the task's completed date as the current day            |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    stringify(self)                                             |   -> string representation of the task instance
                                                                                    |      in the format:
        Usage:          instance.stringify()                                        |'name<tab>priority<tab>due date<tab>completed date'
                                                                                    |
        Description:    Create and return a formatted string representation for the |
                        task instance                                               |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    listify(self)                                               |   -> list representation of the task instance
                                                                                    |      in the format:
        Usage:          instance.stringify()                                        |   [name, priority, due date, completed date]
                                                                                    |
        Description:    Create and return a list representation for the task        |
        ----------------------------------------------------------------------------|-------------------------------------------------

    """
    def __init__(self, name:str, priority:str, due:str, done_date:str):
        self.name = name
        self.priority = priority
        self.due_date = due
        self.completed_date = done_date

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def get_name(self) -> str:
        """
        Parameter:      N/A

        Called By:
            get_completed_log_as_strings()    - ScrumbanInterface.py
            project_backlog_button_clicked()  - ScrumbanInterface.py
            fill_todo_data()                  - ScrumbanInterface.py
            fill_tasks_data()                 - ScrumbanInterface.py

        Calls:          N/A

        Modifies:       N/A

        Return:         str

        Description:    return the task name/descriptor of the Task instance.
        """
        return self.name

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def get_priority(self) -> str:
        """
        Parameter:      N/A

        Called By:      member_to_member() - ScrumbanInterface.py

        Calls:          N/A

        Modifies:       N/A

        Return:         str

        Description:    return the priority of the Task instance.
        """
        return self.priority

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def get_due(self) -> str:
        """
        Parameter:      N/A

        Called By:      N/A

        Calls:          N/A

        Modifies:       N/A

        Return:         str

        Description:    return the due date of the Task MM/DD/YYYY.
        """
        return self.due_date

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def get_done(self) -> str:
        """
        Parameter:      N/A

        Called By:      N/A

        Calls:          N/A

        Modifies:       N/A

        Return:         str

        Description:    return the completed date of the Task MM/DD/YYYY.
        """
        return self.completed_date

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def set_completed_date(self) -> None:
        """
        Parameter:      N/A

        Called By:      complete_task() - ScrumbanBoard.py

        Calls:          datetime.date.today()

        Modifies:       self.completed_date

        Return:         None

        Description:    set the completed data for the Task to the
                        current date MM/DD/YYYY
        """
        # re-format for consistency
        date_list = str(date.today()).split('-')
        self.completed_date = f'{date_list[1]}/{date_list[2]}/{date_list[0]}'

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def stringify(self) -> str:
        """
        Parameter:      N/A

        Called By:      stringify() - ScrumbanMember.py (Member Class)

        Calls:          N/A

        Modifies:       N/A

        Return:         str

        Description:    create and return a string representation of all
                        Task instance's data as a single, tab-delimited str
        """
        return f'{self.name}\t{self.priority}\t{self.due_date}\t{self.completed_date}'

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def listify(self) -> list:
        """
        Parameter:      N/A

        Called By:      get_string_project_backlog() - ScrumbanBoard.py

        Calls:          N/A

        Modifies:       N/A

        Return:         list[str]

        Description:    create and return a list representation of all
                        Task instance's data
        """
        return [self.name, self.priority, self.due_date, self.completed_date]

#=========================================================================#
#=========================================================================#

class ScrumbanMember():
    """
    Encapsulate all data for a single Scrumban team member.

    Used By:
        ScrumbanBoard.py

    Members:
        Member Name:            : Type       : Default Val  -> Description
        ------------------------------------------------------------------------------------------------------------------------------
        self.name               : str        : -            -> the name of the team member

        self.email              : str        : -            -> the email of the team member

        self.current_tasks      : list[Task] : -            -> a list of the tasks (as Task objects) assigned to the team member

        self.questions_concerns : list[str]  : -            -> a list of the questions or concerns associated with the team member

    Methods:

        Private:                                                                     Return:
        ----------------------------------------------------------------------------|-------------------------------------------------
        N/A
        ----------------------------------------------------------------------------|-------------------------------------------------


        Public:                                                                      Return:
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_name(self)                                              |   -> name of the member as a string
                                                                                    |
        Usage:          instance.get_name()                                         |
                                                                                    |
        Description:    Return the name/descriptor of the member                    |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_email(self)                                             |   -> email of the member as a string
                                                                                    |
        Usage:          instance.get_email()                                        |
                                                                                    |
        Description:    Return the email of the member instance                     |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_tasks(self)                                             |   -> list of the member's tasks as Task objects
                                                                                    |
        Usage:          instance.get_tasks()                                        |
                                                                                    |
        Description:    Return the current tasks assigned to the member             |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    get_qc(self)                                                |   -> list of questions and concerns as str
                                                                                    |
        Usage:          instance.get_qc()                                           |
                                                                                    |
        Description:    Return the questions and concerns for the member            |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    add_task(self, task:Task)                                   |   -> None
                                                                                    |
        Usage:          instance.add_task(Task)                                     |
                                                                                    |
        Description:    Add a task to the member's currently assigned task list     |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    remove_task(self, index:int)                                |   -> Task object located at index index
                                                                                    |
        Usage:          instance.remove_task(int)                                   |
                                                                                    |
        Description:    Remove and return a Task from the member's assigned tasks   |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    set_qc(self, questions_concerns:str)                        |   -> None
                                                                                    |
        Usage:          instance.set_qc(str)                                        |
                                                                                    |
        Description:    Set the member's questions/concerns field                   |
        ----------------------------------------------------------------------------|-------------------------------------------------
        Declaration:    stringify(self)                                             |   -> formatted string representation of all
                                                                                    |      member's data, including tasks
        Usage:          instance.remove_task(int)                                   |  'name,email,< ";"-delimited Task strings >,questions/concerns'
                                                                                    |
        Description:    Convert and return a str representation of all member data, |
                        delimiting tasks with a ";"                                 |
        ----------------------------------------------------------------------------|-------------------------------------------------
    """
    def __init__(self, name:str, email:str, current_tasks:list, questions_concerns:str):
        self.name = name
        self.email = email
        self.current_tasks = current_tasks
        self.questions_concerns = questions_concerns

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def get_name(self) -> str:
        """
        Parameter:      N/A

        Called By:      member_to_member() - ScrumbanInterface.py

        Calls:          N/A

        Modifies:       N/A

        Return:         str

        Description:    return the name member of the Member instance.
        """
        return self.name

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def get_email(self) -> str:
        """
        Parameter:      N/A

        Called By:      N/A

        Calls:          N/A

        Modifies:       N/A

        Return:         str

        Description:    return the email member of the Member instance.
        """
        return self.email

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def get_tasks(self) -> list:
        """
        Parameter:      N/A

        Called By:      assign_task()           - ScrumbanBoard.py
                        move_member_to_member() - ScrumbanBoard.py
                        fill_tasks_data()       - ScrumbanInterface.py

        Calls:          N/A

        Modifies:       N/A

        Return:         list[Task]

        Description:    return a list of Tasks assigned to the Member
                        instance
        """
        return self.current_tasks

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def get_qc(self) -> str:
        """
        Parameter:      N/A

        Called By:      fill_questions_concerns_data() - ScrumbanInterface.py

        Calls:          N/A

        Modifies:       N/A

        Return:         str

        Description:    return the questions/concerns field of Member
                        instance as string
        """
        return self.questions_concerns

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def add_task(self, task:Task) -> None:
        """
        Parameter:
            task:       Task to add to the Member's assigned tasks

        Called By:      assign_task() - ScrumbanBoard.py

        Calls:          N/A

        Modifies:       self.current_tasks

        Return:         None

        Description:    add task to current_tasks member field
        """
        self.current_tasks.append(task)

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def remove_task(self, index:int) -> Task:
        """
        Parameter:
            index:      int index of task to remove from current_tasks

        Called By:      complete_task() - ScrumbanBoard.py

        Calls:          N/A

        Modifies:       self.current_tasks

        Return:         Task that was removed

        Description:    remove and return the task at index 'index' from
                        the current_tasks field
        """
        return self.current_tasks.pop(index)

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def set_qc(self, questions_concerns:str) -> None:
        """
        Parameter:
            questions_concerns:     string to set questions_concerns
                                    field to

        Called By:      save_text() - ScrumbanInterface.py

        Calls:          N/A

        Modifies:       self.questions_concerns

        Return:         None

        Description:    set the questions_concerns field to 'questions_concerns'

        """
        self.questions_concerns = questions_concerns

    # ----------------------------------------------------------- #
    # ----------------------------------------------------------- #

    def stringify(self) -> str:
        """
        Parameter:      N/A

        Called By:      get_string_members() - ScrumbanBoard.py

        Calls:          stringify()          - ScrumbanMember.py (Task Class)

        Modifies:       N/A

        Return:         str

        Description:    create and return string representation of Member instance
                        data, data fields are comma ',' delimited and tasks are semi-colon
                        ';' delimited

        """
        task_str = [task.stringify() for task in self.current_tasks]
        return f'{self.name},{self.email},{";".join(task_str)},{self.questions_concerns}'
