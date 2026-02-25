
import unittest
from unittest.mock import MagicMock, patch
import sys

# Dummy Tkinter classes
class DummyTk:
    def __init__(self, *args, **kwargs):
        self.children = {}
    def title(self, *args, **kwargs): pass
    def geometry(self, *args, **kwargs): pass
    def resizable(self, *args, **kwargs): pass
    def withdraw(self): pass

# Mock modules
mock_tk = MagicMock()
mock_tk.Tk = DummyTk
mock_tk.Toplevel = MagicMock
mock_tk.Label = MagicMock
mock_tk.Button = MagicMock
mock_tk.PhotoImage = MagicMock

sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

import main

class TestStepperMotorCalculator(unittest.TestCase):
    def setUp(self):
        # Patch create_widgets to avoid GUI setup during init
        with patch.object(main.StepperMotorCalculator, 'create_widgets', return_value=None):
            self.app = main.StepperMotorCalculator()

        self.app.step_angle_entry = MagicMock()
        self.app.microstep_setting_entry = MagicMock()
        self.app.lead_entry = MagicMock()
        self.app.max_rpm_entry = MagicMock()
        self.app.show_custom_error = MagicMock()

    def test_calculate_success(self):
        self.app.step_angle_entry.get.return_value = "1.8"
        self.app.microstep_setting_entry.get.return_value = "16"
        self.app.lead_entry.get.return_value = "8"
        self.app.max_rpm_entry.get.return_value = "1000"

        with patch('main.showinfo') as mock_showinfo:
            self.app.calculate()

            self.assertTrue(mock_showinfo.called, "showinfo was not called")
            args, _ = mock_showinfo.call_args
            result_text = args[1]
            self.assertIn("Full steps per revolution: 200.00", result_text)
            self.assertIn("Microsteps per revolution: 3200.00", result_text)
            self.assertIn("Steps per millimeter: 400.00", result_text)
            self.assertIn("Maximum linear speed: 8000.00 mm/min", result_text)

    def test_calculate_invalid_input(self):
        self.app.step_angle_entry.get.return_value = "abc"
        self.app.calculate()
        self.app.show_custom_error.assert_called_with("Input Error", unittest.mock.ANY)

    def test_calculate_zero_division_step_angle(self):
        self.app.step_angle_entry.get.return_value = "0"
        self.app.microstep_setting_entry.get.return_value = "16"
        self.app.lead_entry.get.return_value = "8"
        self.app.max_rpm_entry.get.return_value = "1000"

        self.app.calculate()
        self.app.show_custom_error.assert_called_with("Calculation Error", "Step angle must be greater than zero.")

    def test_calculate_zero_division_lead(self):
        self.app.step_angle_entry.get.return_value = "1.8"
        self.app.microstep_setting_entry.get.return_value = "16"
        self.app.lead_entry.get.return_value = "0"
        self.app.max_rpm_entry.get.return_value = "1000"

        self.app.calculate()
        self.app.show_custom_error.assert_called_with("Calculation Error", "Lead must be greater than zero.")

    def test_calculate_microstep_float(self):
        self.app.step_angle_entry.get.return_value = "1.8"
        self.app.microstep_setting_entry.get.return_value = "16.0"
        self.app.lead_entry.get.return_value = "8"
        self.app.max_rpm_entry.get.return_value = "1000"

        with patch('main.showinfo') as mock_showinfo:
            self.app.calculate()
            self.assertTrue(mock_showinfo.called, "showinfo was not called for microstep_float")

if __name__ == '__main__':
    unittest.main()
