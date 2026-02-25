import tkinter as tk
from tkinter import ttk, Toplevel, Label, Button
from tkinter.messagebox import showinfo
import os

class StepperMotorCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stepper Motor Calculator")
        self.geometry("400x300")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Labels and entries
        self.create_label_entry("Step angle (degrees):", "step_angle", 0)
        self.create_label_entry("Microstep setting:", "microstep_setting", 1)
        self.create_label_entry("Lead (mm/rev):", "lead", 2)
        self.create_label_entry("Maximum RPM:", "max_rpm", 3)

        # Calculate button
        calc_button = ttk.Button(self, text="Calculate", command=self.calculate)
        calc_button.grid(row=4, column=0, columnspan=2, pady=10)
        title_font = ("Helvetica", 18, "bold")
        label4 = ttk.Label(self, text="PCB Drilling And Milling Machine", font=title_font)
        label4.grid(row=5, column=0, columnspan=2, pady=10)

    def create_label_entry(self, label_text, attr_name, row):
        label = ttk.Label(self, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = ttk.Entry(self)
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"{attr_name}_entry", entry)

    def calculate(self):
        try:
            # Input values
            step_angle = float(self.step_angle_entry.get())
            microstep_setting = int(float(self.microstep_setting_entry.get()))
            lead = float(self.lead_entry.get())
            max_rpm = float(self.max_rpm_entry.get())

            if step_angle <= 0:
                raise ZeroDivisionError("Step angle must be greater than zero.")
            if lead <= 0:
                raise ZeroDivisionError("Lead must be greater than zero.")

            # Calculations
            full_steps_per_revolution = 360 / step_angle
            microsteps_per_revolution = full_steps_per_revolution * microstep_setting
            steps_per_millimeter = microsteps_per_revolution / lead
            max_linear_speed = lead * max_rpm

            # Display results
            result = (
                f"Full steps per revolution: {full_steps_per_revolution:.2f}\n"
                f"Microsteps per revolution: {microsteps_per_revolution:.2f}\n"
                f"Steps per millimeter: {steps_per_millimeter:.2f}\n"
                f"Maximum linear speed: {max_linear_speed:.2f} mm/min"
            )
            showinfo("Calculation Results", result)
        except ValueError as e:
            self.show_custom_error("Input Error", f"Invalid input: {e}")
        except ZeroDivisionError as e:
            self.show_custom_error("Calculation Error", str(e))

    def show_custom_error(self, title, message):
        error_dialog = Toplevel(self)
        error_dialog.title(title)
        error_dialog.geometry("500x150")
        error_dialog.resizable(False, False)

        if os.path.exists("error.png"):
            try:
                # Load your custom icon
                custom_icon = tk.PhotoImage(file="error.png")
                icon_label = Label(error_dialog, image=custom_icon)
                icon_label.image = custom_icon
                icon_label.pack(side="left", padx=10, pady=10)
            except tk.TclError:
                pass

        # Message label
        message_label = Label(error_dialog, text=message)
        message_label.pack(side="left", padx=10, pady=10)

        # OK button
        ok_button = Button(error_dialog, text="OK", command=error_dialog.destroy)
        ok_button.pack(side="bottom", pady=10)

if __name__ == "__main__":
    app = StepperMotorCalculator()
    app.mainloop()
