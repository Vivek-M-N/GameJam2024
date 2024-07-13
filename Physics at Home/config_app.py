import tkinter as tk
from tkinter import messagebox

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parameter Configuration")
        # self.display_parameters = {
        #     "Mass (kg)": 300,
        #     "Drag Coefficient (-)": 0.47,
        #     "Area (m^2)": 1,
        #     "Air Density (kg/m^3)": 1.15,
        #     "Coefficient Of Restitution (-)": 0.01
        # }
        self.actual_parameters = {
            "Mass (kg)": 300,
            "Drag Coefficient (-)": 0.47,
            "Area (m^2)": 1,
            "Air Density (kg/m^3)": 1.15,
            "Coefficient Of Restitution (-)": 0.9
        }
        self.resolutions = {
            "Mass (kg)": 1,
            "Drag Coefficient (-)": 0.1,
            "Area (m^2)": 0.1,
            "Air Density (kg/m^3)": 0.01,
            "Coefficient Of Restitution (-)": 0.01
        }
        self.limits = {
            "Mass (kg)": (0.1, 3000),
            "Drag Coefficient (-)": (0.01, 10),
            "Area (m^2)": (0.1, 10),
            "Air Density (kg/m^3)": (0.1, 10),
            "Coefficient Of Restitution (-)": (0.2, 1)
        }
        self.sliders = {}
        self.create_sliders()

    def create_sliders(self):
        row = 0
        for key, value in self.actual_parameters.items():
            label = tk.Label(self.root, text=key)
            label.grid(row=row, column=0, padx=10, pady=10)
            resolution = self.resolutions.get(key, 0.01)
            lower_limit, upper_limit = self.limits.get(key, (0, value * 2))
            slider = tk.Scale(self.root, from_=lower_limit, to=upper_limit, orient=tk.HORIZONTAL, resolution=resolution)
            slider.set(value)
            slider.grid(row=row, column=1, padx=10, pady=10)
            self.sliders[key] = slider
            row += 1

        save_button = tk.Button(self.root, text="Save", command=self.save_config)
        save_button.grid(row=row, columnspan=2, padx=10, pady=10)

    def save_config(self):
        for key, slider in self.sliders.items():
            self.actual_parameters[key] = float(slider.get())
        
        with open("config.txt", "w") as file:
            file.write(str(self.actual_parameters))
        
        messagebox.showinfo("Configuration Saved", "Configuration has been saved successfully!")
        self.root.destroy()
