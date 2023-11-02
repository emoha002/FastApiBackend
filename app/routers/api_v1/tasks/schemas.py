import enum
import datetime
from uuid import UUID
from pydantic import BaseModel


class TaskState(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class OrderBy(enum.Enum):
    ASC = "ASC"
    DESC = "DESC"


class TaskColor(enum.Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    ORANGE = "ORANGE"
    PURPLE = "PURPLE"
    PINK = "PINK"
    BROWN = "BROWN"
    BLACK = "BLACK"
    WHITE = "WHITE"
    GREY = "GREY"
    CYAN = "CYAN"
    MAGENTA = "MAGENTA"
    LIME = "LIME"
    TEAL = "TEAL"
    LAVENDER = "LAVENDER"
    TAN = "TAN"
    CYCLAMEN = "CYCLAMEN"
    AQUAMARINE = "AQUAMARINE"
    SALMON = "SALMON"
    GOLD = "GOLD"
    OLIVE = "OLIVE"
    MAROON = "MAROON"
    NAVY = "NAVY"
    MINT = "MINT"
    APRICOT = "APRICOT"
    COBALT = "COBALT"
    PEACH = "PEACH"
    INDIGO = "INDIGO"
    CRIMSON = "CRIMSON"
    ORCHID = "ORCHID"
    PLUM = "PLUM"
    LILAC = "LILAC"
    LEMON = "LEMON"
    TURQUOISE = "TURQUOISE"
    RASPBERRY = "RASPBERRY"
    VIOLET = "VIOLET"
    SAND = "SAND"
    BEIGE = "BEIGE"
    MINT_GREEN = "MINT_GREEN"
    PEANUT = "PEANUT"
    PEAR = "PEAR"
    CHERRY = "CHERRY"
    BANANA = "BANANA"
    COFFEE = "COFFEE"
    CHOCOLATE = "CHOCOLATE"
    CREAM = "CREAM"
    CARROT = "CARROT"
    TOMATO = "TOMATO"
    CINNAMON = "CINNAMON"
    PINEAPPLE = "PINEAPPLE"
    COCONUT = "COCONUT"
    PISTACHIO = "PISTACHIO"
    MANGO = "MANGO"
    PAPAYA = "PAPAYA"


class TaskCreateSchema(BaseModel):
    title: str
    description: str | None
    state: TaskState
    priority: TaskPriority
    color: TaskColor | None = TaskColor.PURPLE
    task_deadline: datetime.date


class TaskOutSchema(TaskCreateSchema):
    task_id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class UpdateTaskSchema(BaseModel):
    # it's the same us the TaskCreateSchema but all the attributes are Optional
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None
    priority: TaskPriority | None = None
    color: TaskColor | None = None
    task_deadline: datetime.date | None = None


class GetTasksFilterSchema(BaseModel):
    title: str | None = None
    state: TaskState | None = None
    priority: TaskPriority | None = None
    color: TaskColor | None = None
    start_time: datetime.date | None = datetime.date.today()
    end_time: datetime.date | None = datetime.date.today() + datetime.timedelta(days=7)
    order_by: OrderBy | None = OrderBy.ASC
