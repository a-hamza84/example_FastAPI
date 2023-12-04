from datetime import date, datetime

from sqlalchemy import select, delete, update
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from models.base import SESSION
from models.tasks import Task

from utils.deps import check_jwt

router = APIRouter()


def get_all_tasks(page):
    '''
    Get All items 
    @param page: Page number of list (int)
    @return List of tasks (list)
    '''
    page_size = 10
    stmt = select(Task).offset(page_size).limit(page * page_size)
    obj = SESSION.execute(stmt).all()
    result_dict = [u.__dict__ for u in obj]
    return result_dict


def search_task(title):
    '''
    Get item with title matching 
    @param title: Search Term (str)
    @return List of tasks (list)
    '''
    page_size = 10
    stmt = (
        select(Task)
        .filter(Task.title.like(f'%{title}%'))
        .offset(page_size)
        .limit(page * page_size)
    )
    obj = SESSION.execute(stmt).all()
    result_dict = [u.__dict__ for u in obj]
    return result_dict


def update_task(id, task):
    '''
    Update Task
    @param id: task ID
    @param task: New task variables (dict)
    @return None
    '''
    stmt = (
        update(Task)
        .where(Task.id == id)
        .values(
            description=task['description'],
            title=task['title'],
            end_date=task['end_date'],
        )
    )
    SESSION.execute(stmt)


def delete_one_task(id):
    '''
    Delete a task with specific id 
    @param id: Task ID (int)
    @return None
    '''
    stmt = delete(Task).where(Task.id == id)
    SESSION.execute(stmt)


@router.post('/add_task')
def add_task(req: dict, jwt_status: bool = Depends(check_jwt)):
    if not jwt_status:
        return JSONResponse(
            status_code=401, content={"error": "Token Expired or Invalid"}
        )
    start_date = datetime.strptime(req['start_date'], '%d-%m-%Y')
    end_date = datetime.strptime(req['end_date'], '%d-%m-%Y')
    task_obj = Task(
        title=req['title'],
        description=req['description'],
        start_date=start_date,
        end_date=end_date,
        created_by=req['user_id'],
        created_at=date.today(),
    )
    task_obj.save_task()
    return JSONResponse(content={"message": "Task Create Success"})


@router.delete('/delete_task/{id}')
def delete_task(id: int, jwt_status: bool = Depends(check_jwt)):
    if not jwt_status:
        return JSONResponse(
            status_code=401, content={"error": "Token Expired or Invalid"}
        )
    delete_one_task(id)
    return JSONResponse(content={"message": "Task Deleted"})


@router.put('/edit_task/{id}')
def edit_task(req: dict, id: int, jwt_status: bool = Depends(check_jwt)):
    if not jwt_status:
        return JSONResponse(
            status_code=401, content={"error": "Token Expired or Invalid"}
        )
    update_task(id, req)
    return JSONResponse(content={"message": "Update Task"})


@router.post('/task_listings')
def login(req: dict, jwt_status: bool = Depends(check_jwt)):
    if not jwt_status:
        return JSONResponse(
            status_code=401, content={"error": "Token Expired or Invalid"}
        )
    page = req['page']
    items = get_all_tasks(page)
    return JSONResponse(
        content={"message": "Tasks fetch Success", "items": items}
    )


@router.get('/search_task')
def login(req: dict, jwt_status: bool = Depends(check_jwt)):
    if not jwt_status:
        return JSONResponse(
            status_code=401, content={"error": "Token Expired or Invalid"}
        )
    search = req['search_term']
    page = req['page']
    items = search_task(page, search)
    return JSONResponse(content={"message": "Search Success", "items": items})
