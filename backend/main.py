from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
import json
import os
import datetime
from fastapi.middleware.cors import CORSMiddleware
#user sends for creating task
class TaskCreate(BaseModel):
    description: str

#what the api returns -- the full task
class Task(BaseModel):
    id: int
    description: str
    status : str
    createdAt : str
    updatedAt : str

#what the user sends to update the model
class TaskUpdate(BaseModel):
    description: str | None = None
    status: str | None = None


def load_tasks():
    if not os.path.exists("tasks.json"):
        return []
    with open("tasks.json", "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open ("tasks.json",'w') as file:
        json.dump(tasks,file, indent=2)
def now():
    return datetime.datetime.now().isoformat()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/tasks", response_model= list[Task])
def list_tasks(status:str | None = None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"]== status]
    return tasks


@app.post("/tasks", response_model= Task, status_code=201)
def create_task(task: TaskCreate):
    tasks=load_tasks()
    new_id = max((t['id']for t in tasks),default=0)+1
    current_time = now()
    new_task ={
        "id": new_id,
        "description": task.description,
        "status": "todo",
        "createdAt": current_time,
        "updatedAt": current_time
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    tasks=load_tasks()
    for t in tasks:
        if (t['id']== task_id):
            if task_update.description is not None:
                t['description'] = task_update.description
            if task_update.status is not None:
                t['status'] = task_update.status
            t['updatedAt']= now()
            save_tasks(tasks)
            return t
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete ("/tasks/{task_id}")
def delete_task(task_id:int):
    tasks=load_tasks()
    for i,t in enumerate(tasks):
        if(t['id']==task_id):
            del tasks[i]
            save_tasks(tasks)
            return {"message":"Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/")
def read_root():
    return {"message":"Task Tracker API is running"}