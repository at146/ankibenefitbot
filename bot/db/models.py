from __future__ import annotations

from datetime import datetime  # noqa: TC003

from sqlalchemy import BIGINT, ForeignKey, MetaData, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class User(Base):
    __tablename__ = "users"

    # id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=True, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    is_clicked_channel: Mapped[bool] = mapped_column(server_default=text("false"))
    is_clicked_article: Mapped[bool] = mapped_column(server_default=text("false"))
    create_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    )

    answers_questions: Mapped[list[AnswerQuestions]] = relationship(back_populates="user", lazy="noload")


class AnswerQuestions(Base):
    __tablename__ = "answers_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    results: Mapped[str]

    user: Mapped[User] = relationship(back_populates="answers_questions", lazy="noload")


class UserChannel(Base):
    __tablename__ = "users_channel"

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=True, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    create_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    )
