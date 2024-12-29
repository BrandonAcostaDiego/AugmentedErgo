from pynput import mouse
import math
import tkinter as tk
import time

class MouseTracker:
    def __init__(self):
        self.is_tracking = False
        self.total_distance = 0.0
        self.last_position = None
        self.listener = None
        self.dpi = self.get_screen_dpi()
        self.time = time.time()
        self.precision_movement = 0
        self.current_velocity = 0
        self.peak_velocity = 0
        self.mouse_clicks = 0
        pass

## distance mouse position, Velocity mouse precision
    def _on_move(self, x, y):
        if not self.is_tracking:
            return
#
        current_position = (x, y)
        current_time = time.time()
        if self.last_position:
            x_diff = current_position[0] - self.last_position[0]
            y_diff = current_position[1] - self.last_position[1]
            distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)

            self.current_distance += distance
            self.total_distance += distance
#
            time_diff = current_time - self.time
            if time_diff > 0.0:
                velocity = distance / time_diff
                self.current_velocity = velocity

                if velocity > self.peak_velocity:
                    self.peak_velocity = velocity


                if 100 <= velocity <= 500 and self.current_distance >= 100:
                    self.precision_movement += 0.01
            self.time = current_time
        self.last_position = current_position

    def _on_click(self, *args):
        if args[-1]:
            self.mouse_clicks += 1



## start button -> stop button
#
    def start_tracking(self):
        self.is_tracking = True
        self.current_distance = 0.0
        self.current_velocity = 0
        self.last_position = None
        self.time = time.time()

        self.listener = mouse.Listener(on_move=self._on_move, on_click=self._on_click)
        self.listener.start()

#
    def stop_tracking(self):
        self.is_tracking = False
        self.listener.stop()
        self.listener.join()
        self.listener = None

        self.current_distance = 0.0
        self.current_velocity = 0
        self.last_position = None

#### data manipulation
#
    def movement_data(self):
        return {'current_distance': self.get_current_distance_in_cm(),
                'total_pixels': self.total_distance,
                'total_distance': self.get_total_distance_in_cm(),
                }
    def click_data(self):
        return {'total_clicks': self.mouse_clicks}
#
    def get_screen_dpi(self):
        root = tk.Tk()
        dpi = root.winfo_fpixels('1i')
        root.destroy()
        return dpi
#
    def get_current_distance_in_cm(self):
        inches = self.current_distance / self.dpi
        return inches * 2.54
    def get_total_distance_in_cm(self):
        inches = self.total_distance / self.dpi
        return inches * 2.54

#
    def velocity_data(self):
        return {'velocity': self.current_velocity, 'peak velocity': self.peak_velocity}

    def reset_all(self):
        self.current_velocity = 0
        self.total_distance = 0.0
        self.current_velocity = 0
        self.precision_movement = 0
        self.last_position = None
        self.time = time.time()
        self.mouse_clicks = 0



