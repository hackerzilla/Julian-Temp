# Virtual_Scrumban_System

## Description of the System

The Virtual Scrumban System is an implementation of the Scrumban software devolpment workflow.

## Authors

Sam Gebhardt, Jaeger Jochimsen, Nick Johnstone, JD Paul

## Date of Creation

2/14/2022

## Why It was Created

This system was created for CIS 422 Software Methodologies at the University of Oregon taught by Professor Anthony Hornof. 

## Install Instructions
1. Clone Cold Call System: `git clone https://github.com/superNick459/Virtual_Scrumban_System.git`
## Operation Instructions
### Initial Setup
Create a list of team members for the project.  
Create a project backlog that is comprised with the list of tasks that must be completed for the project. 

 **Team Member File Requirements:**  
 The file must be a text file (.txt) that adheres to the following format:  
 `<Team Member Name><comma><Team Member Email Address>`  

**Project Backlog File Requirements:**  
The file must be a text file (.txt) that adheres to the following format:  
 `<Task Name><comma><Task Priority><comma><Task Due Date>`  
  (see User Documentation/Manual for more)
### Starting the System for the First Time
1. From terminal, navigate to the Virtual_Scrumban_System directory.
2. Execute the program `python3 VSS.py`.  
3. Select an initial project backlog via the file navigation window.  
4. Select a member file via the file navigation window.  
5. Enter the max todo size and max number of tasks per member in the pop up window.
6. The system is now ready to use.  

### Subsequent System Usage (Same Project)  
1. From terminal, navigate to Virtual_Scrumban_System directory.  
2. Execute the program `python3 VSS.py`.  

### Subsequent System Usage (Resetting System)  
1. Start the system.  
2. Under `Options` select `Reset Project`.
3. Select `Yes`.
4. The system is now ready for a new project.
 
### System Controls
| Keystroke       | Description    |
|-----------------|----------------|
| Ctrl t | Unassign task for a Member |
| Ctrl d | Mark a task as completed  |
| Ctrl r | Move a task from completed to todo |
| Number Keys | Move a task from a backlog to a member |

### Resetting the System
Click the "Reset" button on the right side of the top bar to reset the current project.
## Dependencies
The Cold Call Assist System relies on:
1. [python3.7](https://www.python.org/downloads/) 
2. tkinter 
3. smtplib

## File Manifest
*Software Files*
1. ScrumbanBoard.py
2. ScrumbanHistory.py
3. ScrumbanInterface.py
4. ScrumbanMember.py
5. VSS.py

*Documentation*
1. SRS.pdf
2. SDS.pdf
3. Project_Plan.pdf
4. README.txt
5. Programmer_Documentation.pdf or .txt
6. Installation_Instructions.pdf or .txt
7. User_Manual.pdf
8. User_Observations.pdf

## Credits
1. **"Software Engineering 10th Edition" Ian Sommerville:** UML reference and general Software methods.
2. **Dr. Anthony Hornof:** initial SRS and project consultation.

