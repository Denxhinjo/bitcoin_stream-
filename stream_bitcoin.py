import os
import websocket
import json
import threading
from datetime import datetime, timezone
from collections import deque
from db import insert_tx
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env

SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

MAX_TX = 100
tx_store = deque(maxlen=MAX_TX)
store_lock = threading.Lock()

def on_message(ws, message):
    data = json.loads(message)
    print(json.dumps(data, indent=2))

    tx_hash = data.get('hash')
    outputs = data.get('outputs', [])
    total_satoshis = sum(o.get('value', 0) for o in outputs)
    total_btc = total_satoshis / 1e8  # convert satoshis to BTC
    fee_satoshis = data.get('fees', 0)
    fee_btc = fee_satoshis / 1e8

    print("New TX:")
    print("Hash:", tx_hash)
    print("Total:", total_btc, "BTC")
    print("-" * 30)

    tx_data = {
        'hash': tx_hash,
        'total_btc': total_btc,
        'fee_btc': fee_btc,
        'time': datetime.now(timezone.utc).isoformat() 
    }

    with store_lock:
        tx_store.append(tx_data)
        insert_tx(tx_data)  # ✅ this sends data to your cloud DB

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")
    # Subscribes to unconfirmed transactions
    ws.send(json.dumps({ 
        "event": "unconfirmed-tx",
        "token": "0edb21fea5af42f18cfb7549780360c5"
    }))

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://socket.blockcypher.com/v1/btc/main",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()
