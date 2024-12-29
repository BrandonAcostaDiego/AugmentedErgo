import unittest
from src.mouse_tracker import MouseTracker

class MouseTrackerTest(unittest.TestCase):
    def setUp(self):
        self.tracker = MouseTracker()

    def test_tracking_starts(self):
        self.assertFalse(self.tracker.is_tracking)
        self.assertIsNone(self.tracker.listener)

        self.tracker.start_tracking()

        self.assertTrue(self.tracker.is_tracking)
        self.assertIsNotNone(self.tracker.listener)
        self.assertTrue(self.tracker.listener.running)

    def test_distance_calculation(self):
        self.tracker.start_tracking()

        # verify initial state
        self.assertEqual(self.tracker.total_distance, 0.0)

        self.tracker._on_move(0, 0)
        self.assertEqual(self.tracker.last_position, (0, 0))

        self.tracker._on_move(3, 4)
        self.assertEqual(self.tracker.last_position, (3, 4))

        self.assertAlmostEqual(self.tracker.total_distance, 5.0, places=2)

    def test_tracking_stops(self):
        # initial -> start -> stop -> verify
#
        self.assertFalse(self.tracker.is_tracking)
        self.assertIsNone(self.tracker.listener)
#
        self.tracker.start_tracking()
        self.assertTrue(self.tracker.is_tracking)
        self.assertIsNotNone(self.tracker.listener)
        self.assertTrue(self.tracker.listener.running)
# test movements
        self.tracker._on_move(0, 0)
        self.tracker._on_move(3, 4)
        self.tracker._on_move(7, 5)
        initial_distance = self.tracker.total_distance
#
        self.tracker.stop_tracking()
        self.assertEqual(self.tracker.total_distance, initial_distance)
#
        self.assertFalse(self.tracker.is_tracking)
        self.assertIsNone(self.tracker.listener)
# test after stop
        self.tracker._on_move(10, 10)
        self.assertEqual(self.tracker.total_distance, initial_distance)







