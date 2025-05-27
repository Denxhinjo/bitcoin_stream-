from supabase import create_client, Client

SUPABASE_URL = "supabase_url"
SUPABASE_KEY = "supabase_key"

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
