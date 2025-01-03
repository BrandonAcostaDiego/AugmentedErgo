import tkinter as tk
from tkinter import ttk
from mouse_tracker import MouseTracker
from data_manager import DataManager
from tkinter import messagebox


def main():
    try:
        app = UserInterface()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        root.destroy()
        input("Press Enter to exit...")  # Keeps console open if there's an error


class UserInterface:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("CursorSense")
            self.root.geometry("600x400")
            self.root['bg'] = 'lightgray'

            try:
                self.data_manager = DataManager(tracker=None)  # Create data manager first
                self.tracker = MouseTracker(data_manager=self.data_manager)  # Create tracker with data manager
                self.data_manager.tracker = self.tracker  # Update data manager's tracker reference
                self.data_manager.start_session()
            except Exception as e:
                messagebox.showerror("Initialization Error", f"Failed to initialize tracking: {str(e)}")
                raise

            self.setup_ui()
            self.update_display()
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user interface: {str(e)}")
            raise

    def on_closing(self):
        try:
            if hasattr(self, 'tracker'):
                if getattr(self.tracker, 'is_tracking', False):
                    # Only pause if actually tracking
                    self.tracker.pause_tracking()
                # Clean up tracker regardless of state
                self.tracker = None

            if hasattr(self, 'data_manager'):
                try:
                    self.data_manager.end_session()
                except Exception as e:
                    print(f"Error saving session data: {str(e)}")
                finally:
                    self.data_manager = None
        except Exception as e:
            messagebox.showerror("Error", f"Error while closing: {str(e)}")
        finally:
            self.root.destroy()

    def create_initial_display(self):
        self.display.create_text(
            10, 10,
            text=(
                f'Precise Aiming Effort: -.--\n'
                f'Total Distance: -.-- cm\n'
                f'Peak Velocity: -.-- pixels/s\n'
                f'Total Clicks: -.--\n'
                '\n'
                f'Features to be implemented...\n'
                f'Total Flicks: N/A\n'
                f'Total Time: N/A\n'
                f'Jerky Motions: N/A\n'
                f'+180 degree Turns: N/A\n'
                f'straight lines: N/A\n'
                f'shifts/re-centering: N/A\n'
            ),
            anchor="nw", fill="white", font=('courier', 13)
        )

    def setup_ui(self):
        style = ttk.Style()
        style.configure("Custom.TLabel", foreground='white', background='black', padding=5, relief='sunken')
        style.configure("Start.TButton", width=20, background="lightgreen", foreground='black', relief='sunken')
        style.map("Start.TButton", foreground=[('disabled', 'gray')], background=[('active', 'green')])
        style.configure("Pause.TButton", width=20, background="red", foreground='black', relief='raised')
        style.map("Pause.TButton", foreground=[('disabled', 'gray')], background=[('active', 'darkred')])
        style.configure("reset.TButton", width=20, background="lightblue", foreground='black', relief='raised')

        # current stat display (left frame)
        self.frame = tk.Frame(self.root, bg='gray', relief='raised', width=210)
        self.frame.pack(side='left', fill='y', padx=2, pady=2)
        self.frame.pack_propagate(False)

        # idea: reveal data technique using after
        # total stat display (right canvas)
        self.display = tk.Canvas(self.root, bg='black', relief='sunken', bd=3)
        self.display.pack(pady=10, fill='both', expand=True)
        self.create_initial_display()

        # Labels
        self.distance_label = ttk.Label(self.frame, text="Current Distance: 0.00 cm", style='Custom.TLabel')
        self.distance_label.pack(fill='x', padx=6, pady=10)

        self.velocity_label = ttk.Label(self.frame, text="Current Velocity: 0.00 pixels/sec", style='Custom.TLabel')
        self.velocity_label.pack(fill='x', padx=6, pady=0)


        # Buttons
        self.start_button = ttk.Button(self.frame, text="Start tracking", command=self.start_tracking,style='Start.TButton')
        self.start_button.pack(side='top', pady=(20,5))

        self.pause_button = ttk.Button(self.frame, text="Pause tracking", command=self.pause_tracking, style='Pause.TButton')
        self.pause_button.pack(side='top')
        self.pause_button['state'] = 'disabled'

        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.reset_all, style='reset.TButton')
        self.reset_button.pack(side='bottom')
        self.reset_button['state'] = 'normal'


##### methods:
#
    def update_display(self):
        if self.tracker.is_tracking:
            distData = self.tracker.movement_data()
            velData = self.tracker.velocity_data()
            clickData = self.tracker.click_data()

            self.distance_label.config(text=f"Current Distance: {distData['current_distance']:.2f} cm")
            self.velocity_label.config(text=f"Current Velocity: {velData['velocity']:.2f} pixels/s")

            self.display.delete("all")

            self.display.create_text(
                10, 10,
                text=(
                    f'Precise Aiming Effort: {self.tracker.precision_movement:.2f}\n'
                    f'Total Distance: {distData['total_distance']:.2f} cm\n'
                    f'Peak Velocity: {self.tracker.peak_velocity:.2f} pixels/s\n'
                    f'Total Clicks: {clickData['total_clicks']}\n'
                    '\n'
                    f'Features to be implemented...\n'
                    f'Total Flicks: N/A\n'  #add click requirement at end of flick?
                    f'Total Time: N/A\n'
                    f'Jerky Motions: N/A\n'
                    f'+180 degree Turns: N/A\n' 
                    f'straight lines: N/A\n' #smooth factor
                    f'shifts/re-centering: N/A\n' #mouse pick up inferred with data gap
                ),
                anchor="nw", fill="white", font=('courier', 13)
            )
        self.root.after(50, self.update_display)
                                            # don't need other parameters from pynput
#
    def reset_display(self):
        self.distance_label.config(text="Current Distance: 0.00 cm")
        self.velocity_label.config(text="Current Velocity: 0.00 pixels/s")

#
    def start_tracking(self):
        self.tracker.start_tracking()
        self.data_manager.start_session()
        self.start_button['state'] = 'disabled'
        self.pause_button['state'] = 'normal'
        self.frame.configure(bg='light green', highlightbackground='lime', highlightthickness=3)

#
    def pause_tracking(self):
        self.tracker.pause_tracking()
        self.frame.configure(bg='gray')
        self.frame.configure(highlightbackground='red', highlightthickness='3')
        self.start_button['state'] = 'normal'
        self.pause_button['state'] = 'disabled'
        self.reset_display()
#
    def reset_all(self):
        self.tracker.reset_tracking()
        self.reset_display()
        self.display.delete("all")

        self.start_tracking()
        if self.tracker.pause_tracking:
            self.pause_tracking()



if __name__ == '__main__':
    main()
