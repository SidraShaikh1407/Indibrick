import re
import pandas as pd
from rapidfuzz import fuzz

# ----------------------------- CONFIG -----------------------------
CHAT_FILE = "RealEstateGroup.txt"
OUTPUT_CSV = "client_database_final.csv"
DEDUP_THRESHOLD = 88  # fuzzy duplicate cutoff
# -----------------------------------------------------------------

# REGEX patterns
phone_pattern = re.compile(r"(?:\+91[-\s]?)?([6-9]\d{9})\b")
budget_pattern = re.compile(r"\b[\d,]+(?:\.\d+)?\s?(L|Cr|Lakhs|Crore|lac|lakh)\b", re.I)
area_pattern = re.compile(r"\b\d{2,5}\s?(sq\.? ?ft|sqft|sq ft|sqm|sq m|m2)\b", re.I)

amenities_list = [
    "parking", "gym", "lift", "elevator", "garden", "pool", "swimming",
    "clubhouse", "security", "power backup", "cctv", "play", "kids"
]
amenities_pattern = re.compile("|".join([re.escape(a) for a in amenities_list]), re.I)

property_pattern = re.compile(r"\b(1BHK|2BHK|3BHK|4BHK|Flat|Apartment|Villa|Office|Shop|Plot)\b", re.I)

buyer_words = ["looking", "need", "want", "search", "buy", "required"]
seller_words = ["selling", "available", "for sale", "rent", "lease"]

project_indicators = ["Heights", "Towers", "Residency", "Greens", "Enclave", "Plaza", "Phase"]

# WhatsApp format
line_pattern = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4}),.*? - (.*?): (.*)$")

def detect_role(msg):
    msg_l = msg.lower()
    if any(w in msg_l for w in buyer_words):
        return "Buyer"
    if any(w in msg_l for w in seller_words):
        return "Seller"
    return "Unknown"

def extract_project(msg):
    words = re.findall(r"[A-Z][a-zA-Z0-9]+(?: [A-Z][a-zA-Z0-9]+){0,2}", msg)
    projects = [w for w in words if any(p.lower() in w.lower() for p in project_indicators)]
    return ", ".join(projects)

records = []

# ----------------------------- PARSE CHAT -----------------------------
with open(CHAT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        m = line_pattern.match(line)
        if not m:
            continue

        date, name, message = m.groups()

        phones = ", ".join(sorted(set(phone_pattern.findall(message))))
        budget = ", ".join(budget_pattern.findall(message))
        area = ", ".join(area_pattern.findall(message))
        amenities = ", ".join(set(amenities_pattern.findall(message)))
        prop_type = ", ".join(sorted(set(property_pattern.findall(message))))
        project = extract_project(message)
        role = detect_role(message)

        records.append({
            "Date": date,
            "Name": name,
            "Phone": phones,
            "Role": role,
            "Property Type": prop_type,
            "Budget": budget,
            "Carpet Area": area,
            "Amenities": amenities,
            "Project Names": project,
            "Message": message
        })

df = pd.DataFrame(records)

# ----------------------------- REMOVE DUPLICATES -----------------------------
final_rows = []
used = set()

for i in range(len(df)):
    if i in used:
        continue

    msg_i = df.iloc[i]["Message"]
    group = [i]

    for j in range(i + 1, len(df)):
        if j in used:
            continue

        msg_j = df.iloc[j]["Message"]

        if fuzz.token_sort_ratio(msg_i, msg_j) >= DEDUP_THRESHOLD:
            group.append(j)
            used.add(j)

    used.add(i)
    final_rows.append(df.iloc[i])

final_df = pd.DataFrame(final_rows)

# ----------------------------- SAVE CSV -----------------------------
final_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("---------------------------------------------------------")
print("CSV created successfully:", OUTPUT_CSV)
print("Total messages parsed:", len(df))
print("After duplicate removal:", len(final_df))
print("---------------------------------------------------------")
