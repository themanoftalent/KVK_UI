import tkinter as tk
from tkinter import ttk, messagebox, font

class SimpleApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # ---------- Window setup ----------
        self.title("Simple GUI App – Navigation, Windows, Controls & Visual Layer")
        self.geometry("700x500")
        self.minsize(500, 400)
        self.configure(bg="#1e1e2e")          # dark visual layer

        # Custom fonts (Visual Layer)
        self.title_font = font.Font(family="Segoe UI", size=18, weight="bold")
        self.normal_font = font.Font(family="Segoe UI", size=11)
        self.button_font = font.Font(family="Segoe UI", size=10, weight="bold")

        # Style for ttk widgets
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=self.button_font, padding=8)
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=self.normal_font)
        style.configure("Header.TLabel", font=self.title_font, foreground="#89b4fa")

        # ---------- Navigation container ----------
        self.container = tk.Frame(self, bg="#1e1e2e")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.frames = {}
        for F in (HomePage, SettingsPage, AboutPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """Navigation: switch between pages"""
        frame = self.frames[page_name]
        frame.tkraise()

    def open_secondary_window(self):
        """Open a new independent Window"""
        SecondaryWindow(self)


# ==================== PAGES (Navigation) ====================

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller

        # Header
        ttk.Label(self, text="🏠 Home Page", style="Header.TLabel").pack(pady=(20, 10))

        # Description
        ttk.Label(
            self,
            text="This page demonstrates basic Controls and the Visual Layer.",
            wraplength=500
        ).pack(pady=5)

        # ----- Controls -----
        control_frame = tk.Frame(self, bg="#313244", padx=20, pady=15)
        control_frame.pack(pady=20, fill="x", padx=40)

        ttk.Label(control_frame, text="Enter your name:").pack(anchor="w")
        self.name_entry = ttk.Entry(control_frame, width=30, font=self.controller.normal_font)
        self.name_entry.pack(pady=5, fill="x")

        ttk.Button(
            control_frame,
            text="Greet Me",
            command=self.greet
        ).pack(pady=10)

        self.result_label = ttk.Label(control_frame, text="", foreground="#a6e3a1")
        self.result_label.pack()

        # Navigation buttons
        nav_frame = tk.Frame(self, bg="#1e1e2e")
        nav_frame.pack(side="bottom", pady=20)

        ttk.Button(nav_frame, text="Settings", command=lambda: controller.show_frame("SettingsPage")).pack(side="left", padx=8)
        ttk.Button(nav_frame, text="About", command=lambda: controller.show_frame("AboutPage")).pack(side="left", padx=8)
        ttk.Button(nav_frame, text="Open New Window", command=controller.open_secondary_window).pack(side="left", padx=8)

    def greet(self):
        name = self.name_entry.get().strip()
        if name:
            self.result_label.config(text=f"Hello, {name}! Welcome to the app.")
        else:
            messagebox.showwarning("Input needed", "Please enter your name.")


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller

        ttk.Label(self, text="⚙️ Settings", style="Header.TLabel").pack(pady=(20, 10))

        # Controls example – radio buttons & checkbox
        options_frame = tk.Frame(self, bg="#313244", padx=20, pady=15)
        options_frame.pack(pady=15, fill="x", padx=40)

        ttk.Label(options_frame, text="Theme preference:").pack(anchor="w")
        self.theme_var = tk.StringVar(value="Dark")
        for theme in ["Dark", "Light", "System"]:
            ttk.Radiobutton(options_frame, text=theme, variable=self.theme_var, value=theme).pack(anchor="w")

        self.notify_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Enable notifications", variable=self.notify_var).pack(anchor="w", pady=8)

        ttk.Button(options_frame, text="Save Settings", command=self.save).pack(pady=10)

        # Navigation
        nav = tk.Frame(self, bg="#1e1e2e")
        nav.pack(side="bottom", pady=20)
        ttk.Button(nav, text="← Home", command=lambda: controller.show_frame("HomePage")).pack(side="left", padx=8)
        ttk.Button(nav, text="About →", command=lambda: controller.show_frame("AboutPage")).pack(side="left", padx=8)

    def save(self):
        messagebox.showinfo(
            "Settings Saved",
            f"Theme: {self.theme_var.get()}\nNotifications: {'On' if self.notify_var.get() else 'Off'}"
        )


class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller

        ttk.Label(self, text="ℹ️ About", style="Header.TLabel").pack(pady=(20, 10))

        info = (
            "Simple GUI App\n\n"
            "Demonstrates:\n"
            "• Navigation between pages\n"
            "• Multiple Windows\n"
            "• Common Controls (Entry, Button, Radio, Checkbutton…)\n"
            "• Visual Layer (colors, fonts, layout)\n\n"
            "Built with Python + Tkinter"
        )
        ttk.Label(self, text=info, justify="left").pack(pady=10)

        nav = tk.Frame(self, bg="#1e1e2e")
        nav.pack(side="bottom", pady=20)
        ttk.Button(nav, text="← Home", command=lambda: controller.show_frame("HomePage")).pack(side="left", padx=8)
        ttk.Button(nav, text="Settings", command=lambda: controller.show_frame("SettingsPage")).pack(side="left", padx=8)


# ==================== SECONDARY WINDOW ====================

class SecondaryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Secondary Window")
        self.geometry("400x300")
        self.configure(bg="#181825")

        ttk.Label(self, text="This is a separate Window", style="Header.TLabel").pack(pady=30)

        # Listbox control example
        list_frame = tk.Frame(self, bg="#313244")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ttk.Label(list_frame, text="Example List Control:").pack(anchor="w", pady=5)
        self.listbox = tk.Listbox(list_frame, bg="#45475a", fg="#cdd6f4", font=("Segoe UI", 10), height=6)
        for item in ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(fill="both", expand=True, pady=5)

        ttk.Button(self, text="Close Window", command=self.destroy).pack(pady=15)


# ==================== RUN ====================

if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()