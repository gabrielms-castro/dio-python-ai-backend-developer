from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from workoutapi.contrib.models import BaseModel


class AtletaModel(BaseModel):
    __tablename__ = "atletas"  # Nome da tabela no Banco de Dados

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relacionamentos
    categoria: Mapped["CategoriaModel"] = relationship(back_populates="atleta", lazy="selectin")
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.pk_id")
    )  # nome_tabela.nome_atributo

    centro_treinamento: Mapped["CentroTreinamentoModel"] = relationship(
        back_populates="atleta", lazy="selectin"
    )
    centro_treinamento_id: Mapped[int] = mapped_column(
        ForeignKey("centros_treinamento.pk_id")
    )
