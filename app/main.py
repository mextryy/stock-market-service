from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import redis
import os
import json

app = FastAPI()

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

# data models 

class StockItem(BaseModel):
    name: str
    quantity: int

class BankState(BaseModel):
    stocks: list[StockItem]

class TradeRequest(BaseModel):
    type: str  # supported values: "buy", "sell"


def log_action(action_type, wallet_id, stock_name):
    log_entry = json.dumps({"type": action_type, "wallet_id": wallet_id, "stock_name": stock_name})
    r.rpush("audit_log", log_entry)

# API endpoints

@app.post("/wallets/{wallet_id}/stocks/{stock_name}")
def trade(wallet_id: str, stock_name: str, request: TradeRequest):
    
    bank_quantity = r.hget("bank:stocks", stock_name)
    if bank_quantity is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    bank_quantity = int(bank_quantity)
    wallet_key = f"wallet:{wallet_id}"
    wallet_stock_quantity = int(r.hget(wallet_key, stock_name) or 0)

    if request.type == "buy":
        if bank_quantity <= 0:
            raise HTTPException(status_code=400, detail="No stock in bank")
        
        r.hincrby("bank:stocks", stock_name, -1)
        r.hincrby(wallet_key, stock_name, 1)
        log_action("buy", wallet_id, stock_name)

    elif request.type == "sell":
        if wallet_stock_quantity <= 0:
            raise HTTPException(status_code=400, detail="No stock in wallet")
        
        r.hincrby("bank:stocks", stock_name, 1)
        r.hincrby(wallet_key, stock_name, -1)
        log_action("sell", wallet_id, stock_name)
    
    return Response(status_code=200)

@app.get("/wallets/{wallet_id}")
def get_wallet(wallet_id: str):
    wallet_key = f"wallet:{wallet_id}"
    all_stocks = r.hgetall(wallet_key)
    stocks_list = [{"name": name, "quantity": int(qty)} for name, qty in all_stocks.items()]
    return {"id": wallet_id, "stocks": stocks_list}

@app.get("/wallets/{wallet_id}/stocks/{stock_name}")
def get_wallet_stock(wallet_id: str, stock_name: str):
    wallet_key = f"wallet:{wallet_id}"
    qty = r.hget(wallet_key, stock_name)
    return int(qty) if qty else 0

@app.get("/stocks")
def get_bank_stocks():
    all_stocks = r.hgetall("bank:stocks")
    stocks_list = [{"name": name, "quantity": int(qty)} for name, qty in all_stocks.items()]
    return {"stocks": stocks_list}

@app.post("/stocks")
def set_bank_stocks(state: BankState):
    r.delete("bank:stocks")
    for item in state.stocks:
        r.hset("bank:stocks", item.name, item.quantity)
    return Response(status_code=200)

@app.get("/log")
def get_log():
    logs = r.lrange("audit_log", 0, -1)
    return {"log": [json.loads(l) for l in logs]}

@app.post("/chaos")
def chaos():
    """Simulates an unexpected instance failure for High availability testing."""
    import os
    os._exit(1)