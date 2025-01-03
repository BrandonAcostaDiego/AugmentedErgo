from pynput import mouse
import math
import tkinter as tk
import time
from data_manager import DataManager

class MouseTracker:
    def __init__(self, data_manager=None):
        self.data_manager = data_manager if data_manager else DataManager()
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
        self.current_distance = 0.0



## distance mouse position, Velocity mouse precision
    def _on_move(self, x, y):
        if not self.is_tracking:
            return

        current_position = (x, y)
        current_time = time.time()

        if self.last_position:
            x_diff = current_position[0] - self.last_position[0]
            y_diff = current_position[1] - self.last_position[1]
            distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)

            time_diff = current_time - self.time
            if time_diff > 0:
                velocity = distance / time_diff
                self.current_velocity = velocity
                if velocity > self.peak_velocity:
                    self.peak_velocity = velocity
                if 100 <= velocity <= 500:
                    self.precision_movement += 0.01

            self.current_distance += distance
            self.total_distance += distance

            self.data_manager.store_movement(
                x,
                y,
                precision=self.precision_movement,
                distance=self.get_total_distance_in_cm(),
                velocity=self.peak_velocity
            )

        self.time = current_time
        self.last_position = current_position
    def _on_click(self, x, y, button, pressed):
        if pressed:
            self.data_manager.store_click(x, y, button)
            self.mouse_clicks += 1



## Buttons: start, stop, reset
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
    def pause_tracking(self):
        if self.is_tracking:
            self.listener.stop()
            self.listener.join()
            self.listener = None

            self.current_distance = 0.0
            self.current_velocity = 0
            self.last_position = None

    def reset_tracking(self):
        if self.listener:
            self.pause_tracking()

        # Reset all values
        self.is_tracking = False
        self.current_distance = 0.0
        self.current_velocity = 0
        self.last_position = None
        self.time = time.time()
        self.precision_movement = 0
        self.mouse_clicks = 0
        self.total_distance = 0.0
        self.peak_velocity = 0

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



