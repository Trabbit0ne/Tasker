# Tgenda
## Task Manager with Calendar Interface

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
  - `b`: Go back to the calendar.
  - `q`: Quit the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Trabbit0ne/Tgnda.git
   cd Tgnda
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

> **Note:** The `curses` module is part of Python's standard library and does not require installation. However, it is not available on Windows by default. Windows users may need to install a compatible library like `windows-curses`:
   ```bash
   pip install windows-curses
   ```

## Usage

Run the application using:
```bash
python task_calendar.py
```

### Controls
- **Arrow Keys**: Navigate through the calendar.
- **Enter**: Select a day to view or edit tasks.
- **`a`**: Add a new task.
- **`d`**: Delete an existing task.
- **`b`**: Go back to the calendar view.
- **`q`**: Quit the application.

## File Structure

- `tgnda.py`: Main application script.
- `tasks.json`: JSON file to store tasks (created automatically on first run).
- `requirements.txt`: List of dependencies.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

**Author**: Trabbit0ne
