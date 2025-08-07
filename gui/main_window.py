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

        self.entry = ctk.CTkEntry(self, placeholder_text="enter command here")
        self.entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.select_app)
        self.submit_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=20)

    def capture_face(self):
        success = capture_and_save_face()
        if success:
            self.status_label.configure(text="✅ Face saved!")
        else:
            self.status_label.configure(text="❌ Face not detected!")

    def select_app(self):
        command =self.entry.get()
        if command:
            save_app_command(command)
            self.status_label.configure(text=f"✅ Command saved: {command}")
        else:
            self.status_label.configure(text="No app selected.")

