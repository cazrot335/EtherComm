import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

# Backend URL
API_URL = "http://127.0.0.1:5000"

class DecencordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Decencord - Decentralized Chat")
        self.root.geometry("600x500")

        # Channel ID input
        tk.Label(root, text="Channel ID:").pack()
        self.channel_id_entry = tk.Entry(root)
        self.channel_id_entry.pack(pady=5)

        # Message input
        tk.Label(root, text="Your Message:").pack()
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(pady=5)

        # Send button
        self.send_button = tk.Button(root, text="Send Message", command=self.send_message)
        self.send_button.pack(pady=5)

        # Get messages button
        self.get_button = tk.Button(root, text="Get Messages", command=self.get_messages)
        self.get_button.pack(pady=5)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(root, width=70, height=20)
        self.chat_display.pack(pady=10)

    def send_message(self):
        channel_id = self.channel_id_entry.get().strip()
        message = self.message_entry.get().strip()
        if not channel_id or not message:
            messagebox.showerror("Error", "Channel ID and Message cannot be empty")
            return

        try:
            response = requests.post(f"{API_URL}/send_message", json={"channel_id": channel_id, "message": message})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Message sent successfully!")
                self.message_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Failed to send message: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_messages(self):
        channel_id = self.channel_id_entry.get().strip()
        if not channel_id:
            messagebox.showerror("Error", "Channel ID cannot be empty")
            return

        try:
            response = requests.get(f"{API_URL}/get_messages/{channel_id}")
            if response.status_code == 200:
                messages = response.json().get("messages", [])
                self.chat_display.delete(1.0, tk.END)
                for msg in messages:
                    self.chat_display.insert(tk.END, f"{msg}\n")
            else:
                messagebox.showerror("Error", f"Failed to fetch messages: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DecencordGUI(root)
    root.mainloop()
