import pywhatkit as kit
import time
import random

clients =  [
    "+919820223473",
    "+919987099250",
] # add more numbers
message = """Hii

This is Saad from IndiBrick.

In a market where Mumbai prices shift weekly, the most valuable opportunities stay off-market shared only through private networks.

At IndiBrick, we work directly with top builders & property owners  to secure exclusive, pre-market homes verified, premium, and perfect for fast decision-makers.
 
We’ve just received new 1BHK–3BHK premium units in Andheri, Powai, Lower Parel & Navi Mumbai. These listings won’t stay available long. 

Reply INFO to receive the curated list.

PS: We also assist with premium rentals in the same neighborhoods."""

for number in clients:
    try:
        kit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
        print(f"Message sent to {number}")
    except Exception as e:
        print(f"Error sending to {number}: {e}")

    delay = random.randint(30, 45)
    print(f"Waiting {delay} seconds...")
    time.sleep(delay)
