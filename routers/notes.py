from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Note, NoteCreate

router = APIRouter()


@router.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: Session = Depends(get_session)):
    db_note = Note(title=note.title, content=note.content)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@router.get("/notes")
def get_notes(session: Session = Depends(get_session)):
    notes = session.exec(select(Note).order_by(Note.id.desc())).all()
    return notes


@router.get("/notes/{note_id}")
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="ノートが見つかりません")
    return note


@router.put("/notes/{note_id}")
def update_note(
    note_id: int, note_data: NoteCreate, session: Session = Depends(get_session)
):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="ノートが見つかりません")
    note.title = note_data.title
    note.content = note_data.content
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="ノートが見つかりません")
    session.delete(note)
    session.commit()
    return {"message": "ノートを削除しました"}