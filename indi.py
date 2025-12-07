import pywhatkit as kit
import time

clients = ["+919867207760", "+918691952960"]
message = "Hello! This is an update from our team."

for number in clients:
    try:
        kit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
        print(f"Message sent to {number}")
    except Exception as e:
        print(f"Error sending to {number}: {e}")
    
    time.sleep(5)  # small pause for safety

