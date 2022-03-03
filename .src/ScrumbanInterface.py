"""
File: ScrumbanInterface.py

Description: This module is responsible for outlining the user interface and user experience
             for the Virtual Scrumban System.

             It completes several tasks:

             1. Outlines the structure of the widgets and layout of widgets for the main interface window
             2. Outlines the structure of the widgets and layout of popout windows
             3. Outlines the structure error alert windows when the user attempts to do a prohibited action
             4. Outlines the structure for accepting all initializing information including asking for
             maximum task values and file paths for input files
             4. Performs all key bindings

Dependencies: Tkinter

Author(s): JD Paul

Date Created: 2/15/2022 at 3:45 PM

Dates Modified: 2/16/2022, 2/17/2022, 2/18/2022, 2/19/2022, 2/20/2022, 2/22/2022, 2/23/2022, 2/24/2022, 2/25/2022,
                2/26/2022
"""
import sys
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.messagebox import askyesno

# Window and frame pixel size constants
min_width: int = 1295
min_height: int = 800
button_bar_height: int = 0
todo_and_notes_width: int = 500

# Color values
button_bar_background_color: str = "#ececec"
todo_and_notes_frame_background_color: str = "#FFFFFF"
todo_background_color: str = "#4BAE67"
notes_background_color: str = "#EEF082"
member_frame_background_color: str = "#FFFFFF"
member_background_color: str = "#2E94F1"
member_field_background_color: str = "#C0D2E7"

# Fonts
heading_1_font = ("Times", 25)
heading_2_font = ("Times", 16)
body_font = ("Times", 20)
task_font = ("Times", 20)


class GetInitializingInfo(Tk):
    """
    Outlines the structure for the window that gets the maximum number of tasks allowed in the todolist and the maximum
    number of tasks allowed in a member's task list.

    Used by:
        VSS.py

    Members:
        Member Name:                : Type              : Default Val           -> Description
        ----------------------------------------------------------------------------------------------------------------
        self.max_tasks_in_todo      : int               : None                  -> Holds the maximum number to tasks
                                                                                   allowed in the todo list

        self.max_tasks_per_member   : int               : None                  -> Holds the maximum number to tasks
                                                                                   allowed in a member's task list
    """

    def __init__(self, vss):
        """
        Parameter:      vss - the singleton instance of the VSS class used for setting the limits

        Called By:      startup - VSS.py

        Calls:          None

        Modifies:       None

        Return:         None

        Description:    This class creates a window that accepts values from the user to set the max number of tasks per
                        member and max number of tasks per todo list.
        """
        super().__init__()

        self.max_tasks_in_todo = None
        self.max_tasks_per_member = None

        # Set the size of the tkinter window
        self.geometry("400x200")

        # Set the title at the top of the window
        self.title("Task Length Options")

        # Set the resizable property False
        self.resizable(False, False)

        def give_number():
            try:
                self.max_tasks_in_todo = int(todo_task_count_entry.get())
                self.max_tasks_per_member = int(member_task_count_entry.get())
            except:
                return
            vss.set_limits(self.max_tasks_per_member, self.max_tasks_in_todo)
            print("Destroying and quiting window")
            self.destroy()
            self.quit()

        # Create an Entry widget
        Label(self, text="Input the maximum todo limit", font=body_font).pack()
        todo_task_count_entry = Entry(self, width=35)
        todo_task_count_entry.pack()

        Label(self, text="Input the maximum member task length", font=body_font).pack()
        member_task_count_entry = Entry(self, width=35)
        member_task_count_entry.pack()

        Button(self, text="Submit Values", command=give_number).pack()


class ScrumbanInterface(Tk):
    """
    Outlines the structure for the window that gets the maximum number of tasks allowed in the todolist and the maximum
    number of tasks allowed in a member's task list.

    Used by:
        VSS.py

    Members:
        Member Name:                : Type              : Default Val           -> Description
        ----------------------------------------------------------------------------------------------------------------
        self.vss                    : VSS               : vss                   -> Holds an instance of VSS which is
                                                                                used only for triggering  sending
                                                                                emails when the button is pressed

        self.board_data             : ScrumbanBoard     : None                  -> Holds an instance of ScrumbanBoard
                                                                                which is used for all loading of
                                                                                data

        self.member_interfaces      : [ScrumbanMemberInt: []                    -> Holds an a list of all the member
                                                 erface]                        interfaces; one for each member

        self.maximums_button        : Button            : None                  -> Holds an instance of a tkinter button
                                                                                for opening the maximums window

        self.send_reports_button    : Button            : None                  -> Holds the button for sending email
                                                                                reports

        self.completed_log_button   : Button            : None                  -> Holds the button that opens the
                                                                                completed log

        self.agenda_button          : Button            : None                  -> Holds the button that opens the
                                                                                agenda window

        self.project_backlog_button : Button            : None                  -> Holds an button to open the project
                                                                                backlog window

        self.refresh_todo_button    : Button            : None                  -> Holds the button to refresh the todo
                                                                                log to display its maximum number of
                                                                                tasks

        self.button_bar_frame       : Frame             : Frame()               -> Holds the frame that contains all the
                                                                                buttons

        self.maximums_window_exits  : Bool              : False                 -> True if the window exists and false
                                                                                if not

        self.completed_log_window_ex: Bool              : False                  -> True if the window exists and false
        ists                                                                    if not

        self.agenda_window_exists   : Bool              : False                  -> True if the window exists and false
                                                                                if not

        self.project_backlog_window_: Bool              : False                  -> True if the window exists and false
        exists                                                                  if not

        self.maximums_window        : Toplevel          : None                  -> Holds the window that displays what
                                                                                the maximums are set to

        self.completed_log_window   : Toplevel          : None                  -> Holds the window that displays the
                                                                                list of completed tasks

        self.agenda_window          : Toplevel          : None                  -> Holds the window that displays the
                                                                                agenda that the user inputted

        self.project_backlog_window : Toplevel          : None                  -> Holds the window that displays the
                                                                                list of tasks in the project backlog

        self.below_buttons_frame    : Frame             : Frame()               -> Holds the frame for everything in the
                                                                                window below the button bar frame

        self.todo_and_notes_frame   : Frame             : Frame()               -> Holds the frame that contains the
                                                                                todos and the notes widgets

        self.todo_list_box          : Listbox           : None                  -> Holds the widget that contains the
                                                                                todos

        self.meeting_notes_scrolled_: ScrolledText      : None                  -> Holds the widget that contains the
        text                                                                    meeting notes text

        self.members_frame          : Frame             : Frame()               -> Holds the frame that contains all the
                                                                                member interface instances

        self.task_move_case         : Int               : 0                     -> An intefger that represents what
                                                                                task movements can be done at some point

        self.menu_bar               : Menu              : Menu()                -> Holds the menu bar and it's options


    Methods:

        Private:                                                                     Return:
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _save_text(self)                                            |   -> None
                                                                                    |
        Usage:          instance._save_text()                                       |
                                                                                    |
        Description:    Saves the state of all the text in the member's questions   |
                        and concerns notes boxes as well as in the meeting notes.   |
                        Then it sets up a call on _save_text every 1 millisecond    |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _set_unmap_key_bindings(self)                               |   -> None
                                                                                    |
        Usage:          instance._set_unmap_key_bindings()                          |
                                                                                    |
        Description:    Unmaps the key bindings so that a key is not accidentally   |
                        bound to a command                                          |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _set_completed_to_todo_bindings(self)                       |   -> None
                                                                                    |
        Usage:          instance._set_completed_to_todo_bindings()                  |
                                                                                    |
        Description:    Sets up the key bindings for moving tasks from completed    |
                        to todo                                                     |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _set_key_binding(self)                                      |   -> None
                                                                                    |
        Usage:          instance._set_key_bindingd()                                |
                                                                                    |
        Description:    Sets all other key bindings based on the task key bindings  |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _get_completed_log_as_strings(self)                         |   -> [Tasks name as strings]
                                                                                    |
        Usage:          instance._get_completed_log_as_strings(self)                |
                                                                                    |
        Description:    Gets all the tasks that are completed and puts them in list |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _send_reports_button_clicked(self)                          |   -> None
                                                                                    |
        Usage:          instance._send_reports_button_clicked()                     |
                                                                                    |
        Description:    Calls the VSS to send meeting data over emails              |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _refresh_todo_button_clicked(self)                          |   -> None
                                                                                    |
        Usage:          instance._refresh_todo_button_clicked()                     |
                                                                                    |
        Description:    Refreshes the tasks in the todo list on screen              |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:     _completed_log_button_clicked(self)                        |   -> None
                                                                                    |
        Usage:          instance._completed_log_button_clicked()                    |
                                                                                    |
        Description:    Opens a new window that shows the completed log             |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _maximums_button_clicked(self)                              |   -> None
                                                                                    |
        Usage:          instance._maximums_button_clicked()                         |
                                                                                    |
        Description:    Opens a new window that shows the maximum tasks for members |
                        and in the todo list                                        |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _agenda_button_clicked(self)                                |   -> None
                                                                                    |
        Usage:          instance._agenda_button_clicked(self)                       |
                                                                                    |
        Description:    Opens a new window that shows the agenda                    |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _project_backlog_button_clicked(self)                       |   -> None
                                                                                    |
        Usage:          instance._project_backlog_button_clicked()                  |
                                                                                    |
        Description:    Opens a new window that shows the project backlog           |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _on_closing(self, window)                                   |   -> None
                                                                                    |
        Usage:          instance._on_closing(self.completed_log_window)             |
                                                                                    |
        Description:    Based on the window sent to the function, the window exists |
                        value is set to false. It also destroys the window          |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _mouse_click(self, event)                                   |   -> None
                                                                                    |
        Usage:          Its binded as the action to a button press                  |
                                                                                    |
        Description:    Sets the task_move_case number                              |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _completed_to_todo(self, completed_task_index)              |   -> None
                                                                                    |
        Usage:          instance._completed_to_todo(2)                              |
                                                                                    |
        Description:    Moves a task in the completed list to todo list             |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _todo_to_member(self, member_index, task_in_todo_index)     |   -> None
                                                                                    |
        Usage:          instance._todo_to_member(2, 4)                              |
                                                                                    |
        Description:    Moves a task from todo list to a member list                |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _member_to_todo(self, member_index, task_in_member_index)   |   -> None
                                                                                    |
        Usage:          instance._member_to_todo(2, 3)                              |
                                                                                    |
        Description:    Moves a task from a member to the todo list                 |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _member_to_complete(self, event)                            |   -> None
                                                                                    |
        Usage:          Its binded as the action to a button press                  |
                                                                                    |
        Description:    Moves a member's task to complete based on the member that  |
                        is selected                                                 |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _member_to_member(self, from_member_index,                  |   -> None
                                         task_in_member_index, to_member_index)     |
        Usage:          instance._member_to_member(1, 2, 3)                         |
                                                                                    |
        Description:    Moves a member's task to another member's task list         |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _fill_todo_data(self)                                       |   -> None
                                                                                    |
        Usage:          instance._fill_todo_data(self)                              |
                                                                                    |
        Description:    Fills the todo list box with tasks                          |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _set_up_button_bar(self)                                    |   -> None
                                                                                    |
        Usage:          instance._set_up_button_bar()                               |
                                                                                    |
        Description:    Places the buttons on the button bar and connects them to   |
                        their command                                               |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _set_up_below_buttons_frame(self)                           |   -> None
                                                                                    |
        Usage:          instance._set_up_below_buttons_frame()                      |
                                                                                    |
        Description:    Places the below buttons frame                              |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _set_up_todo_and_notes(self)                                |   -> None
                                                                                    |
        Usage:          instance._set_up_todo_and_notes()                           |
                                                                                    |
        Description:    Places the frames and widgets in the todo and notes section |
                        of the window                                               |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _set_up_members(self)                                       |   -> None
                                                                                    |
        Usage:          instance._set_up_members()                                  |
                                                                                    |
        Description:    Places the members widgets and sets up the scroll bar       |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _set_up_menu_bar(self)                                      |   -> None
                                                                                    |
        Usage:          instance._set_up_menu_bar(self)                             |
                                                                                    |
        Description:    Sets up the menu bar options                                |
        ----------------------------------------------------------------------------|-----------------------------------

    Public:                                                                          Return:
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    set_board_data(self, board_data)                            |   -> None
                                                                                    |
        Usage:          instance.set_board_data(board_data)                         |
                                                                                    |
        Description:    Sets the board data attribute and fills the data and starts |
                        the save text loop                                          |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    set_message_box(self, window_title, message)                |   -> None
                                                                                    |
        Usage:          instance.set_message_box("Bob", "Bob the Builder is cool")  |
                                                                                    |
        Description:    Creates up a message box with the data the method is passed |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    get_project_backlog_input(self)                             |   -> String that is a file path
                                                                                    |
        Usage:          instance.get_project_backlog_input()                        |
                                                                                    |
        Description:    Creates a file opener that returns the path                 |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    get_members_input(self)                                     |   -> String that is a file path
                                                                                    |
        Usage:          instance.get_members_input()                                |
                                                                                    |
        Description:    Creates a file opener that returns the path                 |
        ----------------------------------------------------------------------------|-----------------------------------
    """

    def __init__(self, vss):
        """
        Parameter:      vss - the singleton instance of the VSS class used various value setting.

        Called By:      startup - VSS.py

        Calls:          _set_up_button_bar
                        _set_up_below_buttons_frame
                        _set_up_todo_and_notes

        Modifies:       None

        Return:         None

        Description:    This class creates the main window UI of the program and instantiates the member interfaces.
        """
        super().__init__()

        self.vss = vss

        # Board and members will be filled when add_board method is called
        self.board_data = None  # Type: ScrumbanBoard

        # Lists with a one-to-one relationship to the number of members in the board data's member list
        self.member_interfaces = []  # Type: [ScrumbanInterface]

        # Set the title at the top of the window
        self.title("Scrumban Board")

        # The window will open with the size below and will not allow the user to shrink it any more
        self.minsize(min_width, min_height)

        # Set the resizable property False
        self.resizable(False, False)

        # Create a frame where all the buttons will go
        # (ie. send reports, open agenda, open project backlog, open completed log)
        self.maximums_button = None
        self.send_reports_button = None
        self.completed_log_button = None
        self.agenda_button = None
        self.project_backlog_button = None
        self.refresh_todo_button = None
        self.button_bar_frame = Frame(self, bg=button_bar_background_color, width=1, height=1)
        self._set_up_button_bar()

        # Boolean values for if a window exists
        self.maximums_window_exits = False
        self.completed_log_window_exists = False
        self.agenda_window_exists = False
        self.project_backlog_window_exists = False

        # Variables that hold instantiations for popout windows
        self.maximums_window = None
        self.completed_log_window = None
        self.agenda_window = None
        self.project_backlog_window = None

        # Create the frame that all the widgets besides the button bar frame are placed
        self.below_buttons_frame = Frame(self, height=1, width=1)
        self._set_up_below_buttons_frame()

        # Create the todo_and_notes_frame and fill it with data
        self.todo_and_notes_frame = Frame(self.below_buttons_frame, bg=todo_and_notes_frame_background_color,
                                          width=todo_and_notes_width)
        # Variables that will store the todos list of tasks names and notes text
        self.todo_list_box = None  # The Listbox that will hold the notes
        self.meeting_notes_scrolled_text = None  # The ScrolledText box for meeting notes
        self._set_up_todo_and_notes()

        # Instantiate the members and fill them with data
        self.members_frame = Frame(self.below_buttons_frame, bg=member_background_color)

        # Variables for event handlers
        # Must distinguish if the move is a nothing_is_picked or _todo_to_member or
        # _member_to_completed (case 0, 1, 2) respectively
        self.task_move_case: int = 0  # start with case nothing_is_picked

        # Set up the menu bar at the top of the desktop on macOS and top of the window for Windows and Linux
        self.menu_bar = Menu(self)
        self._set_up_menu_bar()
        self.config(menu=self.menu_bar)

    def _save_text(self):
        """
        Parameter:      None

        Called By:      self
                        _set_board_data

        Calls:          get_questions_concerns_text - MemberInterface

                        get_members,
                        set_notes,
                        set_qc - ScrumbanBoard

                        _save_text - Self

                        after
                        scrolledtext.get - Tkinter

        Modifies:       None

        Return:         None

        Description:    Saves all text written in the questions and concerns section of the member interfaces and the
                        meeting notes text. It sets itself to be called every 1 milisecond (1 thousandth of a second).
        """
        # Save all system text every 10 seconds
        member_index = 0
        for member_interface in self.member_interfaces:
            questions_concerns_text = member_interface.get_questions_concerns_text()
            self.board_data.get_members()[member_index].set_qc(questions_concerns_text)
            member_index += 1
            # save the members questions/concerns
        # Save the meeting notes text
        meeting_notes = self.meeting_notes_scrolled_text.get("1.0", END)
        self.board_data.set_notes(meeting_notes)
        self.after(1, self._save_text)  # the delay is in milliseconds

    # SETTERS ----------------------------------------------------------------------------------------------------------
    def set_board_data(self, board_data):
        """
        Parameter:      board_data: ScrumbanBoard

        Called By:      self
                        _set_board_data

        Calls:          _set_up_members
                        _fill_todo_data
                        _set_key_bindings
                        _save_text

        Modifies:       self.board_data

        Return:         None

        Description:    Sets the board data parameter. With that information the interface can now set up the member
                        interface, _save_text functionality, key bindings, and todo data
        """
        # Called by VSS in init as the second to last task for the init method
        self.board_data = board_data
        self._set_up_members()
        self._fill_todo_data()
        self._set_key_bindings()
        self._save_text()

    def _set_unmap_key_bindings(self):
        """
        Parameter:      None

        Called By:      _set_key_bindings

        Calls:          bind - tkinter

        Modifies:       None

        Return:         None

        Description:    Unmaps all keys that may have been previously mapped to an event handler function.
                        The mouse button stays mapped no matter what
        """
        for number in range(10):
            self.bind(str(number), lambda event: print(f"a number key is unmapped"))
        self.bind("<Control-d>", lambda event: print("Control-d key is unmapped"))
        self.bind("<Control-r>", lambda event: print("Control-r is unmapped"))

    def _set_completed_to_todo_bindings(self):
        """
        Parameter:      None

        Called By:      _set_key_bindings

        Calls:          bind - tkinter

        Modifies:       None

        Return:         None

        Description:    binds the completed to todo buttons if the completed log window is open
        """
        # If completed window exists and an item in it is selected # POTENTIAL BUG make sure that the window is selected
        if self.completed_log_window_exists:
            self.completed_log_window.bind("<Button>", self._mouse_click)
            print("In _set_key_bindings completed_log_window_exists")
            current_selection = self.completed_log_window.get_current_selection()
            print(f"Current selection is {current_selection}")
            if current_selection != ():
                print("BINDING CONTROL_R")
                self.completed_log_window.bind('<Control-r>',
                                               lambda event: self._completed_to_todo(current_selection[0]))

    def _set_key_bindings(self):
        """
        Parameter:      None

        Called By:      set_board_data
                        _completed_log_button_clicked
                        _mouse_click

        Calls:          _set_unmap_key_bindings
                        _set_completed_to_todo_bindings - self

                        Listbox.curselection
                        Tk.bind - tkinter

                        get_task_view - MemberInterface

        Modifies:       None

        Return:         None

        Description:    Binds keys depending on the task move case
        """
        # Called by VSS in init as the final tasks for the init method

        # Get mouse clicks to find out if any lists have been clicked
        self.bind("<Button>", self._mouse_click)

        # Depending on the self.task_move_case, the keybindings must be set correctly
        if self.task_move_case == 1:  # A task in the todo backlog is selected
            self._set_unmap_key_bindings()  # First unmap all keys
            self._set_completed_to_todo_bindings()
            current_task_index = self.todo_list_box.curselection()[0]  # Get the task index that is selected
            # Map every member button to get the current task IF their number is clicked on
            # The task will be removed from the todo_list_box
            # And the task will be added to the selected member
            for member_index in range(len(self.member_interfaces)):
                if member_index == 0:
                    # self.bind(str(member_index+1),
                    # lambda event: self._todo_to_member(member_index, current_task_index))
                    self.bind('1', lambda event: self._todo_to_member(0, current_task_index))
                elif member_index == 1:
                    self.bind('2', lambda event: self._todo_to_member(1, current_task_index))
                elif member_index == 2:
                    self.bind('3', lambda event: self._todo_to_member(2, current_task_index))
                elif member_index == 3:
                    self.bind('4', lambda event: self._todo_to_member(3, current_task_index))
                elif member_index == 4:
                    self.bind('5', lambda event: self._todo_to_member(4, current_task_index))
                elif member_index == 5:
                    self.bind('6', lambda event: self._todo_to_member(5, current_task_index))
                elif member_index == 6:
                    self.bind('7', lambda event: self._todo_to_member(6, current_task_index))
                elif member_index == 7:
                    self.bind('8', lambda event: self._todo_to_member(7, current_task_index))
                elif member_index == 8:
                    self.bind('9', lambda event: self._todo_to_member(8, current_task_index))
                elif member_index == 9:
                    self.bind('0', lambda event: self._todo_to_member(9, current_task_index))
        elif self.task_move_case == 2:  # A task in some member is selected
            self._set_unmap_key_bindings()  # First unmap all keys
            self._set_completed_to_todo_bindings()

            self.bind('<Control-d>', self._member_to_complete)

            # Get the member who's task is selected
            member_index_with_selected_task = None
            for member_index in range(len(self.member_interfaces)):
                if self.member_interfaces[member_index].get_task_view().curselection() != ():
                    member_index_with_selected_task = member_index

            # Find the task in that member
            member = self.member_interfaces[member_index_with_selected_task]
            task_index = member.get_task_view().curselection()[0]

            self.bind('<Control-t>', lambda event: self._member_to_todo(member_index_with_selected_task, task_index))

            for member_index in range(len(self.member_interfaces)):
                if member_index == 0 and member_index_with_selected_task != 0:
                    # self.bind(str(member_index+1), lambda event: self._member_to_member(member_index, task_index))
                    self.bind('1', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 0))
                elif member_index == 1 and member_index_with_selected_task != 1:
                    self.bind('2', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 1))
                elif member_index == 2 and member_index_with_selected_task != 2:
                    self.bind('3', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 2))
                elif member_index == 3 and member_index_with_selected_task != 3:
                    self.bind('4', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 3))
                elif member_index == 4 and member_index_with_selected_task != 4:
                    self.bind('5', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 4))
                elif member_index == 5 and member_index_with_selected_task != 5:
                    self.bind('6', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 5))
                elif member_index == 6 and member_index_with_selected_task != 6:
                    self.bind('7', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 6))
                elif member_index == 7 and member_index_with_selected_task != 7:
                    self.bind('8', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 7))
                elif member_index == 8 and member_index_with_selected_task != 8:
                    self.bind('9', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 8))
                elif member_index == 9 and member_index_with_selected_task != 9:
                    self.bind('0', lambda event: self._member_to_member(member_index_with_selected_task, task_index, 9))
        else:  # self.task_move_case == 0 so no task is highlighted
            self._set_unmap_key_bindings()  # First unmap all keys
            self._set_completed_to_todo_bindings()

    def set_message_box(self, window_title, message):
        """
        Parameter:      None

        Called By:      startup - VSS.py

        Calls:          messagebox.showinfo - tkinter

        Modifies:       None

        Return:         None

        Description:    A setter for external use of creating a a message box
        """
        messagebox.showinfo(title=window_title, message=message)

    # END SETTERS ------------------------------------------------------------------------------------------------------

    # GETTERS ----------------------------------------------------------------------------------------------------------
    def get_project_backlog_input(self):
        """
        Parameter:      None

        Called By:      startup - VSS.py

        Calls:          fd.askopenfilename - tkinter

        Modifies:       None

        Return:         None

        Description:    Called to ask the user for a file for the backlog input
        """
        return fd.askopenfilename(
            title='Open a task list text file',
            initialdir='~'
        )

    def get_members_input(self):
        """
        Parameter:      None

        Called By:      startup - VSS.py

        Calls:          fd.askopenfilename - tkinter

        Modifies:       None

        Return:         None

        Description:    Called to ask the user for a file for the member input file
        """
        return fd.askopenfilename(
            title='Open a members list text file',
            initialdir='~'
        )

    def _get_completed_log_as_strings(self):
        """
        Parameter:      None

        Called By:      _completed_log_button_clicked
                        _completed_to_todo
                        _member_to_complete

        Calls:          get_completed() - ScrumbanBoard

        Modifies:       None

        Return:         ["Completed task name Completed on: Data"]: List of strings

        Description:    Returns the list of all the tasks that have been completed in the currently uploaded project.
        """
        completed_list = []
        list_of_completed = self.board_data.get_completed()
        for task in list_of_completed:
            completed_list.append(f"{task.get_name()}  |  Completed on: {task.get_done()}")
        return completed_list
    # END GETTERS ------------------------------------------------------------------------------------------------------

    # EVENT HANDLERS ---------------------------------------------------------------------------------------------------
    def _send_reports_button_clicked(self):
        """
        Parameter:      None

        Called By:      None. It is a handler function binded to a button.

        Calls:          send_reports - VSS

        Modifies:       None

        Return:         None

        Description:    Triggers the code that sends the reports via email.
        """
        self.vss.send_reports()

    def _refresh_todo_button_clicked(self):
        """
        Parameter:      None

        Called By:      _completed_log_button_clicked
                        _completed_to_todo
                        _member_to_complete

        Calls:          get_completed() - ScrumbanBoard

        Modifies:       None

        Return:         None

        Description:    Returns the list of all the tasks that have been completed in the currently uploaded project.
        """
        # Empty the list
        self.todo_list_box.delete(0, END)
        # Get the todos again and fill them
        self.board_data.backlog_to_todo()
        todos = self.board_data.get_todo()
        for todo in todos:
            self.todo_list_box.insert(END, todo.get_name())

        # Update the backlog if it is open
        updated_backlog = []
        for task in self.board_data.get_project_backlog():
            updated_backlog.append(task.get_name())

        if self.project_backlog_window_exists:
            self.project_backlog_window.update_data(updated_backlog)

    def _completed_log_button_clicked(self):
        """
        Parameter:      None

        Called By:      None

        Calls:          _get_completed_log_as_strings
                        _member_to_complete - Self

                        PopOutWindowInterface
                        Toplevel.protocol - Tkinter

        Modifies:       self.completed_log_window
                        self.completed_log_window_exists

        Return:         None

        Description:    Hanlder for when the completed log button is clicked and opens the completed log window
        """
        if self.completed_log_window_exists:
            return

        # Get the list of completed tasks
        completed_list = self._get_completed_log_as_strings()

        self.completed_log_window = PopOutWindowInterface(self, "Completed Log", completed_list)
        self.completed_log_window_exists = True
        self.completed_log_window.protocol("WM_DELETE_WINDOW", lambda: self._on_closing(self.completed_log_window))

        self._set_key_bindings()

    def _maximums_button_clicked(self):
        """
        Parameter:      None

        Called By:      _set_up_button_bar

        Calls:          PopOutWindowInterface
                        topLevel.protocol - Tkinter

        Modifies:       self.maximums_window_exists

        Return:         None

        Description:    This is the handler for if the maximums button is clicked. It creates a window that says what
                        the user-set maximum task and question/concerns values are.
        """
        text_list = [f"Max Todo Tasks: {self.board_data.get_max_todo_size()}",
                     f"Max Member Tasks: {self.board_data.get_task_member_limit()}"]

        if self.maximums_window_exits:
            return

        self.maximums_window = PopOutWindowInterface(self, "Maximums", text_list, width=0, height=0)
        self.maximums_window_exits = True
        self.maximums_window.protocol("WM_DELETE_WINDOW", lambda: self._on_closing(self.maximums_window))

    def _agenda_button_clicked(self):
        """
        Parameter:      None

        Called By:      _set_up_button_bar

        Calls:          PopOutWindowInterface
                        Toplevel.protocol : Tkinter

        Modifies:       self.agenda_window
                        self.agenda_window_exists

        Return:         None

        Description:    Handler if the agenda button is pressed. It creates an agenda window with the user inputted data
        """
        if self.agenda_window_exists:
            return
        self.agenda_window = PopOutWindowInterface(self, "Agenda", self.board_data.get_agenda())
        self.agenda_window_exists = True
        self.agenda_window.protocol("WM_DELETE_WINDOW", lambda: self._on_closing(self.agenda_window))

    def _project_backlog_button_clicked(self):
        """
        Parameter:      None

        Called By:      _set_up_button_bar

        Calls:          PopOutWindowInterface
                        Toplevel.protocol : Tkinter

        Modifies:       self.project_backlog_window
                        self.project_backlog_window_exists

        Return:         None

        Description:    Handler if the project backlog button is pressed. It creates a window with the project backlog.
        """
        if self.project_backlog_window_exists:
            return

        # Get the project backlog string titles in a list
        project_backlog_list = []
        list_of_backlog = self.board_data.get_project_backlog()
        for task in list_of_backlog:
            project_backlog_list.append(task.get_name())
        self.project_backlog_window = PopOutWindowInterface(self, "Project Backlog", project_backlog_list)
        self.project_backlog_window_exists = True
        self.project_backlog_window.protocol("WM_DELETE_WINDOW", lambda: self._on_closing(self.project_backlog_window))

    def _on_closing(self, window):
        """
        Parameter:      None

        Called By:      _completed_log_button_clicked
                        _maximums_button_clicked
                        _agenda_button_clicked
                        _project_backlog_button_clicked

        Calls:          Tk.destroy - Tkinter

        Modifies:       self.completed_log_window_exists
                        self.agenda_window_exists
                        self.maximums_window_exits
                        self.project_backlog_window_exists

        Return:         None

        Description:    Sets the existence of a window boolean value to false when the window is closed
        """
        if window == self.completed_log_window:
            self.completed_log_window_exists = False
        elif window == self.agenda_window:
            self.agenda_window_exists = False
        elif window == self.maximums_window:
            self.maximums_window_exits = False
        else:
            self.project_backlog_window_exists = False

        window.destroy()

    def _mouse_click(self, event):
        """
        Parameter:      event

        Called By:      Called in button handlers when the mouse button is clicked.

        Calls:          get_task_view - Tkinter
                        _set_key_bindings - Self

        Modifies:       self.task_move_case

        Return:         None

        Description:    Used to process a mouse click and determine what task move case the program is on based on the
                        object the user clicks on.

                        Understand this fact: While the program is running, only one task can ever be highlighted.
                        So of all the members task lists and the todo task list only one of the tasks in one of the
                        lists can ever be highlighted
                        Determine what kind of task move is possible based on what task is highlighted
                        return 0 if no move is possible from this state
                        return 1 if you can move a todo task to a members task list
                        return 2 if you can move a member task to completed
        """
        # Define this helper function
        def is_a_member_task_selected(curr_class):
            for curr_member in curr_class.member_interfaces:
                if curr_member.get_task_view().curselection() != ():
                    return True
            return False

        # case that the todo_list_box is clicked
        if self.todo_list_box.curselection() != ():
            #print("A todo_list_box task has been clicked!")
            #print(self.todo_list_box.curselection())
            self.task_move_case = 1  # For _todo_to_member
        elif is_a_member_task_selected(self):  # case that a member is selected
            for member in self.member_interfaces:
                if member.get_task_view().curselection() != ():
                    #print(f"{member} instance's task_view tasks has been selected")
                    self.task_move_case = 2  # For _member_to_complete
        else:  # Case that nothing has been clicked on
            #print("No task is selected")
            self.task_move_case = 0  # No task is selected so case is nothing_is_picked

        self._set_key_bindings()  # reset key bindings

    def _completed_to_todo(self, completed_task_index):
        """
        Parameter:      completed_task_index

        Called By:      Binded to control+t in _set_completed_to_todo_bindings

        Calls:          completed_to_todo - ScrumbanBoard
                        messagebox.showinfo - Tkinter
                        _fill_todo_data - self
                        update_data - PopOutWindowInterface

        Modifies:       None

        Return:         None

        Description:    Moves a task from the compelted list back to the todo list
        """
        print(f"called_completed_to_todo with a completed_task_index of {completed_task_index}")
        if self.board_data.completed_to_todo(completed_task_index) == 1:
            messagebox.showinfo(title="ERROR; Todo has max tasks",
                                message="The todo list cannot take any new tasks because it is at its maximum length")

        # Update the completed list
        self.completed_log_window.update_data(self._get_completed_log_as_strings())
        # Update the todo list
        self._fill_todo_data()

    def _todo_to_member(self, member_index, task_in_todo_index):
        """
        Parameter:      member_index: int that represents the index the member is at in the list of memebrs
                        task_in_todo_index: int that represents hte index the task is at in the todo list

        Called By:      Binded to button presses when an item in the todo list is clicked on in _set_key_bindinds

        Calls:          assign_task - ScrumbanBoard
                        messagebox.showinfo - Tkinter
                        _fill_todo_data - self
                        fill_tasks_data - member interfaces

        Modifies:       None

        Return:         None

        Description:    Moves a task from the todo list to the correct member task list
        """
        # Get the exact instance of the task
        # Remove the task from the todo list and add it to the right member on the data side
        if self.board_data.assign_task(member_index, task_in_todo_index) == 1:
            messagebox.showinfo(title="ERROR: Member has max tasks",
                                message=f"{self.board_data.get_members()[member_index].get_name()} \
                                already has maximum number of tasks")
        # Get the updated todo list items for the GUI
        self._fill_todo_data()
        # Get the updated member instances todo for the GUI
        print(f"in _todo_to_member memberInterface is this long: {len(self.member_interfaces)} \
        and member index is {member_index}")
        self.member_interfaces[member_index].fill_tasks_data()

    def _member_to_todo(self, member_index, task_in_member_index):
        """
        Parameter:      member_index: int that represents the index the member is at in the list of memebrs
                        task_in_todo_index: int that represents the index the task is at in the mmeber's task list

        Called By:      Binded to button presses when an item in the member's task list is clicked in _set_key_bindinds

        Calls:          member_to_todo - ScrumbanBoard
                        messagebox.showinfo - Tkinter
                        _fill_todo_data - self
                        fill_tasks_data - member interfaces

        Modifies:       None

        Return:         None

        Description:    Moves a member's task back to the todo list
        """
        print(member_index)
        if self.board_data.member_to_todo(member_index, task_in_member_index) == 1:
            messagebox.showinfo(title="ERROR: Todo has max tasks",
                                message="The todo list cannot take any new tasks because it is at its maximum length")

        self._fill_todo_data()
        self.member_interfaces[member_index].fill_tasks_data()

    def _member_to_complete(self, event):
        """
        Parameter:      event - implicitly sent event from Tkinter

        Called By:      Binded to button presses when an item in the member's task list is clicked in _set_key_bindinds

        Calls:          complete_task - ScrumbanInterface
                        fill_tasks_data, get_task_view - MemberInterface
                        _get_completed_log_as_strings - Self
                        update_data - PopOutWindowINterface


        Modifies:       None

        Return:         None

        Description:    Moves a task in a member to the completed list. This function finds the selected task in the
                        member.
        """
        # Get the member who's task is selected
        member_index_with_selected_task = None
        for member_index in range(len(self.member_interfaces)):
            if self.member_interfaces[member_index].get_task_view().curselection() != ():
                member_index_with_selected_task = member_index

        # Find the task in that member
        member = self.member_interfaces[member_index_with_selected_task]
        task_index = member.get_task_view().curselection()[0]

        self.board_data.complete_task(member_index_with_selected_task, task_index)

        # Update the view
        member.fill_tasks_data()

        # Update the completed list if it is open
        if self.completed_log_window_exists:
            completed_list = self._get_completed_log_as_strings()
            self.completed_log_window.update_data(completed_list)

    def _member_to_member(self, from_member_index, task_in_member_index, to_member_index):
        """
        Parameter:      from_member_index: integer index
                        task_in_member_index: integer index
                        to_member_index: integer index

        Called By:      Binded to button presses when an item in the member's task list is clicked in _set_key_bindinds

        Calls:          move_member_to_member - ScrumbanBoard
                        messagebox.showinfo - Tkinter
                        fill_tasks_data - MemberInterface

        Modifies:       None

        Return:         None

        Description:    Moves a members task to another member
        """
        # Remove the task from the fromMember and save the task

        if self.board_data.move_member_to_member(from_member_index, to_member_index, task_in_member_index) == 1:
            messagebox.showinfo(title="ERROR: Member has max tasks",
                                message=f"{self.board_data.get_members()[to_member_index].get_name()} \
                                 already has maximum number of tasks")

        # Get the updated member instances todo for the GUI
        self.member_interfaces[from_member_index].fill_tasks_data()
        self.member_interfaces[to_member_index].fill_tasks_data()

    # END EVENT HANDLERS -----------------------------------------------------------------------------------------------

    # FILL DATA --------------------------------------------------------------------------------------------------------
    def _fill_todo_data(self):
        """
        Parameter:      None

        Called By:      set_board_data,
                        _completed_to_todo,
                        _todo_to_member,
                        _member_to_todo

        Calls:          Listbox.delete
                        Listbox.insert - Tkinter

        Modifies:       None

        Return:         None

        Description:    Fills the todo data from what is saved in the Scrumban Board instance.
        """
        # Delete any existing tasks
        self.todo_list_box.delete(0, END)
        # Fill todos
        for task in self.board_data.get_todo():
            self.todo_list_box.insert(END, task.get_name())

    # END FILL DATA ----------------------------------------------------------------------------------------------------

    # SETUP METHODS ----------------------------------------------------------------------------------------------------
    def _set_up_button_bar(self):
        """
        Parameter:      None

        Called By:      __init__ - self

        Calls:          Button,
                        Tk.pack - Tkinter

        Modifies:       self.send_reports_button
                        self.refresh_todo_button
                        self.completed_log_button
                        self.agenda_button
                        self.project_backlog_button
                        self.maximums_button

        Return:         None

        Description:    Instantiates and places the buttons for the button bar and connects them to their handler
                        command functions
        """
        self.button_bar_frame.pack(side=TOP, fill=X)

        # Instantiate and place buttons for the bar
        self.send_reports_button = Button(self.button_bar_frame, text="Send Reports",
                                          command=self._send_reports_button_clicked).pack(side=LEFT)
        self.refresh_todo_button = Button(self.button_bar_frame, text="Refresh Todo",
                                          command=self._refresh_todo_button_clicked).pack(side=RIGHT)
        self.completed_log_button = Button(self.button_bar_frame, text="Show Completed Log",
                                           command=self._completed_log_button_clicked).pack(side=RIGHT)
        self.agenda_button = Button(self.button_bar_frame, text="Show Agenda",
                                    command=self._agenda_button_clicked).pack(side=RIGHT)
        self.project_backlog_button = Button(self.button_bar_frame, text="Show Project Backlog",
                                             command=self._project_backlog_button_clicked).pack(side=RIGHT)
        self.maximums_button = Button(self.button_bar_frame, text="Show Maximums",
                                      command=self._maximums_button_clicked).pack(side=RIGHT)

    def _set_up_below_buttons_frame(self):
        """
        Parameter:      None

        Called By:       __init__ - self

        Calls:          Tk.pack - Tkinter

        Modifies:       None

        Return:         None

        Description:    Sets up the frame that holds everything on the screen below the button bar
        """
        self.below_buttons_frame.pack(side=TOP, fill=BOTH, expand=True)

    def _set_up_todo_and_notes(self):
        """
        Parameter:      None

        Called By:      __init__ - self

        Calls:          Frame
                        Tk.place
                        Label
                        Listbox
                        ScrolledText - Tkinter

        Modifies:       None

        Return:         None

        Description:    Set up all the contents in hte todo and notes frame. So it sets up the todo section and notes
                        section
        """
        self.todo_and_notes_frame.pack(side=RIGHT, fill=Y)

        # PADDING CONSTANTS
        padding = 10

        # Creating the top frame for todos
        todo_frame = Frame(self.todo_and_notes_frame, bg=todo_background_color)
        todo_frame.place(relwidth=1, relheight=0.5)
        notes_todo_label = Label(todo_frame, text="Todo Backlog", font=heading_1_font, bg=todo_background_color)
        notes_todo_label.pack(side=TOP)

        # Create the list of todos
        self.todo_list_box = Listbox(todo_frame, font=task_font)
        self.todo_list_box.pack(side=TOP, fill=BOTH, expand=True, padx=padding, pady=padding)

        # Creating the bottom frame for notes
        notes_frame = Frame(self.todo_and_notes_frame, bg=notes_background_color)
        notes_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
        notes_title_label = Label(notes_frame, text="Meeting Notes", font=heading_1_font, bg=notes_background_color)
        notes_title_label.pack(side=TOP)
        # Create entry box for meeting notes
        self.meeting_notes_scrolled_text = ScrolledText(notes_frame, font=body_font)
        self.meeting_notes_scrolled_text.pack(padx=padding, pady=padding)
        '''
        # TESTING ------------------------------------------------------------------------------------------------------
        for x in range(100):
            self.todo_list_box.insert(END, f"YOUR MOM {x}")
        # END TESTING --------------------------------------------------------------------------------------------------
        '''

    def _set_up_members(self):
        """
        Parameter:      None

        Called By:      __init__ - self

        Calls:          Frame
                        Tk.place
                        Label
                        Scrollbar - Tkinter

        Modifies:       None

        Return:         None

        Description:    Sets up the member section and instantiates the MemberInterfaces
        """
        self.members_frame.pack(side=LEFT, fill=BOTH, expand=True)  # , width=500, height=400)

        members_label = Label(self.members_frame, text="Members", font=heading_1_font, bg=member_background_color)
        members_label.pack(side=TOP, fill=X)  # Fill across the x axis so everything else goes below

        frame_below_members_label = Frame(self.members_frame, bg=member_background_color)
        frame_below_members_label.pack(side=TOP, fill=BOTH, expand=True)
        # Scroll bar: https://stackoverflow.com/questions/5612237/inserting-a-button-into-a-tkinter-listbox-on-python
        frame_container = Frame(frame_below_members_label)
        canvas_container = Canvas(frame_container)
        members_content_frame = Frame(canvas_container)
        # members_scroll_bar will be visible if the members_content_frame is to to big for the canvas
        members_scroll_bar = Scrollbar(frame_container, orient="vertical", command=canvas_container.yview)
        canvas_container.create_window((0, 0), window=members_content_frame, anchor='nw')

        """
        # TESTING ------------------------------------------------------------------------------------------------------
        for number in range(10):
            self.members.append(MemberInterface(members_content_frame, None))
            self.members[number].pack()
        # END TESTING --------------------------------------------------------------------------------------------------
        """

        # INTERFACE WITH DATA SIDE -------------------------------------------------------------------------------------
        # for member_index in range(len(self.members)):
        members = self.board_data.get_members()
        for member_index in range(len(members)):
            self.member_interfaces.append(MemberInterface(members_content_frame, members[member_index], member_index))
        # END INTERFACE WITH DATA SIDE ---------------------------------------------------------------------------------

        # update members_content_frame height so it's no longer 0 ( height is 0 when it has just been created )
        print(f"Before placing everything the window width is {self.winfo_width()}")
        members_content_frame.update()
        print(f"After placing everything the window width is {self.winfo_width()}")
        canvas_container.configure(yscrollcommand=members_scroll_bar.set,
                                   scrollregion="0 0 0 %s" % members_content_frame.winfo_height())
        canvas_container.pack(side=LEFT, fill=BOTH, expand=True)
        members_scroll_bar.pack(side=RIGHT, fill=Y)
        frame_container.pack(fill=BOTH, expand=True)

    def _set_up_menu_bar(self):
        """
        Parameter:      None

        Called By:      None

        Calls:          configure
                        Menu
                        Menu.add_cascate
                        Menu.add_command - Tkinter

        Modifies:       None

        Return:         None

        Description:    Sets up the menu bar and options and connects the options to their event handler functions
        """
        self.menu_bar.configure()  # Add options here to configure the menu_bar

        # Create the import drop down
        import_menu = Menu(self.menu_bar, tearoff=True)
        # Add the import drop down to the menu_bar
        self.menu_bar.add_cascade(label="Options", menu=import_menu)
        # Add options to hte import drop down
        import_menu.add_command(label="Import Agenda", command=self.import_agenda_clicked)
        import_menu.add_command(label="Project Reset", command=self.project_reset_clicked)

    def import_agenda_clicked(self):
        """
        Parameter:      None

        Called By:      Event handler for import agenda button in _set_up_menu_bar

        Calls:          set_agenda_path
                        load_agenda
                        set_agenda - ScrumbanHistory

        Modifies:       None

        Return:         None

        Description:    Event handler that imports new agendas when it is clicked
        """
        # THIS IS THE MOST COUPLED FUNCTION. IT ACCESSES VSS, HISTORY, AND BOARD
        file_path = fd.askopenfilename(title='Open an agenda text file', initialdir='~')

        self.vss.history.set_agenda_path(file_path)
        self.vss.history.load_agenda()
        self.vss.board.set_agenda(self.vss.history.get_agenda())

    def project_reset_clicked(self):
        """
        Parameter:      None

        Called By:      Event handler for resetting the program button in _set_up_menu_bar

        Calls:          reset_system
                        ScrumbanHistory
                        exit - sys

        Modifies:       None

        Return:         None

        Description:    Event handler that resets the program so the user can import a new project
        """
        are_they_sure = askyesno("Are you sure?", "Are you sure you want to reset the project. All current project \
        DATA WILL BE LOST. SYSTEM WILL QUIT. Restart to re-import data")
        if are_they_sure:
            self.vss.history.reset_system()
            sys.exit()

    # END SETUP METHODS ------------------------------------------------------------------------------------------------


# ******************************************************************************************************************** #


class PopOutWindowInterface(Toplevel):
    """
    Outlines the structure for pop-out window interface. It can display any list of data as strings

    Used by:
        ScrumbanInterface

    Members:
        Member Name:                : Type              : Default Val           -> Description
        ----------------------------------------------------------------------------------------------------------------
        self.items_list             : [str]             : items_list            -> List of the items that will fill the
                                                                                listbox

        self.master_window          : Tk                : master_window         -> The main Tk window

        self.top_frame              : Frame             : Frame()               -> The most high-level frame in the win

        self.label                  : Label             : Label()               -> The label with the title of the win

        self.items_list_widget      : Listbox           : Listbox()             -> The list that holds all the data

    Methods:
        Public:                                                                      Return:
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    get_current_selection(self)                                 |   -> output is a tuple
                                                                                    |   that looks like this (5, )
                                                                                    |
        Usage:          instance.get_current_selection()                            |
                                                                                    |
        Description:    Returns the location in the list that is selected           |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    update_data(self, completed_list)                           |   -> None
                                                                                    |
        Usage:          instance.update_data(list_of_data_as_strings)               |
                                                                                    |
        Description:    Takes an updated version of the data list and fills the list|
        ----------------------------------------------------------------------------|-----------------------------------
    """
    def __init__(self, master_window, window_title: str, items_list: [str], width=350, height=700):
        """
        Parameter:      master_window - A Scrumban Interface window,
                        window_title - A title for the top of the window
                        items_list - The data that fills the data
                        width - Setable window size with a default
                        height - Setable window size with a default

        Called By:      None

        Calls:          Toplevel.minsize
                        Toplevel.group
                        Frame.pack
                        Label.pack
                        Toplevel.update_data - Tkinter

        Modifies:       None

        Return:         None

        Description:    Sets up the PopoutwindowInterface
        """
        super().__init__()

        # Width then height
        self.minsize(width, height)

        self.items_list = items_list

        # Adds the window to the window group administered by the given window. (ie. ScrumbanInterface)
        self.master_window = master_window
        self.group(self.master_window)

        # High level frame
        self.top_frame = Frame(self)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=True)

        # Title Label
        self.label = Label(self.top_frame, text=window_title, font=heading_1_font)
        self.label.pack(side=TOP, fill=X, expand=False)

        # Display list of items
        self.items_list_widget = Listbox(self.top_frame, font=body_font)
        self.items_list_widget.pack(fill=BOTH, expand=True)

        self.update_data(self.items_list)

    def get_current_selection(self):
        """
        Parameter:      None

        Called By:      None

        Calls:          tk.curselection - Tkinter

        Modifies:       None

        Return:         None

        Description:    Public method to get the current selection index in a tuple like this (1, ) if the selected
                        index 1
        """
        return self.items_list_widget.curselection()

    def update_data(self, completed_list):
        """
        Parameter:      completed_list is a list strings

        Called By:      _completed_to_todo
                        _member_to_complete - Scrumban Interface
                        Listbox.insert - Tkinter

        Calls:          None

        Modifies:       None

        Return:         None

        Description:    Updates the data stored in the poopout window
        """
        # First empty the view
        self.items_list_widget.delete(0, END)

        # update the items_list
        self.items_list = completed_list

        # Refill it with updated data
        for item in self.items_list:
            self.items_list_widget.insert(END, item)


# ******************************************************************************************************************** #


class MemberInterface(Frame):
    """
    Outlines the structure for the member interface widget that goes in the ScrumbanInterface Tk window.

    Used by:
        ScrumbanInterface

    Members:
        Member Name:                : Type              : Default Val           -> Description
        ----------------------------------------------------------------------------------------------------------------
        self.member_data            : ScrumbanMember    : member_data           -> Holds an instance of ScrumbanMember
                                                                                which is used for getting data to the UI

        self.name_label             : Label             : Label()               -> Holds the label that has the name of
                                                                                the member

        self.tasks_frame            : Frame             : Frame()               -> The frame for the tasks

        self.task_label_frame       : Frame             : Frame()               -> Frame that just holds the task label

        self.task_label             : Label             : Label()               -> The label that says "tasks"

        self.task_view              : Listbox           : Listbox()             -> Holds the listbox that has the names
                                                                                of the tasks for the member

        self.questions_concerns_fram: Frame             : Frame()               -> Holds the questions/concerns frame
                                   e

        self.questions_concerns_labe: Frame             : Frame()               -> Frame that just holds the q and c
                             l_frame                                            label

        self.questions_concerns_labe: Label             : Label()               -> Label for questions and concerns
                                   l

        self.questions_concerns_entr: ScrolledText      : ScrolledText()        -> Holds the questions/concerns text box
                                   y

        self.questions_concerns_text: string            : None                  -> Hold the text that is being typed as
                                                                                a string

    Methods:
        Private:                                                                     Return:
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    _fill_questions_concerns_data(self)                         |   -> None
                                                                                    |
        Usage:          instance._fill_questions_concerns_data()                    |
                                                                                    |
        Description:    Fills the questions and concerns box with saved text        |
        ----------------------------------------------------------------------------|-----------------------------------

        Public:                                                                      Return:
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    get_task_view(self)                                         |   -> self.task_view
                                                                                    |
        Usage:          instance.get_task_view()                                    |
                                                                                    |
        Description:    Gets the task view which is a listbox with the task names   |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    get_questions_concerns_text(self)                           |   -> String of questions
                                                                                    |      concerns text
        Usage:          instance.get_questions_concerns_text()                      |
                                                                                    |
        Description:    Gets the questions and concerns text and returns them as a  |
                        string                                                      |
        ----------------------------------------------------------------------------|-----------------------------------
        Declaration:    fill_tasks_data(self)                                       |   -> None
                                                                                    |
        Usage:          instance.fill_tasks_data()                                  |
                                                                                    |
        Description:    Gets up to data data to fill the member's tasks             |
        ----------------------------------------------------------------------------|-----------------------------------
    """
    def __init__(self, parent: ScrumbanInterface, member_data, member_index):
        """
        Parameter:      parent is an instance of ScrumbanInterface
                        member_data is ScrumbanMembers
                        member_index and intereger value that returns the index of the member in the member list in the
                        interface

        Called By:      None

        Calls:          A lot of Tkinter methods.

        Modifies:       None

        Return:         None

        Description:    Initializes the member interface.
        """
        Frame.__init__(self, parent, bg='#ab1239')
        self.pack(side=TOP, fill=BOTH, expand=True)

        self.user_member_identifier = f"{member_index + 1}"
        if member_index == 9:
            self.user_member_identifier = "-"

        self.member_data = member_data

        # Create and place name label
        self.name_label = Label(self, text=f"{self.member_data.get_name()} {self.user_member_identifier}",
                                font=heading_2_font, bg=member_background_color)
        self.name_label.pack(side=TOP, fill=X, expand=True)

        # Create frame for Tasks
        self.tasks_frame = Frame(self, bg=member_background_color)  # height = 200
        self.tasks_frame.pack(side=TOP, fill=X, expand=True)
        # Create label for Tasks
        self.task_label_frame = Frame(self.tasks_frame, width=10, bg=member_background_color)
        self.task_label_frame.pack(side=LEFT, padx=55, fill=Y)
        self.task_label = Label(self.task_label_frame, text="Tasks", font=heading_2_font, bg=member_background_color)
        self.task_label.pack(side=TOP)
        # Create the task list
        self.task_view = Listbox(self.tasks_frame, font=task_font)  # width=200
        self.task_view.pack(side=LEFT, padx=1, pady=1, fill=X, expand=True)

        # Create frame for Questions/Concerns
        self.questions_concerns_frame = Frame(self, bg=member_background_color)  # height=100)
        self.questions_concerns_frame.pack(side=TOP, fill=BOTH, expand=True)
        # Create label for Questions/Concerns: Must create a frame to contain it so the label can go at the top of frame
        self.questions_concerns_label_frame = Frame(self.questions_concerns_frame, bg=member_background_color)
        self.questions_concerns_label_frame.pack(side=LEFT, fill=Y, expand=True)
        self.questions_concerns_label = Label(self.questions_concerns_label_frame, text="Questions & Concerns",
                                              font=heading_2_font, bg=member_background_color)
        self.questions_concerns_label.pack(side=TOP)

        # Create the questions and concerns text entry box
        self.questions_concerns_entry = ScrolledText(self.questions_concerns_frame, font=body_font, width=60,
                                                     height=10)
        self.questions_concerns_entry.pack(side=LEFT, padx=1, pady=1) #fill=BOTH, expand=True)

        self.questions_and_concerns_text = None

        self.break_bar = Frame(self, bg="#000000", height=5)
        self.break_bar.pack(side=BOTTOM, fill=X)

        self.fill_tasks_data()
        self._fill_questions_concerns_data()

    def get_task_view(self):
        """
        Parameter:      None

        Called By:      _set_key_bindings
                        _mouse_click
                        _member_to_complete

        Calls:          None

        Modifies:       None

        Return:         The task view which allows access to the tasks of the member

        Description:    Provides access to the members task data
        """
        return self.task_view

    def get_questions_concerns_text(self):
        """
        Parameter:      None

        Called By:      _save_text - ScrumbanInterface

        Calls:          ScrolledText.get - Tkinter

        Modifies:       None

        Return:         _save_text

        Description:    Provides access to the questions and concerns text
        """
        return self.questions_concerns_entry.get("1.0", END)

    def fill_tasks_data(self):
        """
        Parameter:      None

        Called By:      _todo_to_member
                        _member_to_todo
                        _member_to_complete
                        _member_to_member

        Calls:          task_view - self

        Modifies:       None

        Return:         None

        Description:    Fills in the task data for the member
        """
        # First, empty the tasks
        self.task_view.delete(0, END)

        print("FILLING TASK DATA")

        # Fill the tasks
        for task in self.member_data.get_tasks():
            task_name = task.get_name()
            self.task_view.insert(END, task_name)

    def _fill_questions_concerns_data(self):
        """
        Parameter:      None

        Called By:      __init__ - Member Interfaces

        Calls:          ScrolledText.insert - Tkinter

        Modifies:       self.questions_and_concerns_text

        Return:         None

        Description:    Fills the questions and concerns text data
        """
        # Fill the questions/concerns
        self.questions_and_concerns_text = self.member_data.get_qc()
        self.questions_concerns_entry.insert(END, self.questions_and_concerns_text)
        """
        # TEST DATA ----------------------------------------------------------------------------------------------------
        # Test the questions_concerns_entry box
        self.questions_concerns_entry.insert(END, "This is testing if filling works")
       
        # FIll in the tasks with various example tasks
        self.task_view.insert(END, "JD Paul")
        self.task_view.insert(END, "Nick Johnstone")
        # END TEST DATA ------------------------------------------------------------------------------------------------
        """
# ******************************************************************************************************************** #


if __name__ == '__main__':
    # Test Scrumban Interface
    '''
    testScrumbanInterface = ScrumbanInterface()
    testScrumbanInterface.mainloop()

    # TEST FOR A MEMBER
    root = Tk()
    member = MemberInterface(root, None)
    member.pack()
    member2 = MemberInterface(root, None)
    member3 = MemberInterface(root, None)
    member4 = MemberInterface(root, None)

    member.grid(row=0, column=0)
    member2(row=0, column=1)
    member3(row=1, column=0)
    member4(row=1, column=1)
    root.mainloop()
    '''
