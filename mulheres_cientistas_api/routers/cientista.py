from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from mulheres_cientistas_api.crud import create, delete, get_all, get_one, update
from mulheres_cientistas_api.database import get_session
from mulheres_cientistas_api.models import (
    Cientista,
    CientistaCreate,
    CientistaPublic,
    CientistaUpdate,
    Frase,
    FraseCreate,
)

router = APIRouter(prefix="/cientistas", tags=["Cientistas"])


@router.post("", response_model=CientistaPublic, status_code=201)
def create_cientista(
    cientista_to_create: CientistaCreate, session: Session = Depends(get_session)
):
    return create(session=session, model=Cientista, data=cientista_to_create)


@router.post("/com_frases", response_model=CientistaPublic, status_code=201)
def create_cientista_com_frases(
    cientista_to_create: CientistaCreate,
    session: Session = Depends(get_session)
):
    cientista_id = create(session=session, model=Cientista, data=cientista_to_create).id

    for frase_to_create in cientista_to_create.frases:
        create(session=session, model=Frase, data=FraseCreate(frase=frase_to_create, cientista_id=cientista_id))

    return get_one(session=session, model=Cientista, id=cientista_id)


@router.get("", response_model=list[CientistaPublic], status_code=200)
def get_cientistas(session: Session = Depends(get_session)):
    return get_all(session=session, model=Cientista)


@router.get("/{cientista_id}", response_model=CientistaPublic, status_code=200)
def get_cientista_by_id(cientista_id: int, session: Session = Depends(get_session)):
    cientista = get_one(session=session, model=Cientista, id=cientista_id)
    if cientista is None:
        raise HTTPException(status_code=404, detail="Cientista não encontrada")
    return cientista


@router.put("/{cientista_id}", response_model=CientistaPublic, status_code=200)
def update_cientista(
    cientista_id: int,
    cientista_update: CientistaUpdate,
    session: Session = Depends(get_session),
):
    cientista = update(session=session, model=Cientista, id=cientista_id, data=cientista_update)
    if cientista is None:
        raise HTTPException(status_code=404, detail="Cientista não encontrada")
    return cientista


@router.delete("/{cientista_id}", status_code=204)
def delete_cientista(cientista_id: int, session: Session = Depends(get_session)):
    if not delete(session=session, model=Cientista, id=cientista_id):
        raise HTTPException(status_code=404, detail="Cientista não encontrada")
    return None
