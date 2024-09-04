from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from mulheres_cientistas_api.crud import create, delete, get_all, get_one, update
from mulheres_cientistas_api.database import get_session
from mulheres_cientistas_api.models import (
    Frase,
    FraseCreate,
    FrasePublic,
    FraseUpdate,
)

router = APIRouter(prefix="/frases", tags=["Frases"])


@router.post("", response_model=FrasePublic, status_code=201)
def create_frase(frase_to_create: FraseCreate, session: Session = Depends(get_session)):
    try:
        return create(session=session, model=Frase, data=frase_to_create)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Cientista especificada não existe")


@router.get("", response_model=list[FrasePublic], status_code=200)
def get_frases(session: Session = Depends(get_session)):
    return get_all(session=session, model=Frase)


@router.get("/{frase_id}", response_model=FrasePublic, status_code=200)
def get_frase_by_id(frase_id: int, session: Session = Depends(get_session)):
    frase = get_one(session=session, model=Frase, id=frase_id)
    if frase is None:
        raise HTTPException(status_code=404, detail="Frase não encontrada")
    return frase


@router.put("/{frase_id}", response_model=FrasePublic, status_code=200)
def update_frase(
    frase_id: int,
    frase_update: FraseUpdate,
    session: Session = Depends(get_session),
):
    frase = update(session=session, model=Frase, id=frase_id, data=frase_update)
    if frase is None:
        raise HTTPException(status_code=404, detail="Frase não encontrada")
    return frase


@router.delete("/{frase_id}", status_code=204)
def delete_frase(frase_id: int, session: Session = Depends(get_session)):
    if not delete(session=session, model=Frase, id=frase_id):
        raise HTTPException(status_code=404, detail="Frase não encontrada")
    return None
