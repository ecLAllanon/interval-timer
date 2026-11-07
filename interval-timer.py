import sys
import os
import tkinter as tk
from tkinter import messagebox

# Platform-specific audio setup
if sys.platform == "win32":
    import winsound
    def play_beeps():
        # Frequency (Hz), Duration (ms)
        winsound.Beep(1000, 150)
        winsound.Beep(1000, 150)
else:
    def play_beeps():
        # Fallback using system bell / standard output for Linux/Mac
        for _ in range(2):
            sys.stdout.write('\a')
            sys.stdout.flush()
            os.system('sleep 0.15')

class InfiniteIntervalTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Interval Timer")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.remaining_seconds = 0
        self.interval_seconds = 0
        self.timer_job = None
        self.is_running = False

        # Input Frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=15)

        tk.Label(input_frame, text="Interval (minutes):", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.entry_minutes = tk.Entry(input_frame, width=8, font=("Arial", 10))
        self.entry_minutes.pack(side=tk.LEFT)
        # Default value set to 7
        self.entry_minutes.insert(0, "7")

        # Display Label
        self.label_display = tk.Label(root, text="07:00", font=("Arial", 32, "bold"))
        self.label_display.pack(pady=10)

        # Toggle Button
        self.btn_toggle = tk.Button(
            root, text="Start", font=("Arial", 11, "bold"), 
            width=10, command=self.toggle_timer, bg="#4CAF50", fg="white"
        )
        self.btn_toggle.pack(pady=10)

    def toggle_timer(self):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        try:
            minutes = float(self.entry_minutes.get())
            if minutes <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive number.")
            return

        self.interval_seconds = int(minutes * 60)
        self.remaining_seconds = self.interval_seconds
        self.is_running = True
        
        # Lock input field while running
        self.entry_minutes.config(state="disabled")
        self.btn_toggle.config(text="Stop", bg="#f44336")
        
        self.update_clock()

    def stop_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.is_running = False
        self.entry_minutes.config(state="normal")
        self.btn_toggle.config(text="Start", bg="#4CAF50")
        
        # Reset display to initial value in entry field
        try:
            minutes = float(self.entry_minutes.get())
            mins, secs = divmod(int(minutes * 60), 60)
            self.label_display.config(text=f"{mins:02d}:{secs:02d}")
        except ValueError:
            self.label_display.config(text="07:00")

    def update_clock(self):
        if self.remaining_seconds > 0:
            mins, secs = divmod(self.remaining_seconds, 60)
            self.label_display.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining_seconds -= 1
            self.timer_job = self.root.after(1000, self.update_clock)
        else:
            # Reached zero: notify and restart loop
            self.label_display.config(text="00:00")
            play_beeps()
            self.remaining_seconds = self.interval_seconds
            self.timer_job = self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = InfiniteIntervalTimer(root)
    root.mainloop()