from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
import aiohttp
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY
from starlette.responses import Response
import time
import aiohttp
import asyncio

app = FastAPI(title="Cart Service")

REQUEST_COUNT = Counter('cart_service_requests_total', 'Ukupan broj HTTP zahtjeva', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('cart_service_request_latency_seconds', 'Latencija HTTP zahtjeva', ['endpoint'])
ERROR_COUNT = Counter(
    'cart_service_errors_total',
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

class CartItem(BaseModel):
    product_id: str
    quantity: int

cart = []
INVENTORY_SERVICE_URL = "http://toxiproxy:8601"

@app.get("/cart", response_model=List[CartItem])
async def get_cart():
    return cart

async def check_inventory(product_id: str, requested_qty: int, retries=3, timeout_sec=5):
    for attempt in range(retries):
        try:
            timeout = aiohttp.ClientTimeout(total=timeout_sec)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{INVENTORY_SERVICE_URL}/products/{product_id}") as response:
                    if response.status != 200:
                        raise HTTPException(status_code=404, detail="Product not found in inventory")
                    product = await response.json()
                    if product["quantity"] < requested_qty:
                        return False
                    return True
        except (aiohttp.ClientError, asyncio.TimeoutError):
            if attempt == retries - 1:
                raise HTTPException(status_code=503, detail="Inventory service unavailable")
            await asyncio.sleep(1)

@app.post("/cart", response_model=CartItem)
async def add_to_cart(item: CartItem):
    is_available = await check_inventory(item.product_id, item.quantity)
    if not is_available:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    for cart_item in cart:
        if cart_item.product_id == item.product_id:
            new_qty = cart_item.quantity + item.quantity
            is_available = await check_inventory(item.product_id, new_qty)
            if not is_available:
                raise HTTPException(status_code=400, detail="Not enough stock available for the increased quantity")
            cart_item.quantity = new_qty
            return cart_item

    cart.append(item)
    return item

@app.put("/cart/{product_id}", response_model=CartItem)
async def update_cart_item(product_id: str, quantity: int):
    for cart_item in cart:
        if cart_item.product_id == product_id:
            if quantity <= 0:
                cart.remove(cart_item)
                return {"detail": "Item removed from cart"}
            cart_item.quantity = quantity
            return cart_item
    raise HTTPException(status_code=404, detail="Item not found in cart")

@app.delete("/cart/{product_id}")
async def delete_cart_item(product_id: str):
    for cart_item in cart:
        if cart_item.product_id == product_id:
            cart.remove(cart_item)
            return {"detail": "Item removed from cart"}
    raise HTTPException(status_code=404, detail="Item not found in cart")

@app.delete("/cart")
async def clear_cart():
    cart.clear()
    return {"detail": "Cart cleared"}
