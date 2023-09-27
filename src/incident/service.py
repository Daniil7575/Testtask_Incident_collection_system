from src.incident.models import Problem
from sqlalchemy.ext.asyncio import AsyncSession
from src.incident.models import Problem
import sqlalchemy as sa


async def add_problem(
    problem_hash: str, header: dict, body: dict, session: AsyncSession
):
    stmt = (
        sa.insert(Problem)
        .values(hash_value=problem_hash, header=header, body=body)
        .returning(Problem.hash_value)
    )
    new_problem = await session.execute(stmt)
    await session.commit()
    return new_problem.mappings().one()
