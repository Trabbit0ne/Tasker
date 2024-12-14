import curses
import calendar
import json
from datetime import datetime

# Constants
TASK_FILE = "tasks.json"
HEADER_COLOR = 1
DAY_COLOR = 2
SELECTED_DAY_COLOR = 3
ACTION_COLOR = 4
SELECTED_MONTH_COLOR = 5

# Utility Functions
def load_tasks():
    """Load tasks from the JSON file."""
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file)

def setup_colors():
    """Initialize color pairs for the interface."""
    curses.start_color()
    curses.init_pair(HEADER_COLOR, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header
    curses.init_pair(DAY_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Days
    curses.init_pair(SELECTED_DAY_COLOR, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Selected Day
    curses.init_pair(ACTION_COLOR, curses.COLOR_WHITE, curses.COLOR_RED)  # Actions
    curses.init_pair(SELECTED_MONTH_COLOR, curses.COLOR_WHITE, curses.COLOR_CYAN)  # Selected Month

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
    instructions = "Use arrow keys to navigate, Enter to select a day, 'q' to quit, 'L' to list tasks."
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

def list_month_tasks(stdscr, year, month, tasks):
    """List all tasks for the selected month in a single-line format per day."""
    stdscr.clear()
    setup_colors()

    # Display header
    month_name = calendar.month_name[month]
    header_text = f"Tasks for {month_name} {year}:"
    stdscr.addstr(0, 0, header_text, curses.color_pair(HEADER_COLOR) | curses.A_BOLD)

    # Initialize row index for task display
    row_idx = 2
    tasks_found = False

    # Iterate through all days in the month
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        date_key = f"{year}-{month:02}-{day:02}"
        task_list = tasks.get(date_key, [])
        if task_list:
            tasks_found = True
            # Combine tasks into a single line with the day
            tasks_text = " - " + " - ".join(task_list)
            stdscr.addstr(row_idx, 0, f"{day:02}{tasks_text}", curses.color_pair(DAY_COLOR))
            row_idx += 1

    if not tasks_found:
        stdscr.addstr(row_idx, 0, "No tasks for this month.", curses.color_pair(DAY_COLOR))

    # Display options
    stdscr.addstr(row_idx + 2, 0, "Press any key to go back.", curses.color_pair(ACTION_COLOR))
    stdscr.refresh()

    # Wait for key press to go back
    stdscr.getch()

def draw_month_selection(stdscr, selected_month):
    """Render the month selection interface."""
    stdscr.clear()
    setup_colors()

    # Display header
    header_text = "*** Select Month ***"
    stdscr.addstr(0, 0, header_text, curses.color_pair(HEADER_COLOR) | curses.A_BOLD)

    # Display months in a grid (3x4 layout)
    months = list(calendar.month_name[1:])
    rows, cols = 3, 4  # Display months in a 3x4 grid
    for i in range(rows):
        for j in range(cols):
            month_idx = i * cols + j
            if month_idx < len(months):
                month_name = months[month_idx]
                color = curses.color_pair(DAY_COLOR)
                if month_idx == selected_month:
                    color = curses.color_pair(SELECTED_MONTH_COLOR)
                stdscr.addstr(i + 2, j * 20 + 2, f"{month_name}", color | curses.A_BOLD)

    # Display instructions
    instructions = "Use arrow keys to select a month, Enter to confirm, 'q' to quit."
    stdscr.addstr(8, 0, instructions, curses.A_DIM)
    stdscr.refresh()

def main(stdscr):
    """Main application loop."""
    curses.curs_set(0)
    setup_colors()

    # Initialize state
    now = datetime.now()
    current_year = now.year
    selected_month = 0  # Start with January
    tasks = load_tasks()

    while True:
        draw_month_selection(stdscr, selected_month)

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_DOWN:
            if selected_month < 8:  # Stay within the 3x4 grid (9 months max in the grid)
                selected_month += 4
        elif key == curses.KEY_UP:
            if selected_month >= 4:
                selected_month -= 4
        elif key == curses.KEY_RIGHT:
            if selected_month % 4 < 3:  # Avoid moving out of bounds in the grid
                selected_month += 1
        elif key == curses.KEY_LEFT:
            if selected_month % 4 > 0:
                selected_month -= 1
        elif key in (curses.KEY_ENTER, 10, 13):
            # Confirm the selected month
            current_month = selected_month + 1  # Set current month to selected month
            selected_day = 1  # Start on the first day of the month

            # Loop for calendar and task management
            while True:
                draw_calendar(stdscr, current_month, current_year, selected_day)

                key = stdscr.getch()
                if key == ord('q'):
                    break
                elif key == ord('L'):
                    list_month_tasks(stdscr, current_year, current_month, tasks)
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
