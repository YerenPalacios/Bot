from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from db import Base, SessionLocal

class Process(Base):
    __tablename__ = "botprocess"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=None, nullable=True)
    status = Column(Integer, default=0)


def start_process(name):
    db = SessionLocal()
    try:
        p = Process(name=name)
        db.add(p)
        db.commit()
        db.refresh(p)
    finally:
        db.close()

    return p

def end_process(p: Process, status: int):
    p.updated_at = datetime.now(timezone.utc)
    p.status = status
    db = SessionLocal()
    try:
        db.add(p)
        db.commit()
        db.refresh(p)
    finally:
        db.close()

    return p


def get_prpcesses():
    db = SessionLocal()
    try:
        ps = db.query(Process).order_by(Process.created_at.desc()).all()
    finally:
        db.close()

    process = []
    for i in ps:
        duration = 0
        if i.updated_at:
            duration =  i.updated_at - i.created_at
        process.append({'name': i.name, 'status': i.status, "duration": duration, 'created_at': i.created_at})
    return process
