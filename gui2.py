import tkinter as tk
from tkinter import messagebox
import pywhatkit as kit
import time
import random
import re
import pyautogui


def close_invalid_popup():
    """Auto-click 'OK' on WhatsApp popup if number is invalid"""
    try:
        time.sleep(3)
        pyautogui.press("enter")   # closes popup
    except:
        pass


def send_messages():
    numbers_text = entry_numbers.get("1.0", tk.END).strip()
    message = entry_message.get("1.0", tk.END).strip()

    if not numbers_text or not message:
        messagebox.showwarning("Input Error", "Please enter numbers and a message!")
        return

    numbers_list = numbers_text.split("\n")
    valid_numbers = []
    invalid_numbers = []

    # -----------------------------
    # AUTO-CLEAN + AUTO ADD +91
    # -----------------------------
    for num in numbers_list:
        num = num.strip()

        # remove +91 if user typed it
        num = num.replace("+91", "").strip()

        # remove spaces, hyphens, brackets etc.
        num = re.sub(r"[^\d]", "", num)

        # check if valid 10 digit
        if re.fullmatch(r"\d{10}", num):
            valid_numbers.append("+91" + num)   # add +91 automatically
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

    # --------------------------------------------------
    # SEND FIRST MESSAGE (WHATSAPP OPENS ONCE ONLY)
    # --------------------------------------------------
    try:
        kit.sendwhatmsg_instantly(valid_numbers[0], message, wait_time=15, tab_close=False)
        time.sleep(8)
        sent_count += 1
        status_label.config(text=f"Sent: {sent_count}/{valid_count}")
    except:
        whatsapp_invalid.append(valid_numbers[0])
        close_invalid_popup()

    # --------------------------------------------------
    # SEND TO ALL OTHER NUMBERS IN SAME TAB
    # --------------------------------------------------
    for number in valid_numbers[1:]:
        try:
            # open chat in same tab
            kit.search(f"https://wa.me/{number.replace('+', '')}")
            time.sleep(5)

            pyautogui.press("enter")
            time.sleep(4)

            pyautogui.typewrite(message)
            pyautogui.press("enter")

            sent_count += 1
            status_label.config(text=f"Sent: {sent_count}/{valid_count}")

        except:
            whatsapp_invalid.append(number)
            close_invalid_popup()

        delay = random.randint(25, 35)
        status_label.config(text=f"Waiting {delay}s before next...")
        time.sleep(delay)

    # --------------------------------------------------
    # SUMMARY POPUP
    # --------------------------------------------------
    summary = (
        f"📊 Sending Summary\n\n"
        f"Total Input: {total_numbers}\n"
        f"Valid Numbers: {valid_count}\n"
        f"Invalid Format: {invalid_format_count}\n"
        f"Sent Successfully: {sent_count}\n"
        f"Not on WhatsApp / Failed: {len(whatsapp_invalid)}"
    )

    messagebox.showinfo("Summary", summary)
    status_label.config(text="Completed!")


# ============================================================
# GUI DESIGN
# ============================================================

root = tk.Tk()
root.title("WhatsApp Sender Pro - IndiBrick")
root.geometry("500x580")
root.config(bg="#eaf7ff")

tk.Label(root, text="IndiBrick WhatsApp Sender", bg="#0d6efd", fg="white",
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

