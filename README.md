# IOS_Pictures_download
download picture's from IOS to pc

## Update: Fix for Tkinter threading issue

### Solution

To avoid this issue, ensure that all Tkinter GUI operations are executed in the main thread. You can use `self.root.after` or a `queue` for communication between threads.

Here’s how you can fix the code:

1. **Create the 2FA dialog in the main thread**: Always handle GUI tasks in the main thread.
2. **Use a queue for communication between threads**: The main thread can wait for the result from the worker thread.

This approach ensures proper synchronization and prevents conflicts between threads while interacting with Tkinter.



Update:
bugs fixes and more user experience.
New feature that skip pictures that you have already on you're pc:
![image](https://github.com/user-attachments/assets/b88929af-5679-402e-95ce-fc490bc86f93)

![image](https://github.com/user-attachments/assets/ad28e54e-f956-468a-bcc5-4b536332b614)



-------------------------------------------------------------------------------------------
![Capture](https://github.com/user-attachments/assets/9257bb54-131c-4021-b5a0-6596d2185b3a)


Downloaded 2344 files for 25 minutes...
![Capture 2](https://github.com/user-attachments/assets/d2494db7-4535-45b8-8b10-18fdb79958af)
