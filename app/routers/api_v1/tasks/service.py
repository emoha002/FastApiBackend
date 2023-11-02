from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.tasks.exceptions import TASK_NOT_FOUND
from app.routers.api_v1.tasks.models import DBTask
from app.routers.api_v1.tasks.schemas import TaskCreateSchema, UpdateTaskSchema


async def add_new_task(
    db_session: AsyncSession,
    task_create: TaskCreateSchema,
    user: User,
):
    print(task_create)
    print("=========================================")
    try:
        db_task: DBTask = DBTask(user_id=user.id, **task_create.model_dump())
        await db_task.save(db_session=db_session)
        return db_task
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
        ) from ex


async def update_task_service(
    db_session: AsyncSession, update_task: UpdateTaskSchema, user: User, task_id: UUID
):
    query = (
        update(DBTask)
        .where(DBTask.task_id == task_id, DBTask.user_id == user.id)
        .values(update_task.model_dump(exclude_unset=True))
    )

    affected_rows = await db_session.execute(query)
    await db_session.commit()
    if affected_rows.rowcount == 0:
        raise TASK_NOT_FOUND


async def delete_task_service(
    db_session: AsyncSession,
    user: User,
    task_id: UUID,
):
    query = delete(DBTask).where(DBTask.user_id == user.id, DBTask.task_id == task_id)

    affected_rows = await db_session.execute(query)
    await db_session.commit()
    if affected_rows.rowcount == 0:
        raise TASK_NOT_FOUND
