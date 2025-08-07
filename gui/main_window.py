import customtkinter as ctk
from tkinter import filedialog, messagebox
from gui.face_enroll import capture_and_save_face
from core.app_config import save_app_command

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

        self.label = ctk.CTkLabel(self, text="FaceGate Security", font=("Arial", 24))
        self.label.pack(pady=20)

        self.capture_button = ctk.CTkButton(self, text="Capture Face", command=self.capture_face)
        self.capture_button.pack(pady=10)

        self.select_app_button = ctk.CTkButton(self, text="Select Application", command=self.select_app)
        self.select_app_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=20)

    def capture_face(self):
        success = capture_and_save_face()
        if success:
            self.status_label.configure(text="✅ Face saved!")
        else:
            self.status_label.configure(text="❌ Face not detected!")

    def select_app(self):
        filepath = filedialog.askopenfilename(title="Select an App Executable")
        if filepath:
            save_app_command(filepath)
            self.status_label.configure(text=f"✅ App saved: {filepath}")
        else:
            self.status_label.configure(text="No app selected.")
