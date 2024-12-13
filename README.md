# Tasker
A terminal-based task manager application with a calendar interface, built using Python's `curses` module. This app allows users to view a monthly calendar, navigate through dates, and manage tasks for specific days.

## Features

- **Interactive Calendar**: Navigate through days using arrow keys.
- **Task Management**: Add and delete tasks for specific dates.
- **Persistent Storage**: Tasks are saved in a JSON file and persist across sessions.
- **Keyboard Controls**:
  - Arrow keys: Navigate the calendar.
  - Enter: View and manage tasks for a selected day.
  - `a`: Add a task.
  - `d`: Delete a task.
  - `L`: List all task
  - `b`: Go back to the calendar.
  - `q`: Quit the application.

## Installation

Clone the repository:
   ```bash
   git clone https://github.com/Trabbit0ne/Tasker.git
   cd Tasker
   ```

## Usage

Run the application using:
```bash
python3 tasker.py
```
Alias
```bash
echo 'alias agenda="python3 ~/Tasker/tasker.py"' >> ~/.bash_profile
```

### Controls
- **Arrow Keys**: Navigate through the calendar.
- **Enter**: Select a day to view or edit tasks.
- **`a`**: Add a new task.
- **`d`**: Delete an existing task.
- **`b`**: Go back to the calendar view.
- **`q`**: Quit the application.

## File Structure

- `tasker.py`: Main application script.
- `tasks.json`: JSON file to store tasks (created automatically on first run).

**Author**: Trabbit0ne
