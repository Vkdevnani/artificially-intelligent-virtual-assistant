import matplotlib.pyplot as plt

def focus_graph():
    durations = []

    # Read focus durations from the focus.txt file
    try:
        with open("focus.txt", "r") as file:
            for line in file:
                # Parse and convert focus duration from "minutes\n" to float
                line = line.strip()
                if "minutes" in line:
                    duration = line.replace(" minutes", "")
                    if duration:  # Check if duration is not empty
                        durations.append(float(duration))
    except FileNotFoundError:
        print("No focus data found. Run focus mode first to generate data.")
        return

    # Plot the focus durations
    if durations:
        plt.figure(figsize=(10, 5))
        plt.plot(durations, marker="o", color="b", linestyle="-", linewidth=2)
        plt.title("Focus Duration Over Time")
        plt.xlabel("Focus Sessions")
        plt.ylabel("Duration (minutes)")
        plt.grid(True)
        plt.show()
    else:
        print("No focus data available for plotting.")

# Run the focus graph function to display the plot
focus_graph()
