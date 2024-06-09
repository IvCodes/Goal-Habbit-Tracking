Goal Tracker Application
Overview

The Goal Tracker Application is a simple yet powerful tool designed to help you set, manage, and achieve your goals. Built with Python and Tkinter, this desktop application provides an intuitive user interface to track your progress and stay motivated.
Features

    Set and Edit Goals: Easily create new goals or edit existing ones. Specify the goal description and the number of days to complete it.
    Track Progress: Monitor your daily progress towards each goal. Mark each day as completed to visually track your advancement.
    Completion Tracking: The application automatically saves your progress and keeps a history of completed goals.
    User-Friendly Interface: A clean and intuitive UI with scrollable lists to handle multiple goals effectively.
    Persistent Storage: Saves your goals and progress to JSON files, ensuring your data is retained between sessions.

How to Use

    Set a New Goal: Click the "Set New Goal" button, enter the goal description and the number of days, and save it.
    Track Daily Progress: Each day, open the application and mark the day's checkbox for each goal you are working on.
    Edit or Delete Goals: You can edit or delete any goal at any time by clicking the corresponding buttons.
    View Completed Goals: Once a goal is completed, it is automatically moved to a history file for your reference.

Installation

To run the Goal Tracker Application, ensure you have Python installed on your machine. Then follow these steps:

    Clone the repository:

    sh

git clone https://github.com/yourusername/goal-tracker.git

Navigate to the project directory:

sh

cd goal-tracker

Run the application:

sh

    python goal_tracker.py

Dependencies

    tkinter: Used for creating the graphical user interface.
    datetime: Used for handling date and time calculations.
    os: Used for file operations.
    json: Used for reading and writing JSON data files.

Future Enhancements

    Progress Bars: Visual progress bars for each goal to give a clearer view of progress.
    Goal Categories: Allow categorization of goals for better organization.
    Notifications: Add notifications to remind users to update their progress.
    Detailed Reports: Generate detailed reports of progress and completed goals.

Contribution

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.
License

This project is licensed under the MIT License.
