# -------------------------------------------------------
# SIDS Monitoring System - Bachelor of Engineering Project
# -------------------------------------------------------
# This project is a simple attempt to monitor breathing
# movement in infants (SIDS = Sudden Infant Death Syndrome).
# It uses OpenCV + Tkinter for GUI and webcam detection.
# -------------------------------------------------------

# First install dependencies (run in terminal):
# pip install numpy opencv-python pillow

# On Linux / Raspberry Pi, also install tkinter:
# sudo apt-get install python3-tk

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import cv2
import numpy as np


class SIDSApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SIDS Monitoring System")
        self.master.geometry("1000x700")
        self.master.configure(background="lightblue")

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        """Setup the GUI (labels, buttons, etc)."""

        # Title banner
        tk.Label(
            self.master,
            text="SIDS Monitoring System",
            bg="black",
            fg="white",
            font=("Arial", 26, "bold"),
            width=50,
            height=2
        ).pack(pady=10)

        # Instructions
        tk.Label(
            self.master,
            text="Choose an option below",
            bg="lightblue",
            fg="black",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        # Button 1: Compare two images
        tk.Button(
            self.master,
            text="Breath Detection (Two Images)",
            command=self.detect_from_images,
            width=40,
            height=2,
            bg="darkblue",
            fg="white",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        # Button 2: Live webcam detection
        tk.Button(
            self.master,
            text="Live Breath Detection (Webcam)",
            command=self.detect_from_webcam,
            width=40,
            height=2,
            bg="darkblue",
            fg="white",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        # Output label
        self.result_label = tk.Label(
            self.master,
            text="Result will be displayed here...",
            bg="lightblue",
            fg="black",
            font=("Arial", 16, "bold")
        )
        self.result_label.pack(pady=20)

    # -------------------------------
    # Breath detection using 2 images
    # -------------------------------
    def detect_from_images(self):
        messagebox.showinfo("Info", "Select two images for analysis")

        img1_path = filedialog.askopenfilename(title="Select First Image")
        img2_path = filedialog.askopenfilename(title="Select Second Image")

        if not img1_path or not img2_path:
            messagebox.showwarning("Warning", "Image selection cancelled.")
            return

        try:
            img1 = Image.open(img1_path).resize((200, 200))
            img2 = Image.open(img2_path).resize((200, 200))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open images: {e}")
            return

        # Both images should have same size and mode
        if img1.mode != img2.mode or img1.size != img2.size:
            messagebox.showerror("Error", "Images must have same size and mode!")
            return

        # Pixel difference
        pairs = zip(img1.getdata(), img2.getdata())
        if len(img1.getbands()) == 1:
            diff_sum = sum(abs(p1 - p2) for p1, p2 in pairs)
        else:
            diff_sum = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

        total_components = img1.size[0] * img1.size[1] * 3
        difference_percentage = (diff_sum / 255.0 * 100) / total_components

        # Display result
        if difference_percentage < 0.5:  # threshold
            result = f"Difference: {difference_percentage:.4f}%\nNo breathing detected ⚠️"
        else:
            result = f"Difference: {difference_percentage:.4f}%\nBreathing detected ✅"

        self.result_label.config(text=result)

    # ---------------------------------
    # Live breath detection (Webcam)
    # ---------------------------------
    def detect_from_webcam(self):
        messagebox.showinfo("Info", "Press 'q' to quit live detection")

        cap = cv2.VideoCapture(0)  # webcam

        # Read 2 frames for differencing
        ret, frame1 = cap.read()
        ret, frame2 = cap.read()

        while cap.isOpened():
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            movement = cv2.countNonZero(dilated)

            # Show video feed
            cv2.imshow("Live Breath Detection", frame1)

            # Update GUI result label
            if movement < 500:  # threshold for "no movement"
                self.result_label.config(text=f"Movement: {movement}\nNo breathing ⚠️")
            else:
                self.result_label.config(text=f"Movement: {movement}\nBreathing ✅")

            # Slide frames
            frame1 = frame2
            ret, frame2 = cap.read()

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


# -------------------------
# Main program starts here
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SIDSApp(root)
    root.mainloop()
