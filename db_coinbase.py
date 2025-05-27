from supabase import create_client, Client

SUPABASE_URL = "https://watlewvfnqltujhkzfzd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndhdGxld3ZmbnFsdHVqaGt6ZnpkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgyNTg2NTEsImV4cCI6MjA2MzgzNDY1MX0.j1MmQ2xJTkUEnW1dMX0r17BiI3OuiPvc0Tyyr1uPsQg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_tx(tx):
    supabase.table("transactions_coinbase").insert({
        "trade_id": tx["trade_id"],         # int
        "product_id": tx["product_id"],     # text
        "price": str(tx["price"]),          # numeric as string
        "size": str(tx["size"]),            # numeric as string
        "total_usd": str(tx["total_usd"]),  # numeric as string
        "timestamp": tx["timestamp"]             # ISO 8601 string
    }).execute()