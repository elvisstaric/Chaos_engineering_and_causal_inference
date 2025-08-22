from fastapi import FastAPI, HTTPException, Path, Request
from pydantic import BaseModel
from typing import List
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY
from starlette.responses import Response
import csv
import time


app = FastAPI(title="Inventory Service")

INVENTORY_FILE = "inventory.csv"

REQUEST_COUNT = Counter('inv_service_requests_total', 'Ukupan broj HTTP zahtjeva', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('inv_service_request_latency_seconds', 'Latencija HTTP zahtjeva', ['endpoint'])
ERROR_COUNT = Counter(
    'inv_service_errors_total',
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

class Product(BaseModel):
    product_id: str
    name: str
    quantity: int

def read_inventory():
    products = []
    try:
        with open(INVENTORY_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                products.append(Product(
                    product_id=row['product_id'],
                    name=row['product_name'],
                    quantity=int(row['quantity_in_stock'])
                ))
    except FileNotFoundError:
        pass
    return products

def write_inventory(products: List[Product]):
    with open(INVENTORY_FILE, 'w', newline='') as csvfile:
        fieldnames = ['product_id', 'product_name', 'quantity_in_stock']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in products:
            writer.writerow({
                'product_id': p.product_id,
                'product_name': p.name,
                'quantity_in_stock': p.quantity
            })

@app.get("/products", response_model=List[Product])
async def get_products():
    return read_inventory()

@app.post("/products", response_model=Product)
async def add_product(product: Product):
    products = read_inventory()
    for p in products:
        if p.product_id == product.product_id:
            raise HTTPException(status_code=400, detail="Product ID already exists")
    products.append(product)
    write_inventory(products)
    return product

class QuantityUpdate(BaseModel):
    product_id: str
    quantity_change: int  

@app.put("/products/quantity", response_model=Product)
async def update_quantity(update: QuantityUpdate):
    products = read_inventory()
    for p in products:
        if p.product_id == update.product_id:
            new_quantity = p.quantity + update.quantity_change
            if new_quantity < 0:
                raise HTTPException(status_code=400, detail="Insufficient stock")
            p.quantity = new_quantity
            write_inventory(products)
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str = Path(..., description="ID of the product to retrieve")):
    products = read_inventory()
    for p in products:
        if p.product_id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")
