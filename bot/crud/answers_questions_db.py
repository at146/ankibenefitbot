from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db.models import AnswerQuestions


async def insert_answer_questions(
    user_id: int,
    results: str,
    db_session: async_sessionmaker[AsyncSession],
) -> int:
    async with db_session() as session:
        answer_questions = AnswerQuestions()
        answer_questions.user_id = user_id
        answer_questions.results = results
        session.add(answer_questions)
        await session.commit()
        return answer_questions.id


async def update_answer_questions(
    id_answer_questions: int,
    user_id: int,
    results: str,
    db_session: async_sessionmaker[AsyncSession],
) -> None:
    async with db_session() as session:
        sql = (
            update(AnswerQuestions)
            .values(results=results)
            .where(AnswerQuestions.id == id_answer_questions, AnswerQuestions.user_id == user_id)
        )
        await session.execute(sql)
        await session.commit()
