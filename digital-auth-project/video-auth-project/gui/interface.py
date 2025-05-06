import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import sys
import threading
from utils.baseline_manager import analyze_video_against_baseline, store_video_baseline_data

class VideoAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Video Tamper Detection")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        self.uploaded_file_path = ""
        self.mode = tk.StringVar(value="verify")

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="📽️ Video Authentication System", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=20)

        mode_frame = tk.Frame(self.root, bg="#f0f0f0")
        mode_frame.pack(pady=5)
        tk.Label(mode_frame, text="Select Mode:", font=("Helvetica", 12), bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Store Originals", variable=self.mode, value="store", bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="Verify Authenticity", variable=self.mode, value="verify", bg="#f0f0f0").pack(side=tk.LEFT)

        self.upload_btn = tk.Button(self.root, text="Upload Video", font=("Helvetica", 12), command=self.upload_video)
        self.upload_btn.pack(pady=10)

        self.filename_label = tk.Label(self.root, text="No file selected", bg="#f0f0f0", font=("Helvetica", 10))
        self.filename_label.pack(pady=5)

        self.action_btn = tk.Button(self.root, text="Run", font=("Helvetica", 12), command=self.run_action, state=tk.DISABLED)
        self.action_btn.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate", length=300)
        self.progress.pack(pady=5)

        self.result_text = tk.Text(self.root, height=12, width=80, wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(pady=10)

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.uploaded_file_path = file_path
            self.filename_label.config(text=os.path.basename(file_path))
            self.action_btn.config(state=tk.NORMAL)

    def run_action(self):
        if not self.uploaded_file_path:
            messagebox.showwarning("No file", "Please upload a video file first.")
            return

        if not self.uploaded_file_path.endswith('.mp4'):
            messagebox.showwarning("Invalid file type", "Only MP4 files are supported.")
            return

        self.progress.start()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)

        # Disable action button while processing
        self.action_btn.config(state=tk.DISABLED)

        # Run task in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.execute_task)
        thread.start()

    def execute_task(self):
        try:
            if self.mode.get() == "store":
                result = store_video_baseline_data(self.uploaded_file_path)
            else:
                result = analyze_video_against_baseline(self.uploaded_file_path)
            self.display_result(result)
        except Exception as e:
            self.display_result(f"Error: {str(e)}")
        finally:
            self.progress.stop()
            self.action_btn.config(state=tk.NORMAL)

    def display_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoAuthApp(root)
    root.mainloop()
