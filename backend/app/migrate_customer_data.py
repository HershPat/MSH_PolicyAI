import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = "https://zojeptztgkfuudnoeydr.supabase.co"
SUPABASE_KEY = os.getenv("REST_API_KEY")

if not SUPABASE_KEY:
    raise ValueError("REST_API_KEY not found in environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

EXCEL_PATH = "Policy_Billing_AI_Chat_Test_Data.xlsx"

sheet_to_table = {
    "Customer": "customer",
    "Agent": "agent",
    "Policy": "policy",
    "Property": "property",
    "Coverage": "coverage",
    "BillingAccount": "billing_account",  # note underscore
    "Payment": "payment",
    "Cancellation": "cancellation",
    "Claim": "claim",
    "ChatInteraction": "chat_interaction",
    "AI_Metadata": "ai_metadata",
}


def process_and_insert_sheet(sheet_name):
    table_name = sheet_to_table.get(sheet_name)
    if not table_name:
        print(f"❌ No matching table for sheet '{sheet_name}', skipping...")
        return
    
    print(f"Processing sheet: {sheet_name} → table: {table_name}")
    df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name)
    df = df.fillna("")
    
    # Convert datetime columns to ISO strings (Supabase expects JSON-serializable types)
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Convert DataFrame to list of dicts
    rows = df.to_dict(orient="records")
    
    if not rows:
        print(f"No data found in sheet '{sheet_name}' to insert.")
        return
    
    # Insert rows into Supabase table
    response = supabase.table(table_name).upsert(rows).execute()

    # if response.error is None:
    #     print(f"✅ Upserted {len(rows)} rows into '{table_name}'")
    # else:
    #     print(f"❌ Upsert failed: {response.error.message}")

def main():
    # Load Excel file and get all sheet names
    xls = pd.ExcelFile(EXCEL_PATH)
    for sheet_name in xls.sheet_names:
        process_and_insert_sheet(sheet_name)

if __name__ == "__main__":
    main()
