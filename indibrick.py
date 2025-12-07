import threading
import time
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, WebDriverException

driver = None
stop_flag = False

sent_count = 0
invalid_format_count = 0
notwhatsapp_count = 0

def start_sending():
    global driver, stop_flag
    global sent_count, invalid_format_count, notwhatsapp_count

    # Reset counters
    sent_count = 0
    invalid_format_count = 0
    notwhatsapp_count = 0
    stop_flag = False
    update_status()

    numbers_text = txt_numbers.get("1.0", tk.END).strip()
    message = txt_message.get("1.0", tk.END).strip()

    if not numbers_text:
        messagebox.showerror("Error", "Please enter phone numbers!")
        return
    
    if not message:
        messagebox.showerror("Error", "Please enter a message!")
        return

    numbers = numbers_text.split("\n")
    total = len(numbers)

    log("🚀 Starting WhatsApp Auto Sender...")
    
    btn_start.config(state="disabled")
    btn_stop.config(state="normal")

    # Browser setup
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=whatsapp_profile")

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException:
        log("❌ ChromeDriver missing or incompatible!")
        return

    driver.get("https://web.whatsapp.com/")
    log("📌 Scan QR (if needed)...")
    time.sleep(12)

    for i, number in enumerate(numbers, start=1):
        if stop_flag:
            log("\n⛔ Stopped by user!")
            break

        number = number.strip()
        log(f"\n➡ Processing ({i}/{total}): {number}")

        # Validate phone format
        if len(number) != 10 or not number.isdigit():
            invalid_format_count += 1
            update_status()
            log("❌ Invalid number format")
            continue

        driver.get(f"https://web.whatsapp.com/send?phone=91{number}&text=")
        time.sleep(10)

        # Detect Not On WhatsApp popup
        try:
            driver.find_element(By.XPATH, "//div[contains(@data-animate-modal-popup,'true')]")
            notwhatsapp_count += 1
            update_status()
            log("⚠ Number not on WhatsApp")
            continue
        except NoSuchElementException:
            pass

        try:
            # Locate chat message box
            input_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
            input_box.click()
            input_box.send_keys(message)
            time.sleep(1)

            send_btn = driver.find_element(By.XPATH, "//span[@data-icon='send']")
            send_btn.click()

            sent_count += 1
            update_status()
            log(f"📨 Sent successfully! ({sent_count})")

            delay = random.randint(35, 50)
            log(f"⏳ Waiting {delay}s for next message...")
            time.sleep(delay)

        except Exception:
            notwhatsapp_count += 1
            update_status()
            log("❌ Failed: Could not detect chat input/send button")
            continue

    log("\n🎯 Sending Completed!")

    btn_start.config(state="normal")
    btn_stop.config(state="disabled")
    
    driver.quit()

def stop_sending():
    global stop_flag
    stop_flag = True
    log("\n🛑 Stop requested, finishing current task...")

def update_status():
    lbl_sent.config(text=f"Sent: {sent_count}")
    lbl_invalid.config(text=f"Invalid: {invalid_format_count}")
    lbl_notwp.config(text=f"Not WhatsApp: {notwhatsapp_count}")

def log(msg):
    txt_log.insert(tk.END, msg + "\n")
    txt_log.see(tk.END)

# GUI Setup
root = tk.Tk()
root.title("WhatsApp Bulk Sender - Pro Edition")
root.geometry("670x620")
root.resizable(False, False)

tk.Label(root, text="Enter 10-Digit Numbers (One Per Line):", font=("Arial", 11, "bold")).pack(anchor="w", pady=5, padx=10)
txt_numbers = scrolledtext.ScrolledText(root, height=8, width=70)
txt_numbers.pack()

tk.Label(root, text="Enter Message:", font=("Arial", 11, "bold")).pack(anchor="w", pady=5, padx=10)
txt_message = scrolledtext.ScrolledText(root, height=6, width=70)
txt_message.pack()

frame = tk.Frame(root)
frame.pack(pady=10)

btn_start = tk.Button(frame, text="Start Sending", bg="green", fg="white", width=15, font=("Arial", 12, "bold"),
                      command=lambda: threading.Thread(target=start_sending, daemon=True).start())
btn_start.grid(row=0, column=0, padx=10)

btn_stop = tk.Button(frame, text="Stop", bg="red", fg="white", width=10, font=("Arial", 12, "bold"),
                     state="disabled", command=stop_sending)
btn_stop.grid(row=0, column=1, padx=10)

lbl_sent = tk.Label(root, text="Sent: 0", fg="green", font=("Arial", 12, "bold"))
lbl_sent.pack()

lbl_invalid = tk.Label(root, text="Invalid: 0", fg="orange", font=("Arial", 12, "bold"))
lbl_invalid.pack()

lbl_notwp = tk.Label(root, text="Not WhatsApp: 0", fg="red", font=("Arial", 12, "bold"))
lbl_notwp.pack()

tk.Label(root, text="\nLogs:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
txt_log = scrolledtext.ScrolledText(root, height=14, width=70)
txt_log.pack()

root.mainloop()

