import tkinter as tk
from tkinter import messagebox

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration")

        self.labels = ["Mass", "Drag Coefficient", "Area", "Air Density", "Gravity"]
        self.scales = {}

        self.scale_ranges = {
            "Mass": (100, 1000),
            "Drag Coefficient": (0.1, 1.0),
            "Area": (0.1, 10),
            "Air Density": (0.5, 2.0),
            "Gravity": (5, 20)
        }

        for i, label in enumerate(self.labels):
            tk.Label(root, text=label).grid(row=i, column=0)
            scale = tk.Scale(root, from_=self.scale_ranges[label][0], to=self.scale_ranges[label][1],
                             resolution=0.01, orient=tk.HORIZONTAL)
            scale.grid(row=i, column=1)
            self.scales[label] = scale

        self.scales["Mass"].set(300)
        self.scales["Drag Coefficient"].set(0.47)
        self.scales["Area"].set(1)
        self.scales["Air Density"].set(1.15)
        self.scales["Gravity"].set(9.81)

        tk.Button(root, text="Apply", command=self.apply).grid(row=len(self.labels), column=0, columnspan=2)

    def apply(self):
        config = {label: scale.get() for label, scale in self.scales.items()}
        with open("config.txt", "w") as file:
            file.write(str(config))
        messagebox.showinfo("Success", "Configuration applied successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()
