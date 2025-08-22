from fastapi import FastAPI, Request, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY
from pydantic import BaseModel
from starlette.responses import Response
import time
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "tajna_za_jwt" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="User Service")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


REQUEST_COUNT = Counter('user_service_requests_total', 'Ukupan broj HTTP zahtjeva', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('user_service_request_latency_seconds', 'Latencija HTTP zahtjeva', ['endpoint'])
ERROR_COUNT = Counter(
    'user_service_errors_total',
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


users = {
    "user1": {"password": "pass1"},
    "user2": {"password": "pass2"},
    "admin1": {"password": "adminpass1"},
    "admin2": {"password": "adminpass2"}
}

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(req: LoginRequest):
    user = users.get(req.username)
    if user and user["password"] == req.password:
        token_data = {"sub": req.username}
        access_token = create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/register")
async def register(req: RegisterRequest):
    if req.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[req.username] = {"password": req.password}
    return {"message": "User registered successfully", "user": req.username}
