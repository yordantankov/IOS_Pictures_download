import os
from pyicloud import PyiCloudService
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, StringVar, IntVar, ttk
import threading


class iCloudDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("iCloud Photo Downloader")
        self.root.geometry("400x300")

        self.status_var = StringVar()
        self.progress_var = IntVar()

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Apple ID input
        Label(self.root, text="Apple ID:").pack(pady=5)
        self.apple_id_entry = Entry(self.root, width=50)
        self.apple_id_entry.pack(pady=5)

        # Password input
        Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = Entry(self.root, width=50, show='*')  # Show '*' for password
        self.password_entry.pack(pady=5)

        # Status label
        self.status_label = Label(self.root, textvariable=self.status_var)
        self.status_label.pack(pady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate',
                                            variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        # Start Button
        self.start_button = Button(self.root, text="Start Download", command=self.start_download)
        self.start_button.pack(pady=10)

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
        api = authenticate_icloud(apple_id, password)
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

            for index, photo in enumerate(photos):
                try:
                    file_name = photo.filename or f"photo_{index}.jpg"
                    download_path = os.path.join(save_directory, file_name)

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


def authenticate_icloud(apple_id, password):
    api = PyiCloudService(apple_id, password)

    if api.requires_2fa:
        code = input("Enter the code you received on your devices: ")
        result = api.validate_2fa_code(code)
        if not result:
            print("Failed to verify 2FA code.")
            return None
        if not api.is_trusted_session:
            print("Session is not trusted. Please trust the session in your account settings.")
            return None

    return api


if __name__ == "__main__":
    root = Tk()
    app = iCloudDownloaderApp(root)
    root.mainloop()
