import os
import curses
import calendar
import json
from datetime import datetime

# Constants
TASK_FILE = os.path.expanduser("~/.agenda/tasks.json")  # Save in a specific directory
HEADER_COLOR = 1
DAY_COLOR = 2
SELECTED_DAY_COLOR = 3
ACTION_COLOR = 4

# Utility Functions
def ensure_task_file_directory():
    """Ensure the tasks directory exists."""
    directory = os.path.dirname(TASK_FILE)
    os.makedirs(directory, exist_ok=True)

def load_tasks():
    """Load tasks from the JSON file."""
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    ensure_task_file_directory()  # Ensure the directory exists
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def setup_colors():
    """Initialize color pairs for the interface."""
    curses.start_color()
    curses.init_pair(HEADER_COLOR, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header
    curses.init_pair(DAY_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Days
    curses.init_pair(SELECTED_DAY_COLOR, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Selected Day
    curses.init_pair(ACTION_COLOR, curses.COLOR_WHITE, curses.COLOR_RED)  # Actions

def draw_calendar(stdscr, month, year, selected_day):
    """Render the calendar view."""
    stdscr.clear()
    setup_colors()

    # Display header
    month_name = calendar.month_name[month]
    header_text = f"*** {month_name} {year} ***"
    stdscr.addstr(0, 0, header_text, curses.color_pair(HEADER_COLOR) | curses.A_BOLD)

    # Display day headers
    headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, header in enumerate(headers):
        stdscr.addstr(2, i * 4 + 2, header, curses.A_BOLD)

    # Display days of the month
    cal = calendar.monthcalendar(year, month)
    for row_idx, week in enumerate(cal):
        for col_idx, day in enumerate(week):
            if day != 0:
                color = curses.color_pair(DAY_COLOR)
                if day == selected_day:
                    color = curses.color_pair(SELECTED_DAY_COLOR)
                stdscr.addstr(3 + row_idx, col_idx * 4 + 2, f"{day:2}", color)
            else:
                stdscr.addstr(3 + row_idx, col_idx * 4 + 2, "  ")

    # Display instructions
    instructions = "Use arrow keys to navigate, Enter to select a day, 'q' to quit."
    stdscr.addstr(10, 0, instructions, curses.A_DIM)
    stdscr.refresh()

def task_window(stdscr, year, month, day, tasks):
    """Handle task management for a specific day."""
    while True:
        stdscr.clear()
        setup_colors()

        # Display header
        date_str = f"{day:02}/{month:02}/{year}"
        stdscr.addstr(0, 0, f"Tasks for {date_str}:", curses.color_pair(HEADER_COLOR) | curses.A_BOLD)

        # Display tasks
        task_list = tasks.get(f"{year}-{month:02}-{day:02}", [])
        for idx, task in enumerate(task_list):
            stdscr.addstr(2 + idx, 0, f"{idx + 1}. {task}")

        # Display options
        options = "Press 'a' to add a task, 'd' to delete a task, or 'b' to go back."
        stdscr.addstr(4 + len(task_list), 0, options, curses.color_pair(ACTION_COLOR))

        key = stdscr.getch()
        if key == ord('b'):
            break
        elif key == ord('a'):
            # Add task
            stdscr.addstr(6 + len(task_list), 0, "Enter new task: ", curses.color_pair(ACTION_COLOR))
            curses.echo()
            new_task = stdscr.getstr(6 + len(task_list), 15, 60).decode("utf-8")
            curses.noecho()
            if new_task:
                tasks.setdefault(f"{year}-{month:02}-{day:02}", []).append(new_task)
                save_tasks(tasks)
        elif key == ord('d'):
            # Delete task
            if task_list:
                stdscr.addstr(6 + len(task_list), 0, "Enter task number to delete: ", curses.color_pair(ACTION_COLOR))
                curses.echo()
                try:
                    task_num = int(stdscr.getstr(6 + len(task_list), 30, 2).decode("utf-8")) - 1
                    if 0 <= task_num < len(task_list):
                        del task_list[task_num]
                        if not task_list:
                            tasks.pop(f"{year}-{month:02}-{day:02}")
                        save_tasks(tasks)
                except ValueError:
                    pass
                curses.noecho()
        stdscr.refresh()

def main(stdscr):
    """Main application loop."""
    curses.curs_set(0)
    setup_colors()

    # Initialize state
    now = datetime.now()
    current_year, current_month, selected_day = now.year, now.month, now.day
    tasks = load_tasks()

    while True:
        draw_calendar(stdscr, current_month, current_year, selected_day)

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_RIGHT:
            if selected_day < calendar.monthrange(current_year, current_month)[1]:
                selected_day += 1
        elif key == curses.KEY_LEFT:
            if selected_day > 1:
                selected_day -= 1
        elif key == curses.KEY_UP:
            selected_day = max(1, selected_day - 7)
        elif key == curses.KEY_DOWN:
            max_day = calendar.monthrange(current_year, current_month)[1]
            selected_day = min(max_day, selected_day + 7)
        elif key in (curses.KEY_ENTER, 10, 13):
            task_window(stdscr, current_year, current_month, selected_day, tasks)

if __name__ == "__main__":
    curses.wrapper(main)
