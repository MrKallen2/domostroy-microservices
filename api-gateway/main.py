import os
from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI(title="API Gateway - Domostroy")

ORDERS_URL = os.getenv("ORDERS_SERVICE_URL", "http://orders-service:8002")
NOTIF_URL = os.getenv("NOTIF_SERVICE_URL", "http://notifications-service:8003")

class ClientOrderRequest(BaseModel):
    client_name: str
    service_type: str
    total_price: float
    email: str

@app.post("/api/v1/process-order")
def process_order(data: ClientOrderRequest):
    order_payload = {
        "client_name": data.client_name,
        "service_type": data.service_type,
        "total_price": data.total_price
    }
    try:
        resp = requests.post(f"{ORDERS_URL}/orders", json=order_payload, timeout=5)
        order_data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orders service connection error: {str(e)}")

    notif_payload = {
        "recipient": data.email,
        "message": f"Уважаемый(-ая) {data.client_name}, ваш заказ на услуги '{data.service_type}' успешно принят."
    }
    try:
        requests.post(f"{NOTIF_URL}/notify", json=notif_payload, timeout=5)
    except Exception:
        pass

    return {
        "gateway_status": "success",
        "order_result": order_data
    }

@app.get("/api/v1/orders")
def get_all_orders():
    try:
        resp = requests.get(f"{ORDERS_URL}/orders", timeout=5)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orders service error: {str(e)}")