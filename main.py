from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: list[ChoiceBase]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
@app.get("/questions")
async def read_questions(db: db_dependency):
    result = db.query(models.Questions).options(joinedload(models.Questions.choices)).all()
    return result

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")
    return result

@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices are not found")
    return result


@app.post("/questions")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(**choice.model_dump(), question_id=db_question.id)
        db.add(db_choice)
    db.commit()
    return {"message": "Question is created"}

@app.put("/questions/{question_id}")
async def update_question(question_id: int, question: QuestionBase, db: db_dependency):
    db_question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question is not found")
    db_question.question_text = question.question_text # type: ignore
    db.commit()
    db.refresh(db_question)
    db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()
    for choice in question.choices:
        db_choice = models.Choices(**choice.model_dump(), question_id=db_question.id)
        db.add(db_choice)
    db.commit()
    return {"message": "Question is updated"}

@app.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: db_dependency):
    if not db.query(models.Questions).filter(models.Questions.id == question_id).first():
        raise HTTPException(status_code=404, detail="Question is not found")
    db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()
    db.query(models.Questions).filter(models.Questions.id == question_id).delete()
    db.commit()
    return {"message": "Question is deleted"}