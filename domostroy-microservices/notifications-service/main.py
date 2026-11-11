from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Notifications Service')

class Notification(BaseModel):
    recipient: str
    message: str

@app.post('/notify')
def send_notification(notif: Notification):
    print(f'[NOTIFICATION LOG] To: {notif.recipient} | Content: {notif.message}')
    return {'status': 'sent', 'recipient': notif.recipient, 'log': 'Notification processed'}

