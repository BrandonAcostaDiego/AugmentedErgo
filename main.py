from src.mouse_tracker import MouseTracker
import time

def main():
    tracker = MouseTracker()
    tracker.start_tracking()

    print("Tracking initiated...")
    for i in range(5):
        time.sleep(0.5)
        print(f"distance movement: {tracker.total_distance:.2f} pixels")
        print(f'precision movements: {tracker.precision_movement:.2f}')
    tracker.pause_tracking()
    print(f"Distance in centimeters is: {tracker.get_total_distance_in_cm():.2f} cm")
    print(f'final precision count: {tracker.precision_movement:.2f}')



if __name__ == "__main__":
    main()