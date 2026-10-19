import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, bookings, cars, customers, inspections, maintenance, payments

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def log_request_time(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} {request.url.path} took {process_time:.4f} seconds")
    return response

for route_module in (auth, cars, customers, bookings, inspections, payments, maintenance):
    app.include_router(route_module.router)
