import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Global variables
driver = None
stop_flag = False
sent_count = 0
invalid_format_count = 0
notwhatsapp_count = 0

def update_status():
    status_label.config(
        text=f"Sent: {sent_count} | Invalid: {invalid_format_count} | Not WhatsApp: {notwhatsapp_count}"
    )

def send_whatsapp_message(phone, message):
    global sent_count, invalid_format_count, notwhatsapp_count

    if not phone.isdigit() or len(phone) != 10:
        invalid_format_count += 1
        update_status()
        return

    phone = "+91" + phone
    driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={message}")

    time.sleep(random.randint(8, 12))

    try:
        send_btn = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
        send_btn.click()
        sent_count += 1
        update_status()
        return

    except:
        try:
            alert = driver.switch_to.alert
            alert.accept()
            notwhatsapp_count += 1
            update_status()
        except:
            pass

def start_sending():
    global driver, stop_flag
    global sent_count, invalid_format_count, notwhatsapp_count

    sent_count = 0
    invalid_format_count = 0
    notwhatsapp_count = 0
    stop_flag = False
    update_status()

    numbers = numbers_box.get("1.0", tk.END).strip().split("\n")
    message = message_box.get("1.0", tk.END).strip()

    if not numbers or not message:
        messagebox.showerror("Error", "Enter numbers and message!")
        return

    log.insert(tk.END, "Starting WhatsApp Auto Sender...\n")
    log.yview(tk.END)

    try:
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=whatsapp_session")
        chrome_options.add_argument("--start-maximized")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.get("https://web.whatsapp.com/")
        log.insert(tk.END, "📱 Scan QR if required...\n")
        log.yview(tk.END)

        time.sleep(15)

        for number in numbers:
            if stop_flag:
                break
            log.insert(tk.END, f"Sending to {number}...\n")
            log.yview(tk.END)

            send_whatsapp_message(number, message)
            time.sleep(random.randint(5, 10))

        log.insert(tk.END, "\n✔ Process Completed!\n")
        log.yview(tk.END)

    except Exception as e:
        log.insert(tk.END, f"Error: {e}\n")

def stop_sending():
    global stop_flag
    stop_flag = True
    log.insert(tk.END, "⛔ Stopping...\n")
    log.yview(tk.END)


# UI Setup
root = tk.Tk()
root.title("WhatsApp Auto Sender")
root.geometry("650x650")

tk.Label(root, text="Mobile Numbers (10 digits only):").pack()
numbers_box = scrolledtext.ScrolledText(root, width=60, height=10)
numbers_box.pack()

tk.Label(root, text="Message:").pack()
message_box = scrolledtext.ScrolledText(root, width=60, height=5)
message_box.pack()

start_btn = tk.Button(root, text="Start Sending", bg="green", fg="white", command=start_sending)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop", bg="red", fg="white", command=stop_sending)
stop_btn.pack()

status_label = tk.Label(root, text="Sent: 0 | Invalid: 0 | Not WhatsApp: 0", font=("Arial", 12), fg="blue")
status_label.pack(pady=5)

tk.Label(root, text="Logs:").pack()
log = scrolledtext.ScrolledText(root, width=65, height=20)
log.pack()

root.mainloop()
