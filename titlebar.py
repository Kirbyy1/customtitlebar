import customtkinter as ctk
import ctypes
from PIL import Image

# --- Styling Constants ---
TITLE_BAR_BG = "#1E1F22"
BG_DARK = "#313338"
BORDER_COLOR = "#3F4147"
TEXT_MUTED = "#B5BAC1"
BLURPLE = "#5865F2"


class CustomTitleWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Window Configuration
        self.geometry("500x400")
        self.configure(fg_color=BG_DARK)
        self.overrideredirect(True)  # Removes the native Windows title bar

        # Variables for window dragging and pinning
        self.old_x, self.old_y = 0, 0
        self.is_pinned = False

        # 2. Setup the UI
        self.setup_custom_title_bar()

        # 3. Windows Taskbar Fix
        # This allows the window to appear in the taskbar despite overrideredirect(True)
        self.after(10, self.set_appwindow)

    def set_appwindow(self):
        """Fixes the missing taskbar icon caused by overrideredirect."""
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = (ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE) & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        self.withdraw()
        self.after(10, self.deiconify)

    def setup_custom_title_bar(self):
        # Container for the title bar
        bar = ctk.CTkFrame(self, fg_color=TITLE_BAR_BG, height=35, corner_radius=0)
        bar.pack(side="top", fill="x")

        # --- Icon & Title ---
        try:
            self.title_icon_img = ctk.CTkImage(Image.open("logo.ico"), size=(18, 18))
            self.icon_label = ctk.CTkLabel(bar, image=self.title_icon_img, text="")
            self.icon_label.pack(side="left", padx=(10, 0))
        except Exception:
            pass  # Fallback if icon is missing

        ctk.CTkLabel(bar, text=" MY PROJECT TITLE", font=("Segoe UI", 10, "bold"),
                     text_color=TEXT_MUTED).pack(side="left", padx=5)

        # --- Control Buttons (Right Side) ---
        # Close Button
        ctk.CTkButton(bar, text="✕", width=40, height=35, fg_color="transparent",
                      hover_color="#ED4245", corner_radius=0,
                      command=self.destroy).pack(side="right")

        # Minimize Button
        ctk.CTkButton(bar, text="—", width=40, height=35, fg_color="transparent",
                      hover_color=BORDER_COLOR, corner_radius=0,
                      command=self.withdraw).pack(side="right")

        # Pin/Always on Top Button
        self.pin_btn = ctk.CTkButton(bar, text="📌", width=40, height=35, fg_color="transparent",
                                     hover_color=BORDER_COLOR, corner_radius=0,
                                     command=self.toggle_pin)
        self.pin_btn.pack(side="right")

        # --- Dragging Bindings ---
        bar.bind("<ButtonPress-1>", self.on_press)
        bar.bind("<B1-Motion>", self.on_move)

    # --- Window Logic Methods ---
    def on_press(self, e):
        self.old_x, self.old_y = e.x, e.y

    def on_move(self, e):
        x = self.winfo_x() + (e.x - self.old_x)
        y = self.winfo_y() + (e.y - self.old_y)
        self.geometry(f"+{x}+{y}")

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.attributes("-topmost", self.is_pinned)
        self.pin_btn.configure(fg_color=BLURPLE if self.is_pinned else "transparent")


if __name__ == "__main__":
    app = CustomTitleWindow()
    app.mainloop()
