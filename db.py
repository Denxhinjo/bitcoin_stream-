from supabase import create_client, Client

SUPABASE_URL = "supabase_url"
SUPABASE_KEY = "supabase_key"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_tx(tx):
    supabase.table("transactions").insert({
        "hash": tx["hash"],
        "total_btc": tx["total_btc"],
        "fee_btc": tx["fee_btc"],
        "timestamp": tx["time"]
    }).execute()
