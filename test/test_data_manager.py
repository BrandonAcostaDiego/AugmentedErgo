import pytest
from datetime import datetime, timezone
from src.data_manager import DataManager
import os
from pathlib import Path


class TestDataManager:
    @pytest.fixture
    def data_manager(self):
        cred_path = Path("influxdb_credentials.txt.txt")
        with open(cred_path) as f:
            creds = {line.split('=', 1)[0].strip(): line.split('=', 1)[1].strip()
                     for line in f}

        dm = DataManager(
            url=creds["INFLUXDB_URL"],
            token=creds["INFLUXDB_TOKEN"],
            bucket=creds["INFLUXDB_BUCKET"]
        )
        yield dm
        dm.cleanup()


    def test_start_session(self, data_manager):
        session_id = data_manager.start_session()
        assert isinstance(session_id, str)
        assert len(session_id) > 0

    def test_store_movement(self, data_manager):
        data_manager.start_session()
        data_manager.store_movement(100, 200)

        results = data_manager.get_session_data()
        assert len(results) > 0

    def test_store_click(self, data_manager):
        data_manager.start_session()
        data_manager.store_click(150, 250, "left")

        results = data_manager.get_session_data()
        assert len(results) > 0

    def test_session_required(self, data_manager):
        with pytest.raises(RuntimeError):
            data_manager.store_movement(100, 200)

    def test_end_session(self, data_manager):
        data_manager.start_session()
        data_manager.end_session()
        assert data_manager.session_id is None