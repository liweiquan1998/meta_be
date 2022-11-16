from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from utils import web_try, sxtimeit

router_user = APIRouter(
    prefix="/user",
    tags=["user-用户管理"],
)



@router_user.get("/")
@web_try()
@sxtimeit
def get_users(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_users(db), params)


@router_user.get("/getOnce/{item_id}")
@web_try()
@sxtimeit
def get_user_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_user_once(db=db, item_id=item_id)


@router_user.put("/{item_id}")
@web_try()
@sxtimeit
def update_user(item_id: int, update_item: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db,item_id=item_id,update_item=update_item)


@router_user.post("/")
@web_try()
@sxtimeit
def add_user(item: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, item=item)
