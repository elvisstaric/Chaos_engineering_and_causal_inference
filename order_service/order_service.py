import aiohttp
import asyncio
from fastapi import FastAPI, HTTPException, Header, Request, Path
import uuid
import json
import os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY
from starlette.responses import Response
import time

app = FastAPI(title="Order Service")
REQUEST_COUNT = Counter('order_service_requests_total', 'Ukupan broj HTTP zahtjeva', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('order_service_request_latency_seconds', 'Latencija HTTP zahtjeva', ['endpoint'])
ERROR_COUNT = Counter(
    'order_service_errors_total',
    'Broj grešaka HTTP zahtjeva',
    ['method', 'endpoint', 'http_status_class']
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    REQUEST_LATENCY.labels(request.url.path).observe(process_time)
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    
    status_class = f"{response.status_code // 100}xx"
    if status_class in ['4xx', '5xx']:
        ERROR_COUNT.labels(request.method, request.url.path, status_class).inc()

    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

ORDERS_FILE = "./orders.json"
CART_SERVICE_URL = "http://toxiproxy:8602"

async def get_cart(retries=3, timeout_sec=5):
    for attempt in range(retries):
        try:
            timeout = aiohttp.ClientTimeout(total=timeout_sec)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{CART_SERVICE_URL}/cart") as response:
                    if response.status != 200:
                        raise HTTPException(status_code=400, detail="Cannot retrieve cart or cart is empty")
                    return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError):
            if attempt == retries - 1:
                raise HTTPException(status_code=503, detail="Cart service unavailable")
            await asyncio.sleep(1)

async def clear_cart(retries=3, timeout_sec=5):
    for attempt in range(retries):
        try:
            timeout = aiohttp.ClientTimeout(total=timeout_sec)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.delete(f"{CART_SERVICE_URL}/cart") as response:
                    if response.status != 200:
                        raise HTTPException(status_code=500, detail="Failed to clear cart")
                    return
        except (aiohttp.ClientError, asyncio.TimeoutError):
            if attempt == retries - 1:
                raise HTTPException(status_code=503, detail="Cart service unavailable")
            await asyncio.sleep(1)

def load_orders():
    if not os.path.exists(ORDERS_FILE) or os.path.getsize(ORDERS_FILE) == 0:
        return []
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)

def save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

@app.post("/orders")
async def create_order(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: No valid token provided")
    
    token = authorization.split(" ")[1]
    if token != "valid-token":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid token")
    cart_items = await get_cart()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    orders = load_orders()
    order_id = str(uuid.uuid4())
    order_data = {
        "order_id": order_id,
        "items": cart_items,
        "status": "created"
    }
    orders.append(order_data)
    save_orders(orders)
    await clear_cart()
    return {"order_id": order_id, "status": "created"}

@app.get("/orders")
async def get_all_orders():
    orders = load_orders()
    return orders

@app.get("/orders/{order_id}")
async def get_order(order_id: str = Path(..., description="ID narudžbe")):
    orders = load_orders()
    for order in orders:
        if order["order_id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Narudžba nije pronađena")