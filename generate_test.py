import json
from faker import Faker
from enum import Enum
import requests

# Initialize faker
fake = Faker()


# Define your enums
class TaskState(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskColor(Enum):
    PURPLE = "PURPLE"
    # Add other colors here...

    # Define your headers


headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiZWxraWRhbmVtYXJpYW05OUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImJlbGxhX2ttIiwiZnVsbG5hbWUiOiJhYmVsIGtpZGFuZW1hcmlhbSIsImlkIjoiNTc0MjEzMDMtNGM3OS00YjVhLTk0ZmYtMTUyZTZiMTliYjJiIiwiaXNfYWN0aXZhdGVkIjpmYWxzZSwiaXNfYWRtaW4iOmZhbHNlLCJleHAiOjE2OTkwMzQ0ODJ9.hRUcUx_XHedYX0HTAkneLbVtcHww1tzcw0FYbd63aSY",
    "Content-Type": "application/json",
}


def generate_fake_request():
    # Generate fake data
    title = fake.sentence(nb_words=6)
    description = fake.text(max_nb_chars=200)
    state = fake.random_element(elements=[e.value for e in TaskState])
    priority = fake.random_element(elements=[e.value for e in TaskPriority])
    color = fake.random_element(elements=[e.value for e in TaskColor])
    task_deadline = (fake.date_time_between(start_date="-30d", end_date="+30d")).date()

    # Prepare your data
    data = {
        "title": title,
        "description": description,
        "state": state,
        "priority": priority,
        "color": color,
        "task_deadline": task_deadline.isoformat(),
    }

    # Convert dict to json
    data_json = json.dumps(data)
    return data_json


for _ in range(30):
    data_json = generate_fake_request()
    response = requests.post(
        "http://0.0.0.0:8000/api_v1/task/add_tasks", headers=headers, data=data_json
    )
    print(response.status_code)


# Use the function

# Print the response
# print(response.json())
