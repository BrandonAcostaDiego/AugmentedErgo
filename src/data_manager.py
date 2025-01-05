from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os


def load_credentials():
    import sys

    # Look in the same directory as the executable or script
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    creds_path = os.path.join(base_path, 'influxdb_credentials.txt')
    print(f"Looking for credentials at: {creds_path}")  # Debug print

    creds = {}
    try:
        with open(creds_path, encoding='utf-8') as f:
            content = f.read()
            print(f"File content: {content}")  # Debug print
            for line in content.splitlines():
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    print(f"Found key: {key}, value: {value}")  # Debug print
                    creds[key] = value
    except FileNotFoundError:
        raise ValueError(f"Credentials file not found at {creds_path}")
    except Exception as e:
        raise ValueError(f"Error reading credentials: {str(e)}")

    required = ['INFLUXDB_URL', 'INFLUXDB_TOKEN', 'INFLUXDB_ORG', 'INFLUXDB_BUCKET']
    for key in required:
        if key not in creds:
            raise ValueError(f"Missing required credential: {key}")

    return creds


class DataManager:
    def __init__(self, tracker=None):
        self.tracker = tracker
        creds = load_credentials()
        self.client = InfluxDBClient(
            url=creds.get('INFLUXDB_URL').strip(),
            token=creds.get('INFLUXDB_TOKEN').strip(),
            org=creds.get('INFLUXDB_ORG').strip()
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = creds.get('INFLUXDB_BUCKET')
        self.session_id = None

    def start_session(self):
        self.session_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.session_id

    def store_movement(self, x, y, precision=None, distance=None, velocity=None, timestamp=None):
        if not self.session_id:
            raise RuntimeError("Session not started")

        point = (
            Point("mouse_metrics")
            .tag("session_id", self.session_id)
            .field("x", float(x))
            .field("y", float(y))
            .field("precision_effort", float(precision) if precision else 0.0)
            .field("total_distance_cm", float(distance) if distance else 0.0)
            .field("peak_velocity", float(velocity) if velocity else 0.0)
            .time(datetime.now(timezone.utc))
        )
        self.write_api.write(bucket=self.bucket, record=point)

    def store_click(self, x, y, button, timestamp=None):
        if not self.session_id:
            raise RuntimeError("Session not started")

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        point = Point("mouse_click") \
            .tag("session_id", self.session_id) \
            .tag("button", str(button)) \
            .field("x", x) \
            .field("y", y) \
            .time(timestamp)

        self.write_api.write(bucket=self.bucket, record=point)

    def end_session(self):
        self.session_id = None

    def get_session_data(self, session_id=None):
        if session_id is None:
            session_id = self.session_id

        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["session_id"] == "{session_id}")
        '''

        query_api = self.client.query_api()
        return query_api.query(query)

    def cleanup(self):
        self.client.close()
