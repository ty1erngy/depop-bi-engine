"""
clean_depop.py
Cleans a raw Depop sales export so it loads into BigQuery.

What it does:
  1. Reads the raw export (handles descriptions that span multiple lines)
  2. Removes buyer names and addresses (privacy)
  3. Drops the long Description column (not needed for analysis)
  4. Removes $ signs and Excel junk like ="-" from money columns
  5. Converts dates to YYYY-MM-DD
  6. Renames columns to snake_case (no spaces) for BigQuery
  7. Adds source + acquisition_cost columns (default: closet / 0.00)
  8. Saves a clean CSV ready to upload

How to run:
  python clean_depop.py "Depop Sales 07_30_2026 - 10_29_2026.csv"
"""

import re
import sys
import pandas as pd

RAW_FILE = sys.argv[1] if len(sys.argv) > 1 else "depop_raw.csv"
OUT_FILE = "depop_sales_cleaned.csv"

# ---------- 1. Read the raw export ----------
# pandas handles quoted text with line breaks and emojis automatically
df = pd.read_csv(RAW_FILE, dtype=str, encoding="utf-8")
print(f"Loaded {len(df)} sales and {len(df.columns)} columns")
print("Original columns:", list(df.columns))

# ---------- 2. Remove private buyer information ----------
# Exact Depop column names that identify a person. Money columns that
# mention "buyer" (shipping cost, marketplace fee, refunds) are kept.
PRIVATE = {"buyer", "name", "address line 1", "address line 2", "city",
           "state", "post code", "zip", "country", "phone", "email"}

private_cols = [c for c in df.columns if c.lower().strip() in PRIVATE]
df = df.drop(columns=private_cols)
print("Removed private columns:", private_cols)

# ---------- 3. Drop the long description ----------
df = df.drop(columns=[c for c in df.columns if c.lower().strip() == "description"])

# ---------- 4. Rename columns to snake_case ----------
def snake(name):
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")

df.columns = [snake(c) for c in df.columns]

# ---------- 5. Clean junk values everywhere ----------
junk = {'="-"': "", "=\"-\"": "", "-": "", "N/A": "", "n/a": "", "nan": ""}
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
df = df.replace(junk)
# Remove the Excel ="..." wrapper if any remain, e.g. ="123" -> 123
df = df.apply(lambda col: col.str.replace(r'^="(.*)"$', r"\1", regex=True)
              if col.dtype == "object" else col)

# ---------- 6. Money columns: remove $ and commas, make numbers ----------
MONEY_WORDS = ["price", "cost", "total", "fee", "tax", "amount", "payout"]
money_cols = [
    c for c in df.columns
    if any(w in c for w in MONEY_WORDS)
    and "date" not in c
    and c != "bundle_amount_of_items"
]
for c in money_cols:
    df[c] = (df[c].str.replace("$", "", regex=False)
                  .str.replace(",", "", regex=False))
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
print("Money columns cleaned:", money_cols)

# ---------- 7. Date columns: make YYYY-MM-DD ----------
date_cols = [c for c in df.columns if "date" in c]
for c in date_cols:
    df[c] = pd.to_datetime(df[c], format="%m/%d/%Y", errors="coerce").dt.strftime("%Y-%m-%d")
print("Date columns cleaned:", date_cols)
# ---------- 7b. Tidy columns Depop leaves blank ----------
# SKU is never filled in on Depop, so drop it
if "sku" in df.columns and df["sku"].replace("", pd.NA).isna().all():
    df = df.drop(columns=["sku"])

# Single items count as 1; bundle rows keep Depop's count, others in the bundle get 0
if "bundle_amount_of_items" in df.columns:
    is_bundle = df["bundle"].str.lower().eq("yes")
    count = pd.to_numeric(df["bundle_amount_of_items"], errors="coerce")
    df["bundle_amount_of_items"] = count.where(is_bundle, 1).fillna(0).astype(int)
# ---------- 8. Add source and acquisition_cost ----------
# Default every item to closet / $0. Edit rows in the output file afterward
# for anything you thrifted or bought, using the REAL price you paid.
if "source" not in df.columns:
    df["source"] = "closet"
if "acquisition_cost" not in df.columns:
    df["acquisition_cost"] = 0.0
# Single items count as 1; bundle rows keep Depop's count, others in the bundle get 0
if "bundle_amount_of_items" in df.columns:
    is_bundle = df["bundle"].str.lower().eq("yes")
    count = pd.to_numeric(df["bundle_amount_of_items"], errors="coerce")
    df["bundle_amount_of_items"] = count.where(is_bundle, 1).fillna(0).astype(int)
# ---------- 9. Quick checks ----------
print("\nChecks:")
print(" Rows:", len(df))
print(" Blank sale dates:", df[date_cols[0]].isna().sum() if date_cols else "no date column")
print(" Source values:", df["source"].value_counts().to_dict())

# ---------- 10. Save ----------
df.to_csv(OUT_FILE, index=False)
print(f"\nSaved {OUT_FILE}")
print("Final columns (use these for your BigQuery schema):")
for c in df.columns:
    print("  ", c)