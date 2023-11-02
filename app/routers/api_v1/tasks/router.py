from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.routers.api_v1.auth.dependencies import get_current_user
from app.routers.api_v1.auth.models import User
from app.routers.api_v1.tasks.exceptions import NOTHING_TO_UPDATE
from app.routers.api_v1.tasks.models import DBTask

from app.routers.api_v1.tasks.schemas import (
    GetTasksFilterSchema,
    TaskCreateSchema,
    TaskOutSchema,
    UpdateTaskSchema,
)
from app.routers.api_v1.tasks.service import (
    add_new_task,
    delete_task_service,
    update_task_service,
)


task_router = APIRouter(
    prefix="/task",
    tags=["Task"],
    responses={404: {"description": "Incorrect Not found"}},
)


@task_router.post(
    "/add_tasks",
    status_code=201,
    response_model=TaskOutSchema,
)
async def get_tasks(
    task_create: TaskCreateSchema,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    print(user)
    return await add_new_task(db_session=db_session, task_create=task_create, user=user)


@task_router.get("/get_task/{task_id}", response_model=TaskOutSchema, status_code=200)
async def get_task(
    task_id: UUID,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    print(task_id)
    return await DBTask.get_task_by_id(
        db_session=db_session, task_id=task_id, user=user
    )


@task_router.post("/get_all_tasks", response_model=list[TaskOutSchema], status_code=200)
async def get_all_tasks(
    filter: GetTasksFilterSchema,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    return await DBTask.get_all_my_tasks(
        db_session=db_session, user=user, filter=filter
    )


# update task
@task_router.put(
    "/update_task/{task_id}", response_model=dict[str, str], status_code=200
)
async def update_task(
    task_id: UUID,
    update_task: UpdateTaskSchema,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    if not update_task.model_dump(exclude_unset=True):
        raise NOTHING_TO_UPDATE
    await update_task_service(
        db_session=db_session,
        update_task=update_task,
        user=user,
        task_id=task_id,
    )
    return {"message": "task updated successfully"}


@task_router.delete(
    "/delete_task/{task_id}",
    response_model=dict[str, str],
    status_code=200,
)
async def delete_task(
    task_id: UUID,
    user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db),
):
    await delete_task_service(
        db_session=db_session,
        user=user,
        task_id=task_id,
    )
    return {"message": "task deleted successfully"}


"""
TODO
    - [x] Create task
    - [x] Get task
    - [x] Get all tasks
    - [x] Update task
    - [x] Delete task
    - [ ] Get all tasks by user
        - query params can be
        - title, state, priority, color, task_deadline
        - fetchs all the tasks by user id
        - not time range will be added since it's optional
"""
