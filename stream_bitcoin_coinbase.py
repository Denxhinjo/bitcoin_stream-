import json
import uuid
from datetime import datetime
from websocket import WebSocketApp
from supabase import create_client, Client

# Supabase credentials (replace with your actual values)
SUPABASE_URL = "supabase_url"
SUPABASE_KEY = "supabase_key"
TABLE_NAME = "table_coinbase"  # Replace with the actual name

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Coinbase WebSocket URL
COINBASE_WS_URL = "wss://ws-feed.exchange.coinbase.com"

def on_message(ws, message):
    data = json.loads(message)

    if data['type'] == 'match':
        record = {
            "id": str(uuid.uuid4()),
            "trade_id": data.get("trade_id"),
            "product_id": data.get("product_id"),
            "price": float(data.get("price", 0)),
            "size": float(data.get("size", 0)),
            "total_usd": float(data.get("price", 0)) * float(data.get("size", 0)),
            "timestamp": data.get("time", datetime.utcnow().isoformat())
        }

        print(f"Inserting trade: {record}")

        try:
            response = supabase.table(TABLE_NAME).insert(record).execute()
            print(f"Inserted: {response}")
        except Exception as e:
            print(f"Error inserting to Supabase: {e}")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    subscribe_message = {
        "type": "subscribe",
        "channels": [{"name": "matches", "product_ids": ["BTC-USD"]}]
    }
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to BTC-USD matches")

if __name__ == "__main__":
    ws_app = WebSocketApp(
        COINBASE_WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    print("Starting Coinbase WebSocket stream...")
    ws_app.run_forever()
