import unittest
from unittest.mock import patch, MagicMock
import threading
from . import periodic_refresh

# python



class TestPeriodicRefresh(unittest.TestCase):
    @patch("app.__init__.refresh_omari_loan_data")
    @patch("app.__init__.time.sleep")
    def test_periodic_refresh_runs_once(self, mock_sleep, mock_refresh):
        # Arrange: make time.sleep raise after first call to break the loop
        def sleep_side_effect(*args, **kwargs):
            raise RuntimeError("Stop thread after one iteration")
        mock_sleep.side_effect = sleep_side_effect

        # Act & Assert
        with self.assertRaises(RuntimeError):
            periodic_refresh(interval_seconds=5)
        mock_refresh.assert_called_once()
        mock_sleep.assert_called_once_with(5)
        
        




if __name__ == "__main__":
    unittest.main()