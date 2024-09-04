from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class CientistaBase(SQLModel):
    nome: str = Field(index=True, nullable=False)
    descrição: str = Field(nullable=False)
    data_nascimento: date = Field(nullable=False)
    data_morte: date | None = Field(default=None)
    img_link: str = Field(nullable=False)
    wikipedia_link: str = Field(nullable=False)


class Cientista(CientistaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    frases: list["Frase"] = Relationship(back_populates="cientista", cascade_delete=True)


class CientistaCreate(CientistaBase):
    frases: list[str] | None = Field(exclude=True)


class CientistaPublic(CientistaBase):
    id: int
    frases: list["FrasePublic"] = []


class CientistaUpdate(SQLModel):
    nome: str | None = Field(default=None)
    descrição: str | None = Field(default=None)
    data_nascimento: date | None = Field(default=None)
    data_morte: date | None = Field(default=None)
    img_link: str | None = Field(default=None)
    wikipedia_link: str | None = Field(default=None)


class FraseBase(SQLModel):
    frase: str = Field(nullable=False)
    cientista_id: int = Field(foreign_key="cientista.id", nullable=False)


class Frase(FraseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cientista: Cientista = Relationship(back_populates="frases")


class FraseCreate(FraseBase):
    pass


class FrasePublic(FraseBase):
    id: int


class FraseUpdate(SQLModel):
    frase: str | None = Field(default=None)
