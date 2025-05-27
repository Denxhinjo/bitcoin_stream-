from supabase import create_client, Client

SUPABASE_URL = "https://watlewvfnqltujhkzfzd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndhdGxld3ZmbnFsdHVqaGt6ZnpkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgyNTg2NTEsImV4cCI6MjA2MzgzNDY1MX0.j1MmQ2xJTkUEnW1dMX0r17BiI3OuiPvc0Tyyr1uPsQg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_tx(tx):
    supabase.table("transactions").insert({
        "hash": tx["hash"],
        "total_btc": tx["total_btc"],
        "fee_btc": tx["fee_btc"],
        "timestamp": tx["time"]
    }).execute()