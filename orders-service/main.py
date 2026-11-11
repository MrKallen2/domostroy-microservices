import os
import time
from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel

app = FastAPI(title='Orders Service')

DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'app')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', '1234')

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except Exception:
            time.sleep(2)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            client_name VARCHAR(100),
            service_type VARCHAR(100),
            total_price NUMERIC
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.on_event('startup')
def startup_event():
    init_db()

class OrderCreate(BaseModel):
    client_name: str
    service_type: str
    total_price: float

@app.post('/orders')
def create_order(order: OrderCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO orders (client_name, service_type, total_price) VALUES (%s, %s, %s) RETURNING id;',
        (order.client_name, order.service_type, order.total_price)
    )
    order_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {'status': 'success', 'order_id': order_id, 'message': 'Saved to PostgreSQL database successfully'}

@app.get('/orders')
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, client_name, service_type, total_price FROM orders;')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{'id': r[0], 'client_name': r[1], 'service_type': r[2], 'total_price': float(r[3])} for r in rows]

