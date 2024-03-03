from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4

app = FastAPI()

class ToDoItem(BaseModel):
    id: Optional[UUID] = uuid4()
    title: str
    description: Optional[str] = None
    completed: bool = False


todo_items: List[ToDoItem] = []

templates = Jinja2Templates(directory="templates")


# Read 기능
@app.get("/todos/", response_class=HTMLResponse)
def read_todos(request: Request):
    return templates.TemplateResponse("todo_list.html", {"request": request, "todo_items": todo_items})

# Create 기능
@app.post("/todos/")
def create_todo(request: Request, title: str = Form(...), description: str = Form(""), completed: bool = Form(False)):
    todo_item = ToDoItem(title=title, description=description, completed=completed)
    todo_items.append(todo_item)
    return RedirectResponse(url='/todos/', status_code=303)

# Update 기능
@app.post("/todos/{todo_id}/update")
def update_todo(todo_id: UUID, request: Request, title: str = Form(...), description: str = Form(""), completed: bool = Form(False)):
    for todo_item in todo_items:
        if todo_item.id == todo_id:
            todo_item.title = title
            todo_item.description = description
            todo_item.completed = completed
            return RedirectResponse(url='/todos/', status_code=303)
    raise HTTPException(status_code=404, detail="ToDo not found")

# Delete 기능
@app.post("/todos/{todo_id}/delete")
def delete_todo(todo_id: UUID, request: Request):
    for index, todo_item in enumerate(todo_items):
        if todo_item.id == todo_id:
            del todo_items[index]
            return RedirectResponse(url='/todos/', status_code=303)
    raise HTTPException(status_code=404, detail="ToDo not found")
