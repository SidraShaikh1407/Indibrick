#gui for indibrick bulk whatsapp message sending
import tkinter as tk
from tkinter import messagebox
import pywhatkit as kit
import time
import random
import re

def send_messages():
    numbers_text = entry_numbers.get("1.0", tk.END).strip()
    message = entry_message.get("1.0", tk.END).strip()

    if not numbers_text or not message:
        messagebox.showwarning("Input Error", "Please enter numbers and a message!")
        return

    numbers_list = numbers_text.split("\n")
    valid_numbers = []
    invalid_numbers = []

    for num in numbers_list:
        num = num.strip()
        if re.fullmatch(r"\d{10}", num):
            valid_numbers.append("+91" + num)
        else:
            invalid_numbers.append(num)

    total_numbers = len(numbers_list)
    valid_count = len(valid_numbers)
    invalid_format_count = len(invalid_numbers)
    sent_count = 0
    whatsapp_invalid = []

    if valid_count == 0:
        messagebox.showerror("Error", "No valid numbers found.")
        return

    status_label.config(text="Connecting to WhatsApp...")

    for i, number in enumerate(valid_numbers, start=1):
        try:
            # MUST keep tab open for WhatsApp to load
            kit.sendwhatmsg_instantly(number, message, wait_time=15, tab_close=False)
            sent_count += 1
            print(f"Message attempted for {number}")

            time.sleep(8)  # extra wait for typing + clicking send
            status_label.config(text=f"Sent {sent_count}/{valid_count}")

        except Exception as e:
            print(f"Error sending to {number}: {e}")
            whatsapp_invalid.append(number)

        if i < valid_count:
            delay = random.randint(30,39)
            status_label.config(text=f"Waiting {delay}s before next...")
            print(f"Waiting {delay} seconds...\n")
            time.sleep(delay)

    summary = (
        f"📊 Sending Summary\n\n"
        f"Total Input: {total_numbers}\n"
        f"Valid Format: {valid_count}\n"
        f"Invalid Format: {invalid_format_count}\n"
        f"Sent Successfully: {sent_count}\n"
        f"Failed / Not on WhatsApp: {len(whatsapp_invalid)}"
    )

    messagebox.showinfo("Summary", summary)
    status_label.config(text="Completed!")

root = tk.Tk()
root.title("WhatsApp Sender Pro")
root.geometry("500x580")
root.config(bg="#eaf7ff")

tk.Label(root, text="IndiBrick ", bg="#0d6efd", fg="white",
         font=("Arial", 17, "bold"), pady=10).pack(fill="x")

tk.Label(root, text="Enter 10-digit Numbers (one per line):", bg="#eaf7ff",
         font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
entry_numbers = tk.Text(root, height=8, width=46, font=("Arial", 10))
entry_numbers.pack(pady=6)

tk.Label(root, text="Enter Message:", bg="#eaf7ff",
         font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
entry_message = tk.Text(root, height=8, width=46, font=("Arial", 10))
entry_message.pack(pady=6)

tk.Button(root, text="Send Messages", bg="#0d6efd", fg="white",
          font=("Arial", 13, "bold"),
          command=send_messages).pack(pady=15)

status_label = tk.Label(root, text="Waiting to start...", bg="#eaf7ff",
                        font=("Arial", 11, "bold"))
status_label.pack(pady=5)

root.mainloop()
