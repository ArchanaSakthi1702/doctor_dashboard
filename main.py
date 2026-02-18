from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
import asyncio


import uuid

import models,schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/spine-data")
def receive_spine_data(
    data: schemas.SpineDataCreate,
    db: Session = Depends(get_db)
):
    db_data = models.SpineData(
        id=str(uuid.uuid4()),
        patient_id=data.patient_id,
        upper=data.upper,
        middle=data.middle,
        lower=data.lower,
        cobb=data.cobb
    )

    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return {"status": "stored"}


@app.websocket("/ws/spine/{patient_id}")
async def websocket_endpoint(websocket: WebSocket, patient_id: str):
    await websocket.accept()

    db: Session = SessionLocal()   # 👈 manually create DB session

    try:
        while True:
            data = (
                db.query(models.SpineData)
                .filter(models.SpineData.patient_id == patient_id)
                .order_by(desc(models.SpineData.created_at))
                .first()
            )

            if data:
                await websocket.send_json({
                    "upper": data.upper,
                    "middle": data.middle,
                    "lower": data.lower,
                    "cobb": data.cobb,
                    "timestamp": str(data.created_at)
                })

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("WebSocket disconnected")

    finally:
        db.close()   # 👈 very important
