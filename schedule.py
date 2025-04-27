# schedule_tasks.py

def add_tasks_to_file(tasks, filename="tasks.txt"):
    """Append tasks to the tasks file."""
    with open(filename, "a") as file:
        for i, task in enumerate(tasks):
            file.write(f"{i + 1}. {task}\n")


def handle_task_input(takeCommand, word_to_number, speak):
    """Handle the input of tasks from the user."""
    tasks = []
    speak("How many tasks do you want to add?")
    no_tasks_word = takeCommand().lower()
    no_tasks = word_to_number(no_tasks_word)
    if no_tasks is not None:
        for i in range(no_tasks):
            speak(f"Enter task {i + 1}")
            task = takeCommand()
            tasks.append(task)
        return tasks
    else:
        speak("Sorry, I did not understand the number of tasks.")
        return []


def schedule_my_day(takeCommand, word_to_number, speak):
    """Schedule tasks for the day."""
    speak("Do you want to clear old tasks? Please say YES or NO.")
    response = takeCommand().lower()
    if "yes" in response:
        with open("tasks.txt", "w") as file:
            pass  # Just clear the file
    elif "no" not in response:
        speak("Sorry, I did not understand your response.")
        return

    tasks = handle_task_input(takeCommand, word_to_number, speak)
    if tasks:
        add_tasks_to_file(tasks)
        speak("Tasks have been added to your schedule.")
