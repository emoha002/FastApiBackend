from fastapi import APIRouter


task_router = APIRouter(
    prefix="/task",
    tags=["Task"],
    responses={404: {"description": "Incorrect Not found"}},
)


@task_router.get("/get_tasks")
async def get_tasks():
    return {"message" "Hello World"}
