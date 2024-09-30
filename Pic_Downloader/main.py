import os
from pyicloud import PyiCloudService
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, StringVar, IntVar, ttk, simpledialog
import threading


class iCloudDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iCloud Photo Downloader")
        self.root.geometry("450x350")
        self.root.configure(bg='#f0f0f0')  # Set background color

        # Custom icon (ensure the path to the .ico file is correct)
        self.root.iconbitmap('icon2.ico')

        self.status_var = StringVar()
        self.progress_var = IntVar()

        # Define a consistent font style for the entire app
        self.font_style = ("Courier New", 12)

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        Label(self.root, text="iCloud Photo Downloader", font=("Helvetica", 16, 'bold'), bg='#f0f0f0').pack(pady=10)

        # Apple ID input
        Label(self.root, text="Apple ID 🔑 :", font=self.font_style, bg='#f0f0f0').pack(pady=5)
        self.apple_id_entry = Entry(self.root, width=40, font=self.font_style)
        self.apple_id_entry.pack(pady=5)

        # Password input
        Label(self.root, text="Password 🔐 :", font=self.font_style, bg='#f0f0f0').pack(pady=5)
        self.password_entry = Entry(self.root, width=40, font=self.font_style, show='*')
        self.password_entry.pack(pady=5)

        # Status label
        self.status_label = Label(self.root, textvariable=self.status_var, font=self.font_style, bg='#f0f0f0')
        self.status_label.pack(pady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate',
                                            variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        # Start Button with a modern style
        self.start_button = Button(self.root, text="Start Download 💾", font=self.font_style, width=20, bg="#4CAF50",
                                   fg="white",
                                   command=self.start_download)
        self.start_button.pack(pady=20)

    def start_download(self):
        apple_id = self.apple_id_entry.get()
        password = self.password_entry.get()

        if not apple_id or not password:
            messagebox.showerror("Input Error", "Please enter both Apple ID and Password.")
            return

        # Disable button and start background thread
        self.start_button.config(state="disabled")
        self.status_var.set("Connecting to iCloud...")
        threading.Thread(target=self.download_photos, args=(apple_id, password)).start()

    def download_photos(self, apple_id, password):
        api = authenticate_icloud(apple_id, password, self.root)

        if api:
            self.status_var.set("Fetching iCloud Photos...")
            photos = api.photos.all
            total_photos = len(photos)

            if total_photos == 0:
                self.status_var.set("No photos found in iCloud.")
                self.start_button.config(state="normal")
                return

            self.progress_bar.config(maximum=total_photos)
            self.progress_var.set(0)

            save_directory = filedialog.askdirectory(title="Select Folder to Save Photos")
            if not save_directory:
                self.status_var.set("No folder selected. Exiting...")
                self.start_button.config(state="normal")
                return

            existing_files = set(os.listdir(save_directory))  # List of files already in the directory

            for index, photo in enumerate(photos):
                try:
                    file_name = photo.filename or f"photo_{index}.jpg"
                    download_path = os.path.join(save_directory, file_name)

                    # Check if the photo already exists based on filename
                    if file_name in existing_files:
                        self.status_var.set(f"Skipping {file_name}, already exists.")
                        self.progress_var.set(index + 1)
                        self.root.update_idletasks()
                        continue

                    # Download photo if it doesn't exist
                    response = photo.download()
                    with open(download_path, "wb") as f:
                        f.write(response.content)

                    self.progress_var.set(index + 1)
                    self.root.update_idletasks()
                    self.status_var.set(f"Downloaded {file_name}")

                except Exception as e:
                    self.status_var.set(f"Error downloading {photo.filename}: {e}")

            self.status_var.set("Download completed.")
        else:
            self.status_var.set("iCloud connection failed.")

        self.start_button.config(state="normal")


def authenticate_icloud(apple_id, password, root):
    api = PyiCloudService(apple_id, password)

    if api.requires_2fa:
        # Prompt for 2FA code in a dialog window instead of the console
        code = simpledialog.askstring("Two-factor Authentication",
                                      "Enter the 2FA code sent to your device:", parent=root)
        if not code:
            messagebox.showerror("2FA Error", "No 2FA code entered.")
            return None

        result = api.validate_2fa_code(code)
        if not result:
            messagebox.showerror("2FA Error", "Failed to verify 2FA code.")
            return None

        if not api.is_trusted_session:
            messagebox.showerror("Session Error",
                                 "Session is not trusted. Please trust the session in your account settings.")
            return None

    return api


if __name__ == "__main__":
    root = Tk()
    app = iCloudDownloaderApp(root)
    root.mainloop()
