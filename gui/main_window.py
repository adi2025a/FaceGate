import customtkinter as ctk
from tkinter import messagebox
from gui.face_enroll import capture_and_save_face
from core.app_config import save_app_command
from desktop.patcher import patch_app


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def run_app():
    app = FaceGateApp()
    app.mainloop()


class FaceGateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FaceGate - Face Lock for Apps")
        self.geometry("500x400")

        # Title
        self.label = ctk.CTkLabel(self, text="FaceGate Security", font=("Arial", 24))
        self.label.pack(pady=20)

        # Face Capture Button
        self.capture_button = ctk.CTkButton(self, text="Capture Face", command=self.capture_face)
        self.capture_button.pack(pady=10)

        # App Command Input
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter app command (e.g., google-chrome)")
        self.entry.pack(pady=10)

        # Patch App Button
        self.submit_button = ctk.CTkButton(self, text="Secure App", command=self.select_and_patch_app)
        self.submit_button.pack(pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=20)

    def capture_face(self):
        success = capture_and_save_face()
        if success:
            self.status_label.configure(text="✅ Face saved!")
        else:
            self.status_label.configure(text="❌ Face not detected!")

    def select_and_patch_app(self):
        command = self.entry.get().strip()
        if not command:
            self.status_label.configure(text="⚠️ Please enter a command.")
            return

        # Save app command
        save_app_command(command)

        # Try to patch app (assumes .desktop filename = command name)
        app_name = command  # e.g., 'google-chrome'
        patched = patch_app(app_name, command)

        if patched:
            self.status_label.configure(text=f"✅ App secured: {command}")
        else:
            self.status_label.configure(text=f"❌ Failed to patch: {command}")
