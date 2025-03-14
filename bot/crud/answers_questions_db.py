from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db.models import AnswerQuestions


async def insert_answers_questions(
    user_id: int,
    results: str,
    db_session: async_sessionmaker[AsyncSession],
) -> None:
    async with db_session() as session:
        sql = insert(AnswerQuestions).values(user_id=user_id, results=results)
        await session.execute(sql)
        await session.commit()
