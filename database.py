import re
import pandas as pd
from rapidfuzz import fuzz

# ---------------- CONFIG ----------------
CHAT_FILE = "RealEstateGroup.txt"
OUTPUT_CSV = "real_estate_advanced.csv"
DEDUP_THRESHOLD = 88  # fuzzy match score for duplicates
# -----------------------------------------

# ---------------- REGEX PATTERNS ----------------

phone_pattern = re.compile(r"(?:\+91[-\s]?)?([6-9]\d{9})\b")

bhk_pattern = re.compile(r"\b([1-9]\s?BHK)\b", re.I)

carpet_pattern = re.compile(r"\bcarpet\s?[:\-]? ?(\d{2,5}\s?(sqft|sq ft|sq\.ft))\b", re.I)
builtup_pattern = re.compile(r"\bbuilt[- ]?up\s?[:\-]? ?(\d{2,5}\s?(sqft|sq ft|sq\.ft))\b", re.I)

generic_area_pattern = re.compile(r"\b\d{2,5}\s?(sqft|sq ft|sq\.ft|sqm)\b", re.I)

furnish_pattern = re.compile(r"\b(furnished|semi[- ]furnished|unfurnished)\b", re.I)

amenities_list = [
    "parking", "gym", "lift", "garden", "pool", "swimming", "clubhouse",
    "security", "power backup", "cctv", "kids", "play", "wifi"
]
amenities_pattern = re.compile("|".join([re.escape(a) for a in amenities_list]), re.I)

# Rent / Sale detection
rent_words = re.compile(r"\brent|lease\b", re.I)
sale_words = re.compile(r"\bsale|selling|outright|available\b", re.I)

rent_amount_pattern = re.compile(r"\b(\d{2,5})\s?(k|thousand)\b", re.I)
deposit_pattern = re.compile(r"\bdeposit\s?(\d{2,6}\s?(k|thousand|lac|lakh)?)\b", re.I)
sale_amount_pattern = re.compile(r"\b[\d\.]+\s?(cr|crore|lakh|lac)\b", re.I)

# Location list
locations = [
    "Andheri", "Bandra", "Borivali", "Thane", "Powai", "Goregaon",
    "Kandivali", "Malad", "Kurla", "Dadar", "Juhu", "Khar", "Navi Mumbai",
    "Panvel", "Vashi", "Chembur", "Mulund", "Ghatkopar"
]
location_pattern = re.compile("|".join(locations), re.I)

# Owner / Broker detection
owner_words = ["owner", "direct", "no broker", "owner listing"]
broker_words = ["broker", "agent", "realtor", "dealership"]

# WhatsApp format
line_pattern = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4}),.*? - (.*?): (.*)$")


# ---------------- LOGIC FUNCTIONS ----------------

def detect_type(msg):
    msg = msg.lower()
    if rent_words.search(msg):
        return "Rent"
    if sale_words.search(msg):
        return "Sale"
    if "cr" in msg or "crore" in msg:
        return "Sale"
    if "k" in msg or "thousand" in msg or "lakh" in msg:
        return "Rent"
    return "Unknown"

def detect_owner_broker(msg):
    m = msg.lower()
    if any(w in m for w in owner_words):
        return "Owner"
    if any(w in m for w in broker_words):
        return "Broker"
    return "Unknown"

def extract_rent(msg):
    m = rent_amount_pattern.findall(msg)
    return ", ".join(["".join(x) for x in m]) if m else ""

def extract_deposit(msg):
    m = deposit_pattern.findall(msg)
    return ", ".join([x[0] for x in m]) if m else ""

def extract_sale(msg):
    m = sale_amount_pattern.findall(msg)
    if not m:
        return ""
    # m returns only unit; we need the number+unit
    matches = re.findall(r"\b([\d\.]+\s?(?:cr|crore|lakh|lac))\b", msg, re.I)
    return ", ".join(matches)

def extract_carpet(msg):
    m = carpet_pattern.search(msg)
    return m.group(1) if m else ""

def extract_builtup(msg):
    m = builtup_pattern.search(msg)
    return m.group(1) if m else ""


# ---------------- PARSE CHAT ----------------

rows = []

with open(CHAT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        m = line_pattern.match(line)
        if not m:
            continue

        date, name, message = m.groups()

        phones = ", ".join(sorted(set(phone_pattern.findall(message))))
        bhk = ", ".join(sorted(set(bhk_pattern.findall(message))))

        carpet = extract_carpet(message)
        builtup = extract_builtup(message)

        # If only generic area is present
        generic = ", ".join(generic_area_pattern.findall(message))

        location = ", ".join(sorted(set(location_pattern.findall(message))))
        furnished = ", ".join(sorted(set(furnish_pattern.findall(message))))
        amenities = ", ".join(sorted(set(amenities_pattern.findall(message))))

        type_rs = detect_type(message)
        rent_amt = extract_rent(message)
        deposit = extract_deposit(message)
        sale_amt = extract_sale(message)

        owner_broker = detect_owner_broker(message)

        rows.append({
            "Name": name,
            "Number": phones,
            "Location": location,
            "BHK": bhk,
            "Carpet Area": carpet,
            "Built-up Area": builtup,
            "Generic Area": generic,
            "Furnishing": furnished,
            "Amenities": amenities,
            "Type (Rent/Sale)": type_rs,
            "Rent Amount": rent_amt,
            "Deposit": deposit,
            "Outright Price": sale_amt,
            "Owner/Broker": owner_broker,
            "Remarks (Full Message)": message
        })

df = pd.DataFrame(rows)

# ---------------- REMOVE DUPLICATES ----------------

final_rows = []
used = set()

for i in range(len(df)):
    if i in used:
        continue
    
    msg_i = df.iloc[i]["Remarks (Full Message)"]
    group = [i]
    
    for j in range(i + 1, len(df)):
        if j in used:
            continue
        msg_j = df.iloc[j]["Remarks (Full Message)"]
        
        if fuzz.token_sort_ratio(msg_i, msg_j) >= DEDUP_THRESHOLD:
            used.add(j)

    used.add(i)
    final_rows.append(df.iloc[i])

final_df = pd.DataFrame(final_rows)

# ---------------- SAVE CSV ----------------
final_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("CSV created:", OUTPUT_CSV)
print("Total:", len(df))
print("After removing duplicates:", len(final_df))

