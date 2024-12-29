import tkinter as tk
from tkinter import ttk
from mouse_tracker import MouseTracker

class user_interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AugmentedErgo")
        self.tracker = MouseTracker()
        self.root.geometry("600x400")
        self.root['bg'] = 'lightgray'
        self.update_display()
        style = ttk.Style()


# current stat display (left frame)
        self.frame = tk.Frame(self.root, bg='gray', relief='raised', width=210)
        self.frame.pack(side='left', fill='y', padx=2, pady=2)
        self.frame.pack_propagate(False)


# total stat display (right canvas)
        self.display = tk.Canvas(self.root, bg='black', relief='sunken', bd=3)
        self.display.pack(pady=10, fill='both', expand=True)
## labels
        style.configure("Custom.TLabel", foreground='white', background='black', padding=5, relief='sunken')
    #
        self.distance_label = ttk.Label(self.frame, text="Current Distance: 0.00 cm", style='Custom.TLabel')
        self.distance_label.pack(fill='x', padx=6, pady=10)
    #
        self.velocity_label = ttk.Label(self.frame, text="Current Velocity: 0.00 pixels/sec", style='Custom.TLabel')
        self.velocity_label.pack(fill='x', padx=6, pady=0)
# buttons

        style.configure("Start.TButton", width=20, background="lightgreen", foreground='black', relief='sunken')
        style.map("Start.TButton", foreground=[('disabled', 'gray')], background=[('active', 'green')])

        style.configure("Stop.TButton", width=20, background="red", foreground='black', relief='raised')
        style.map("Stop.TButton", foreground=[('disabled', 'gray')], background=[('active', 'darkred')])

    #
        self.start_button = ttk.Button(self.frame, text="Start tracking", command=self.start_tracking,style='Start.TButton')
        self.start_button.pack(side='top', pady=(20,5))
    #
        self.stop_button = ttk.Button(self.frame, text="Stop tracking", command=self.stop_tracking,style='Stop.TButton')
        self.stop_button.pack(side='top')
        self.stop_button['state'] = 'disabled'

    # test button
        '''
        self.button = tk.Button(self.root,
                           text="test button",
                           bg="#4287f5",  # Normal state
                           activebackground="#2d5ba3",  # Clicked state
                           fg="white",
                           relief="raised",
                           borderwidth=2)
        self.button.place(x=100, y=100)
        '''
# update loop
        self.update_display()
        self.root.mainloop()

### methods:
# precision, distance, velocity
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
                    f'Total Flicks:\n'
                    f'Total Time:\n'
                    f'Total Clicks: {clickData['total_clicks']}\n'
                    f'Jerky Motions:}\n'

                ),
                anchor="nw", fill="white", font=('courier', 13)
            )
        # update timing
        self.root.after(50, self.update_display)

    def reset_display(self):
        self.distance_label.config(text="Current Distance: 0.00 cm")
        self.velocity_label.config(text="Current Velocity: 0.00 pixels/sec")
        #current session time
        #current flicks
#
    def start_tracking(self):
        self.tracker.start_tracking()
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
        self.frame.configure(bg='light green', highlightbackground='lime', highlightthickness=3)

#
    def stop_tracking(self):
        self.tracker.stop_tracking()
        self.frame.configure(bg='gray')
        self.frame.configure(highlightbackground='red', highlightthickness='3')
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'
        self.reset_display()

#
    def test_button(self):
        self.test_button()['state'] = 'disabled'
        self.test_button()['state'] = 'normal'

if __name__ == '__main__':
    app = user_interface()

