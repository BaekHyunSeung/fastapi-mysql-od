from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app import model
from app.database import Base, engine, get_db

app = FastAPI()


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

@app.post("/save-od")
async def save_object_detection(data: dict, db: Session = Depends(get_db)):
    new_record = model.DetectionResult(
        image_name=data.get("image_name"),
        label=data.get("label"),
        confidence=data.get("conf"),
        bbox=data.get("bbox"),
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {"status" : "success", "id" : new_record.id}