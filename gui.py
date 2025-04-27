import threading
from tkinter import *
from PIL import Image, ImageTk, ImageSequence

shutdown_event = threading.Event()


def play_gif():
    root = Tk()
    root.geometry("1280x1280")  # Adjust dimensions as necessary

    # Ensure the window is always on top
    root.attributes("-topmost", True)

    img = Image.open("jarvis.gif")
    frames = [ImageTk.PhotoImage(frame.resize((1280, 1280))) for frame in ImageSequence.Iterator(img)]

    lbl = Label(root)
    lbl.place(x=0, y=0)

    def update_frame(frame_index=0):
        if shutdown_event.is_set():
            root.quit()
            return

        frame = frames[frame_index]
        lbl.config(image=frame)
        root.update_idletasks()
        root.update()

        frame_index = (frame_index + 1) % len(frames)
        root.after(50, update_frame, frame_index)

    # Start the GIF animation
    update_frame()

    # Debugging: Print to confirm that the window is starting
    print("GIF window should be visible now.")

    # Start the Tkinter main loop
    root.mainloop()


def start_gif():
    shutdown_event.clear()
    gif_thread = threading.Thread(target=play_gif)
    gif_thread.start()


def stop_gif():
    shutdown_event.set()
